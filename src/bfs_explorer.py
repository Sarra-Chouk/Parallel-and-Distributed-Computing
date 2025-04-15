"""
This module implements the BFSExplorer class that solves the maze
using a bidirectional breadth-first search algorithm.
After a solution is found, it applies a path-smoothing routine to remove unnecessary moves.
"""

import time
from collections import deque
from typing import List, Tuple

def line_of_sight(maze, p: Tuple[int, int], q: Tuple[int, int]) -> bool:
    """
    Check if there is a clear line-of-sight between points p and q in the maze.
    Uses a simple Bresenham-based algorithm. Assumes maze.grid[y][x]==0 means free.
    """
    x0, y0 = p
    x1, y1 = q
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    n = 1 + dx + dy
    x_inc = 1 if x1 > x0 else -1
    y_inc = 1 if y1 > y0 else -1
    error = dx - dy
    dx *= 2
    dy *= 2

    for _ in range(n):
        # If there's a wall at (x, y), no direct path exists.
        if maze.grid[y][x] != 0:
            return False
        # Move along the line.
        if error > 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
    return True

def smooth_path(maze, path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Given a path (list of grid cells), remove unnecessary intermediate nodes.
    For each node, look as far ahead as possible for which a direct line-of-sight exists.
    """
    if not path:
        return []
    
    new_path = [path[0]]
    i = 0
    while i < len(path) - 1:
        # Try to jump from path[i] as far forward as possible.
        j = len(path) - 1
        while j > i + 1:
            if line_of_sight(maze, path[i], path[j]):
                break
            j -= 1
        new_path.append(path[j])
        i = j
    return new_path

class BFSExplorer:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.path: List[Tuple[int, int]] = []
        self.backtracks = 0  # BFS does not perform backtracking explicitly

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        
        # Special case: if start equals end.
        if self.start == self.end:
            self.path = [self.start]
            return time.time() - start_time, self.path
        
        # Initialize two frontiers: one from the start and one from the end.
        frontier_forward = deque([self.start])
        frontier_backward = deque([self.end])
        came_from_forward = {self.start: None}
        came_from_backward = {self.end: None}
        meeting_point = None

        # Alternate expanding the forward and backward frontiers.
        while frontier_forward and frontier_backward and meeting_point is None:
            # Expand forward frontier.
            current_forward = frontier_forward.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current_forward[0] + dx, current_forward[1] + dy)
                if (0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height and
                    self.maze.grid[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from_forward):
                    came_from_forward[neighbor] = current_forward
                    frontier_forward.append(neighbor)
                    if neighbor in came_from_backward:
                        meeting_point = neighbor
                        break
            if meeting_point is not None:
                break

            # Expand backward frontier.
            current_backward = frontier_backward.popleft()
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current_backward[0] + dx, current_backward[1] + dy)
                if (0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height and
                    self.maze.grid[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from_backward):
                    came_from_backward[neighbor] = current_backward
                    frontier_backward.append(neighbor)
                    if neighbor in came_from_forward:
                        meeting_point = neighbor
                        break

        if meeting_point is not None:
            # Reconstruct forward path from start to meeting point.
            forward_path = []
            current = meeting_point
            while current is not None:
                forward_path.append(current)
                current = came_from_forward[current]
            forward_path.reverse()
            # Reconstruct backward path from meeting point to end.
            backward_path = []
            current = came_from_backward[meeting_point]
            while current is not None:
                backward_path.append(current)
                current = came_from_backward[current]
            raw_path = forward_path + backward_path
            # Smooth the path to eliminate unnecessary moves.
            self.path = smooth_path(self.maze, raw_path)
        else:
            self.path = []

        time_taken = time.time() - start_time
        return time_taken, self.path
"""
This module implements the BFSExplorer class that solves the maze
using a bidirectional breadth-first search algorithm.
"""

import time
from collections import deque
from typing import List, Tuple

class BFSExplorer:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.path: List[Tuple[int, int]] = []
        self.backtracks = 0  # BFS does not perform backtracking explicitly

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        
        # Special case: start is the same as end.
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
                    # Check if this neighbor is in the backward frontier.
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
                    # Check if this neighbor is in the forward frontier.
                    if neighbor in came_from_forward:
                        meeting_point = neighbor
                        break

        if meeting_point is not None:
            # Reconstruct the forward path from start to meeting point.
            forward_path = []
            current = meeting_point
            while current is not None:
                forward_path.append(current)
                current = came_from_forward[current]
            forward_path.reverse()
            # Reconstruct the backward path from meeting point to end.
            backward_path = []
            current = came_from_backward[meeting_point]
            while current is not None:
                backward_path.append(current)
                current = came_from_backward[current]
            self.path = forward_path + backward_path
        else:
            self.path = []

        time_taken = time.time() - start_time
        return time_taken, self.path
"""
This module implements the BFSExplorer class that solves the maze
using a breadth-first search algorithm.
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
        self.backtracks = 0  # BFS does not backtrack explicitly

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        queue = deque()
        queue.append(self.start)
        came_from = {}
        came_from[self.start] = None

        found = False
        while queue:
            current = queue.popleft()
            if current == self.end:
                found = True
                break
            x, y = current
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_cell = (x + dx, y + dy)
                if (0 <= next_cell[0] < self.maze.width and 0 <= next_cell[1] < self.maze.height and
                    self.maze.grid[next_cell[1]][next_cell[0]] == 0 and next_cell not in came_from):
                    queue.append(next_cell)
                    came_from[next_cell] = current

        if found:
            # Reconstruct path from end to start.
            current = self.end
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            self.path = path
        else:
            self.path = []
        end_time = time.time()
        time_taken = end_time - start_time
        return time_taken, self.path
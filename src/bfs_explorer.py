"""
This module implements the BFSExplorer class that solves the maze
using a breadth-first search (BFS) algorithm.
"""

import time
from collections import deque
from typing import List, Tuple

class BFSExplorer:
    def __init__(self, maze):
        """
        Initialize the BFSExplorer with the given maze.
        """
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.path: List[Tuple[int, int]] = []
        self.backtracks = 0  # BFS is non-backtracking

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Perform BFS to find the shortest path from start to end.

        Returns:
            time_taken (float): Time taken to solve the maze.
            path (List[Tuple[int, int]]): List of (x, y) coordinates representing the path.
        """
        start_time = time.time()

        # Initialize BFS queue and visited map
        queue = deque()
        queue.append(self.start)
        came_from = {self.start: None}

        found = False
        while queue:
            current = queue.popleft()

            # Check if goal reached
            if current == self.end:
                found = True
                break

            x, y = current
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_cell = (x + dx, y + dy)

                # Check if neighbor is valid and unvisited
                if (0 <= next_cell[0] < self.maze.width and
                    0 <= next_cell[1] < self.maze.height and
                    self.maze.grid[next_cell[1]][next_cell[0]] == 0 and
                    next_cell not in came_from):
                    
                    queue.append(next_cell)
                    came_from[next_cell] = current

        if found:
            # Reconstruct path by backtracking from end to start
            current = self.end
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            self.path = path
        else:
            self.path = []

        time_taken = time.time() - start_time
        return time_taken, self.path
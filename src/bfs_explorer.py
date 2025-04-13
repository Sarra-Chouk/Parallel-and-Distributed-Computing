"""
Breadth-First Search (BFS) Solver for the Maze.
This solver will find the shortest path in an unweighted grid maze.
"""

import time
from collections import deque

class BFSSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_pos
        self.goal = maze.end_pos
        self.width = maze.width
        self.height = maze.height

    def solve(self):
        """Run BFS on the maze and return (path, time_taken)."""
        start_time = time.time()
        queue = deque()
        queue.append(self.start)
        came_from = {self.start: None}

        while queue:
            current = queue.popleft()
            if current == self.goal:
                break

            x, y = current
            # Explore the four neighbors: right, left, down, up.
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (x + dx, y + dy)
                if (0 <= neighbor[0] < self.width and 
                    0 <= neighbor[1] < self.height and 
                    self.maze.grid[neighbor[1]][neighbor[0]] == 0 and 
                    neighbor not in came_from):
                    queue.append(neighbor)
                    came_from[neighbor] = current

        if self.goal not in came_from:
            print("No path found!")
            return None, time.time() - start_time

        # Reconstruct path by stepping backwards from goal
        current = self.goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        end_time = time.time()
        return path, end_time - start_time

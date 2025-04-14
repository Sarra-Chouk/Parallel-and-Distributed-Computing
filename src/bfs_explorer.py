"""
Breadth-First Search (BFS) Solver for the Maze.
This solver finds the shortest path in an unweighted grid maze.
"""

import time
from collections import deque

class BFSSolver:
    def __init__(self, maze):
        """
        Initialize the BFS solver with the maze instance.
        
        Args:
            maze: Maze object containing the grid, start and end positions.
        """
        self.maze = maze
        self.start = maze.start_pos
        self.goal = maze.end_pos
        self.width = maze.width
        self.height = maze.height

    def solve(self):
        """
        Solve the maze using Breadth-First Search.
        
        Returns:
            path (List[Tuple[int, int]]): The shortest path from start to goal.
            time_taken (float): Time taken to compute the solution.
        """
        start_time = time.time()

        # Initialize BFS queue and tracking dictionary
        queue = deque()
        queue.append(self.start)
        came_from = {self.start: None}  # Maps each cell to its predecessor

        while queue:
            current = queue.popleft()

            # Exit condition: goal reached
            if current == self.goal:
                break

            x, y = current
            # Explore four adjacent neighbors: right, left, down, up
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (x + dx, y + dy)
                
                if (
                    0 <= neighbor[0] < self.width and 
                    0 <= neighbor[1] < self.height and 
                    self.maze.grid[neighbor[1]][neighbor[0]] == 0 and 
                    neighbor not in came_from
                ):
                    queue.append(neighbor)
                    came_from[neighbor] = current

        # If goal was not reached
        if self.goal not in came_from:
            print("No path found!")
            return None, time.time() - start_time

        # Reconstruct path from goal to start using the came_from map
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

        end_time = time.time()
        return path, end_time - start_time
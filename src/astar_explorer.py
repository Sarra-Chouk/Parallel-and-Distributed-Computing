"""
A* Explorer module (no visualization).

Implements the A* algorithm for finding the shortest path from the
maze's start position to the goal using Manhattan distance.
Returns the path and total time taken.
"""

import time
import heapq

class AStarExplorer:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_pos
        self.goal = maze.end_pos
        self.width = maze.width
        self.height = maze.height

    def heuristic(self, a, b):
        """Return Manhattan distance between two points."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        """Build path by walking back from goal to start."""
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        return path[::-1]  # Reverse to start from the beginning

    def solve(self):
        """
        Run A* algorithm. Return (path, time_taken).
        If no path found, return (None, time_taken).
        """
        start_time = time.time()
        open_set = [(0, self.start)]  # Priority queue ordered by f = g + h
        came_from = {self.start: None}  # To reconstruct path
        cost_so_far = {self.start: 0}   # Tracks g cost
        found = False

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == self.goal:
                found = True
                break

            x, y = current
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (x + dx, y + dy)
                if not (0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height):
                    continue  # Out of bounds
                if self.maze.grid[neighbor[1]][neighbor[0]] == 1:
                    continue  # Wall

                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, self.goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current

        end_time = time.time()

        if not found:
            print("A* Explorer: No path found!")
            return None, end_time - start_time

        path = self.reconstruct_path(came_from, self.goal)
        return path, end_time - start_time
"""
A* Explorer module (no visualization).

This module implements the A* algorithm to find a path from the maze’s
start position to the goal using Manhattan distance as the heuristic.
It returns a tuple containing the solution path (list of cell coordinates)
and the total time taken to compute the solution.
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
        """Compute Manhattan distance between points a and b."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        """Reconstructs the path from start to goal using the came_from map."""
        path = []
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def solve(self):
        """
        Execute A* search on the maze and return (path, time_taken).
        If no path is found, returns (None, elapsed_time).
        """
        start_time = time.time()
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {self.start: None}
        cost_so_far = {self.start: 0}
        found = False

        while open_set:
            current_priority, current = heapq.heappop(open_set)
            if current == self.goal:
                found = True
                break

            x, y = current
            # Explore the four cardinal neighbors.
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (x + dx, y + dy)
                # Check bounds.
                if not (0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height):
                    continue
                # Skip walls.
                if self.maze.grid[neighbor[1]][neighbor[0]] == 1:
                    continue

                new_cost = cost_so_far[current] + 1  # uniform step cost
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
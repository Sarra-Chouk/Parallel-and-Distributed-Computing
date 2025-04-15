"""
This module implements the AStarExplorer class that solves the maze
using an A* search algorithm with Manhattan distance as the heuristic.
"""

import time
from heapq import heappop, heappush
from typing import List, Tuple

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class AStarExplorer:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.path: List[Tuple[int, int]] = []
        self.backtracks = 0  # Not applicable for A*

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        open_set = []
        heappush(open_set, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: manhattan_distance(self.start, self.end)}

        while open_set:
            current = heappop(open_set)[1]
            if current == self.end:
                break
            x, y = current
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (x + dx, y + dy)
                if (0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height and
                    self.maze.grid[neighbor[1]][neighbor[0]] == 0):
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + manhattan_distance(neighbor, self.end)
                        heappush(open_set, (f_score[neighbor], neighbor))

        if self.end in came_from or self.start == self.end:
            current = self.end
            path = []
            while current is not None:
                path.append(current)
                current = came_from.get(current)
            path.reverse()
            self.path = path
        else:
            self.path = []
        end_time = time.time()
        time_taken = end_time - start_time
        return time_taken, self.path
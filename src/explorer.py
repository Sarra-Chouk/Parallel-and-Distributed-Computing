"""
Maze Explorer module that implements automated maze solving.
"""

import time
import pygame
import heapq
from typing import Tuple, List, Optional, Deque
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)  # Keep track of last 3 moves
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0  # Count number of backtrack operations
        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def heuristic(self, a, b):
        """Calculate the Manhattan distance between two points"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self):
        """A* pathfinding algorithm implementation"""
        frontier = []
        heapq.heappush(frontier, (0, self.maze.start_pos))
        came_from = {self.maze.start_pos: None}
        cost_so_far = {self.maze.start_pos: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == self.maze.end_pos:
                break
                
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] < self.maze.width and 
                    0 <= next_pos[1] < self.maze.height and 
                    self.maze.grid[next_pos[1]][next_pos[0]] == 0):
                    
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + self.heuristic(self.maze.end_pos, next_pos)
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current
        
        # Reconstruct path
        current = self.maze.end_pos
        path = []
        while current != self.maze.start_pos:
            path.append(current)
            current = came_from[current]
        path.append(self.maze.start_pos)
        path.reverse()
        
        return path

    def optimize_path(self, path):
        """Remove unnecessary turns from the path"""
        if len(path) < 3:
            return path
            
        optimized = [path[0]]
        i = 0
        
        while i < len(path) - 1:
            j = len(path) - 1
            while j > i:
                if self.is_straight_line_possible(path[i], path[j]):
                    optimized.append(path[j])
                    i = j
                    break
                j -= 1
            else:
                optimized.append(path[i+1])
                i += 1
                
        return optimized

    def is_straight_line_possible(self, start, end):
        """Check if we can move directly from start to end without walls"""
        x0, y0 = start
        x1, y1 = end
        
        # Vertical line
        if x0 == x1:
            step = 1 if y1 > y0 else -1
            for y in range(y0, y1, step):
                if self.maze.grid[y][x0] == 1:
                    return False
            return True
        
        # Horizontal line
        if y0 == y1:
            step = 1 if x1 > x0 else -1
            for x in range(x0, x1, step):
                if self.maze.grid[y0][x] == 1:
                    return False
            return True
        
        return False

    def turn_right(self):
        """Turn 90 degrees to the right."""
        x, y = self.direction
        self.direction = (-y, x)

    def turn_left(self):
        """Turn 90 degrees to the left."""
        x, y = self.direction
        self.direction = (y, -x)

    def can_move_forward(self) -> bool:
        """Check if we can move forward in the current direction."""
        dx, dy = self.direction
        new_x, new_y = self.x + dx, self.y + dy
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0)

    def move_forward(self):
        """Move forward in the current direction."""
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        current_move = (self.x, self.y)
        self.moves.append(current_move)
        self.move_history.append(current_move)
        if self.visualize:
            self.draw_state()

    def is_stuck(self) -> bool:
        """Check if the explorer is stuck in a loop."""
        if len(self.move_history) < 3:
            return False
        return (self.move_history[0] == self.move_history[1] == self.move_history[2])

    def backtrack(self) -> bool:
        """Backtrack to the last position where we had multiple choices."""
        if not self.backtrack_path:
            self.backtrack_path = self.find_backtrack_path()
        
        if self.backtrack_path:
            next_pos = self.backtrack_path.pop()
            self.x, self.y = next_pos
            self.backtrack_count += 1
            if self.visualize:
                self.draw_state()
            return True
        return False

    def find_backtrack_path(self) -> List[Tuple[int, int]]:
        """Find a path back to a position with multiple choices."""
        path = []
        current_pos = (self.x, self.y)
        visited = set()
        
        for i in range(len(self.moves) - 1, -1, -1):
            pos = self.moves[i]
            if pos in visited:
                continue
            visited.add(pos)
            path.append(pos)
            
            choices = self.count_available_choices(pos)
            if choices > 1:
                return path[::-1]
        
        return path[::-1]

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Count the number of available moves from a position."""
        x, y = pos
        choices = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0):
                choices += 1
        return choices

    def draw_state(self):
        """Draw the current state of the maze and explorer."""
        self.screen.fill(WHITE)
        
        # Draw maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                   (x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points
        pygame.draw.rect(self.screen, (0, 255, 0),
                        (self.maze.start_pos[0] * CELL_SIZE,
                         self.maze.start_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (self.maze.end_pos[0] * CELL_SIZE,
                         self.maze.end_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw explorer
        pygame.draw.rect(self.screen, BLUE,
                        (self.x * CELL_SIZE, self.y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        """Print detailed statistics about the exploration."""
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """Solve the maze using the most appropriate algorithm."""
        self.start_time = time.time()
        
        if isinstance(self.maze, StaticMaze):
            # Use A* for static maze
            path = self.a_star_search()
            optimized_path = self.optimize_path(path)
            self.moves = optimized_path.copy()
            self.x, self.y = self.maze.end_pos
            
            if self.visualize:
                for pos in optimized_path:
                    self.x, self.y = pos
                    self.draw_state()
        else:
            # Use right-hand rule for random mazes
            visited = set()
            visited.add((self.x, self.y))
            
            if self.visualize:
                self.draw_state()
            
            while (self.x, self.y) != self.maze.end_pos:
                if self.is_stuck():
                    if not self.backtrack():
                        self.turn_left()
                        self.turn_left()
                        self.move_forward()
                    self.backtracking = True
                else:
                    self.backtracking = False
                    self.turn_right()
                    if self.can_move_forward():
                        self.move_forward()
                        visited.add((self.x, self.y))
                    else:
                        self.turn_left()
                        if self.can_move_forward():
                            self.move_forward()
                            visited.add((self.x, self.y))
                        else:
                            self.turn_left()
                            if self.can_move_forward():
                                self.move_forward()
                                visited.add((self.x, self.y))
                            else:
                                self.turn_left()
                                self.move_forward()
                                visited.add((self.x, self.y))

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()
        
        self.print_statistics(time_taken)
        return time_taken, self.moves
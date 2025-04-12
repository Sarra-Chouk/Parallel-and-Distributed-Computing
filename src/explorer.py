"""
Maze Explorer module that implements automated maze solving with heuristic-based move selection.
"""

import time
import pygame
from typing import Tuple, List
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

    def get_valid_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Return a list of tuples: (direction, (new_x, new_y)) for each valid move.
        Directions considered: right, down, left, up.
        """
        valid_moves = []
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            dx, dy = d
            new_x, new_y = self.x + dx, self.y + dy
            if (0 <= new_x < self.maze.width and
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0):
                valid_moves.append((d, (new_x, new_y)))
        return valid_moves

    def is_stuck(self) -> bool:
        """Check if the explorer is stuck in a loop."""
        if len(self.move_history) < 3:
            return False
        return (self.move_history[0] == self.move_history[1] == self.move_history[2])

    def backtrack(self) -> bool:
        """Backtrack to the last position where we had multiple movement choices."""
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
        """Find a path back to a position with multiple available moves."""
        path = []
        visited = set()
        for i in range(len(self.moves) - 1, -1, -1):
            pos = self.moves[i]
            if pos in visited:
                continue
            visited.add(pos)
            path.append(pos)
            if self.count_available_choices(pos) > 1:
                return path[::-1]
        return path[::-1]

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Count how many moves are available from a given position."""
        x, y = pos
        choices = 0
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + d[0], y + d[1]
            if (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0):
                choices += 1
        return choices

    def draw_state(self):
        """Render the current state of the maze, start/end points, and explorer."""
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE, self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE, self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        if time_taken > 0:
            print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using a heuristic-based move selection.
        At each step, gather all valid moves, compute the Manhattan distance from each candidate move
        to the exit, and select the move that minimizes that distance.
        Falls back to backtracking if no valid moves are available.
        """
        self.start_time = time.time()
        # Loop until the explorer reaches the exit.
        while (self.x, self.y) != self.maze.end_pos:
            if self.is_stuck():
                if not self.backtrack():
                    self.turn_left()
                    self.turn_left()  # Turn around
                    self.move_forward()
            else:
                valid_moves = self.get_valid_moves()
                if valid_moves:
                    exit_x, exit_y = self.maze.end_pos
                    # For each valid move, compute the Manhattan distance from the candidate position to the exit.
                    best_move, best_pos = min(valid_moves, key=lambda mv: abs(mv[1][0] - exit_x) + abs(mv[1][1] - exit_y))
                    self.direction = best_move
                    self.move_forward()
                else:
                    # No valid moves, so fall back to backtracking.
                    if not self.backtrack():
                        self.turn_left()
                        self.turn_left()
                        self.move_forward()
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        self.print_statistics(time_taken)
        return time_taken, self.moves
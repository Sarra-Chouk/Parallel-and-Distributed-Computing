"""
Enhanced Maze Explorer module that implements automated maze solving with 
heuristic-based adaptive move selection and targeted backtracking.
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
        self.direction = (1, 0)  # Initial direction: right
        self.moves = []          # List of moves (cells) visited
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.backtracking = False
        self.backtrack_path = []  # Stores positions for backtracking
        self.backtrack_count = 0  # Count of backtracking operations
        
        # Use a deque to record a short history (for potential alternate checks)
        self.move_history = deque(maxlen=5)
        
        # Global visited count dictionary for loop and dead-end detection
        self.visited_count = {}
        self._update_visited((self.x, self.y))
        
        # Threshold for early abandonment (if path becomes excessively long)
        self.max_path_length = 200  # (This number can be adjusted experimentally)
        
        # Failsafe iteration counter to prevent infinite loops
        self.iteration_counter = 0
        self.MAX_ITERATIONS = 10000  # Adjust according to expected maze complexity
        
        # Only initialize pygame if visualization is enabled
        if self.visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving (Enhanced)")
            self.clock = pygame.time.Clock()

    def _update_visited(self, pos: Tuple[int, int]):
        """Record a visit to a cell."""
        self.visited_count[pos] = self.visited_count.get(pos, 0) + 1

    def manhattan_distance(self, pos: Tuple[int, int]) -> int:
        """Compute Manhattan distance from pos to exit."""
        ex, ey = self.maze.end_pos
        x, y = pos
        return abs(ex - x) + abs(ey - y)

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Count the number of valid moves from a given cell."""
        x, y = pos
        choices = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.maze.width and
                0 <= new_y < self.maze.height and
                self.maze.grid[new_y][new_x] == 0):
                choices += 1
        return choices

    def score_move(self, new_x: int, new_y: int) -> int:
        """
        Score a potential move using Manhattan distance and available choices.
        Lower score indicates a more promising move.
        """
        distance = self.manhattan_distance((new_x, new_y))
        # More available choices should slightly lower the score (encourage junctions)
        choices = self.count_available_choices((new_x, new_y))
        score = distance - choices
        return score

    def is_valid_move(self, new_x: int, new_y: int) -> bool:
        """Check if moving to (new_x, new_y) is within bounds and not a wall."""
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0)

    def get_new_direction(self, turn: str) -> Tuple[int, int]:
        """
        Given a relative turn command ('right', 'forward', 'left', 'back'),
        compute the new direction vector.
        """
        dx, dy = self.direction
        if turn == "right":
            # Rotate 90 degrees clockwise
            return (-dy, dx)
        elif turn == "left":
            # Rotate 90 degrees counter-clockwise
            return (dy, -dx)
        elif turn == "back":
            # Reverse direction (180-degree turn)
            return (-dx, -dy)
        elif turn == "forward":
            # No change in direction
            return (dx, dy)
        else:
            return (dx, dy)

    def move_forward(self):
        """Move forward in the current direction and update state."""
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        current_move = (self.x, self.y)
        self.moves.append(current_move)
        self.move_history.append(current_move)
        self._update_visited(current_move)
        if self.visualize:
            self.draw_state()

    def draw_state(self):
        """Draw the current state of the maze and explorer."""
        self.screen.fill(WHITE)
        # Draw maze walls
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
        # Draw start and exit points
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        # Draw explorer (current position)
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        """Print detailed statistics for the exploration."""
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves) / time_taken:.2f}")
        print("==================================\n")

    def find_backtrack_path(self) -> List[Tuple[int, int]]:
        """Find a backtrack path by scanning through moves for a junction."""
        path = []
        visited = set()
        # Iterate backwards over the moves to find a junction with multiple choices.
        for pos in reversed(self.moves):
            if pos in visited:
                continue
            visited.add(pos)
            path.append(pos)
            if self.count_available_choices(pos) > 1:
                return path[::-1]  # Return the reversed path
        return path[::-1]

    def backtrack(self) -> bool:
        """Backtrack using a targeted strategy to a promising junction."""
        if not self.backtrack_path:
            # Find a backtracking path from the move history.
            self.backtrack_path = self.find_backtrack_path()
        if self.backtrack_path:
            next_pos = self.backtrack_path.pop(0)
            self.x, self.y = next_pos
            self.backtrack_count += 1
            if self.visualize:
                self.draw_state()
            return True
        return False

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using an enhanced right-hand rule algorithm that includes:
          - Heuristic-based adaptive move selection
          - Global visited count for loop and dead-end detection
          - Targeted backtracking and early abandonment
        Returns the time taken and the list of moves made.
        """
        self.start_time = time.time()
        if self.visualize:
            self.draw_state()
            
        # Continue until exit is reached or the iteration limit is exceeded
        while (self.x, self.y) != self.maze.end_pos:
            self.iteration_counter += 1
            if self.iteration_counter > self.MAX_ITERATIONS:
                print("Exceeded maximum iterations without finding the exit.")
                break

            # Early abandonment: if path becomes too long, force backtracking.
            if len(self.moves) >= self.max_path_length:
                if not self.backtrack():
                    # If backtracking fails, simply reverse direction.
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()
                continue

            # Build candidate moves from relative directions
            candidates = []
            for rel_turn in ["right", "forward", "left", "back"]:
                new_direction = self.get_new_direction(rel_turn)
                new_x = self.x + new_direction[0]
                new_y = self.y + new_direction[1]
                if self.is_valid_move(new_x, new_y):
                    # Only consider cells that have not been over-visited.
                    visits = self.visited_count.get((new_x, new_y), 0)
                    if visits < 3:  # Arbitrary limit; adjust based on experiments.
                        score = self.score_move(new_x, new_y)
                        candidates.append((score, rel_turn, new_direction, (new_x, new_y)))
            
            if candidates:
                # Choose the candidate move with the lowest score.
                candidates.sort(key=lambda x: x[0])
                best = candidates[0]
                # Set the new direction from the chosen candidate.
                self.direction = best[2]
                self.move_forward()
            else:
                # No candidate moves found; trigger targeted backtracking.
                if not self.backtrack():
                    # If backtracking fails, perform a turnaround move.
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()
                self.backtracking = True

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()
        self.print_statistics(time_taken)
        return time_taken, self.moves
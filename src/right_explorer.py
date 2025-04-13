"""
Enhanced Maze Explorer module using a heuristic–driven right-hand rule.

Improvements over the original right-hand explorer:
 • Instead of a fixed turn order, candidate moves are evaluated using a scoring function.
   The score is computed using the Manhattan distance from the candidate cell to the exit,
   with an additional bonus for available choices (favoring junctions).
 • When no promising candidate move exists, targeted backtracking is used to revert to a previous junction.
 • An early-abandonment threshold limits runaway paths.
"""

import time
import pygame
from typing import Tuple, List
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class EnhancedExplorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []          # List of all moves taken
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        # Record a history of moves (used in case we need to backtrack)
        self.move_history = deque(maxlen=5)
        # Record how many times a cell has been visited (to avoid cycles)
        self.visited_count = {}
        self._update_visited((self.x, self.y))
        # For targeted backtracking
        self.backtrack_path = []
        self.backtrack_count = 0
        # Limit the overall path length to force early reconsideration of choices.
        self.max_path_length = 300
        
        if self.visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Enhanced Maze Explorer")
            self.clock = pygame.time.Clock()

    def _update_visited(self, pos: Tuple[int, int]):
        self.visited_count[pos] = self.visited_count.get(pos, 0) + 1

    def manhattan_distance(self, pos: Tuple[int, int]) -> int:
        """Compute Manhattan distance from pos to the maze exit."""
        ex, ey = self.maze.end_pos
        x, y = pos
        return abs(ex - x) + abs(ey - y)

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        """Return the number of valid moves from a given cell."""
        x, y = pos
        choices = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if self.maze.grid[ny][nx] == 0:
                    choices += 1
        return choices

    def is_valid_move(self, x: int, y: int) -> bool:
        """Return True if (x,y) is within bounds and not a wall."""
        return (0 <= x < self.maze.width and 0 <= y < self.maze.height and 
                self.maze.grid[y][x] == 0)

    def get_new_direction(self, rel_turn: str) -> Tuple[int, int]:
        """
        Given a relative turn ("right", "forward", "left", "back"),
        compute the new direction vector.
        """
        dx, dy = self.direction
        if rel_turn == "right":
            return (-dy, dx)
        elif rel_turn == "left":
            return (dy, -dx)
        elif rel_turn == "back":
            return (-dx, -dy)
        elif rel_turn == "forward":
            return (dx, dy)
        else:
            return (dx, dy)

    def get_candidate_moves(self) -> List[Tuple[float, str, Tuple[int, int], Tuple[int, int]]]:
        """
        Evaluate moves in four relative directions.
        Returns a list of tuples (score, rel_turn, new_direction, new_position).
        Lower score indicates a more promising move.
        The score is computed as:
            score = ManhattanDistance - (0.5 * available_choices)
        """
        candidates = []
        for rel_turn in ["right", "forward", "left", "back"]:
            new_direction = self.get_new_direction(rel_turn)
            new_x = self.x + new_direction[0]
            new_y = self.y + new_direction[1]
            if self.is_valid_move(new_x, new_y):
                # Basic score based on Manhattan distance to goal
                score = self.manhattan_distance((new_x, new_y))
                # Reward positions that have more available choices (junctions)
                choices = self.count_available_choices((new_x, new_y))
                score -= choices * 0.5  # The weight is tunable
                candidates.append((score, rel_turn, new_direction, (new_x, new_y)))
        return candidates

    def move_forward(self):
        """Advance one step in the current direction and update internal state."""
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        new_pos = (self.x, self.y)
        self.moves.append(new_pos)
        self.move_history.append(new_pos)
        self._update_visited(new_pos)
        if self.visualize:
            self.draw_state()

    def draw_state(self):
        """Draw the maze, start/goal and the explorer's current position."""
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw the start (green) and goal (red) points.
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw the explorer (blue).
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def find_backtrack_path(self) -> List[Tuple[int, int]]:
        """
        Look backwards through the move history to find a cell with
        more than one available move (a junction), and return a path
        from the current position back to that junction.
        """
        path = []
        seen = set()
        for pos in reversed(self.moves):
            if pos in seen:
                continue
            seen.add(pos)
            path.append(pos)
            if self.count_available_choices(pos) > 1:
                return path[::-1]  # reverse the collected path
        return path[::-1]

    def backtrack(self) -> bool:
        """
        Revert the explorer's position along a target backtrack path.
        Increases the backtrack counter.
        Returns True if backtracking was successfully performed.
        """
        if not self.backtrack_path:
            self.backtrack_path = self.find_backtrack_path()
        if self.backtrack_path:
            next_pos = self.backtrack_path.pop(0)
            self.x, self.y = next_pos
            self.backtrack_count += 1
            if self.visualize:
                self.draw_state()
            return True
        return False

    def print_statistics(self, time_taken: float):
        """Print evaluation metrics for the exploration."""
        print("\n=== Enhanced Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("============================================\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using an enhanced right-hand rule algorithm.
        The explorer chooses moves by evaluating candidate directions
        with a heuristic score. When stuck or when the path exceeds a threshold,
        targeted backtracking is used.
        Returns a tuple (time_taken, moves) where moves is the list of visited cells.
        """
        self.start_time = time.time()
        while (self.x, self.y) != self.maze.end_pos:
            # Early abandonment to prevent excessively long paths.
            if len(self.moves) > self.max_path_length:
                if not self.backtrack():
                    # If backtracking fails, force a turnaround.
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()
                continue

            candidates = self.get_candidate_moves()
            if candidates:
                # Choose the candidate with the lowest score.
                candidates.sort(key=lambda item: item[0])
                best_candidate = candidates[0]
                # Update current direction and move forward.
                self.direction = best_candidate[2]
                self.move_forward()
            else:
                # No valid candidate moves found; trigger backtracking.
                if not self.backtrack():
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()

        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()
        self.print_statistics(total_time)
        return total_time, self.moves
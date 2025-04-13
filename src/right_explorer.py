"""
Enhanced Maze Explorer module using a heuristic–driven right-hand rule.

Improvements over the original right-hand explorer:
 • Instead of a fixed turn order, candidate moves are evaluated using a scoring function.
   The score is computed using the Manhattan distance from the candidate cell to the exit,
   with an additional bonus for available choices (favoring junctions).
 • When no promising candidate move exists, targeted backtracking is used to revert to a previous junction.
 • An early-abandonment threshold limits runaway paths.
 
This headless version has all visualization code removed.
"""

import time
from typing import Tuple, List
from collections import deque

class EnhancedExplorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []          # List of all moves taken
        self.start_time = None
        self.end_time = None
        # Even though a 'visualize' flag exists, it will be ignored in this headless version.
        self.visualize = False
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
                score = self.manhattan_distance((new_x, new_y))
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
        iteration = 0
        max_iterations = 100000  # Failsafe to prevent an infinite loop.
        while (self.x, self.y) != self.maze.end_pos and iteration < max_iterations:
            iteration += 1
            # Early abandonment to prevent excessively long paths.
            if len(self.moves) > self.max_path_length:
                if not self.backtrack():
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()
                continue

            candidates = self.get_candidate_moves()
            if candidates:
                # Choose the candidate with the lowest score.
                candidates.sort(key=lambda item: item[0])
                best_candidate = candidates[0]
                self.direction = best_candidate[2]
                self.move_forward()
            else:
                if not self.backtrack():
                    self.direction = (-self.direction[0], -self.direction[1])
                    self.move_forward()

        if iteration >= max_iterations:
            print("Exceeded maximum iterations without finding the exit.")
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        self.print_statistics(total_time)
        return total_time, self.moves
"""
Enhanced Maze Explorer module using a heuristic–driven right-hand rule with improvements:

1. Incorporates a penalty for revisited cells.
2. Stores a more informed history at junctions.
3. Uses dynamic thresholds to trigger backtracking.
4. Returns more detailed junction information to guide backtracking.

This version runs completely headless.
"""

import time
from typing import Tuple, List, Dict
from collections import deque

class EnhancedExplorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []          # List of visited cells along the current path
        self.start_time = None
        self.end_time = None
        self.visualize = False  # Visualization disabled
        self.move_history = deque(maxlen=5)
        self.visited_count = {}
        self._update_visited((self.x, self.y))
        # For storing informed junction info (keyed by cell coordinate)
        self.junction_info: Dict[Tuple[int, int], List[Tuple[float, str, Tuple[int, int], Tuple[int, int]]]] = {}
        # For targeted backtracking history (list of junction positions)
        self.junction_history = []
        self.backtrack_count = 0
        # Instead of a fixed max_path_length, we use a dynamic threshold:
        # current_estimate = steps_so_far + ManhattanDistance. We track the best (lowest) estimate.
        self.best_estimate = float('inf')
        self.threshold_factor = 1.5  # If current estimate exceeds best_estimate*factor, trigger backtracking.
        # Failsafe iteration counter
        self.iteration_counter = 0
        self.max_iterations = 100000

        # Adjustable weights:
        self.choice_bonus = 1.0   # bonus per available choice (higher => more attraction to junctions)
        self.visit_penalty = 1.0  # penalty per revisit

    def _update_visited(self, pos: Tuple[int, int]):
        self.visited_count[pos] = self.visited_count.get(pos, 0) + 1

    def manhattan_distance(self, pos: Tuple[int, int]) -> int:
        ex, ey = self.maze.end_pos
        x, y = pos
        return abs(ex - x) + abs(ey - y)

    def count_available_choices(self, pos: Tuple[int, int]) -> int:
        x, y = pos
        choices = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                if self.maze.grid[ny][nx] == 0:
                    choices += 1
        return choices

    def is_valid_move(self, x: int, y: int) -> bool:
        return (0 <= x < self.maze.width and 0 <= y < self.maze.height and 
                self.maze.grid[y][x] == 0)

    def get_new_direction(self, rel_turn: str) -> Tuple[int, int]:
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
        Returns a list of tuples: (score, rel_turn, new_direction, new_position).
        Lower score indicates a more promising move.
        Score = ManhattanDistance - (choice_bonus * available_choices) + (visit_penalty * visited_count)
        """
        candidates = []
        for rel_turn in ["right", "forward", "left", "back"]:
            new_direction = self.get_new_direction(rel_turn)
            new_x = self.x + new_direction[0]
            new_y = self.y + new_direction[1]
            if self.is_valid_move(new_x, new_y):
                base = self.manhattan_distance((new_x, new_y))
                choices = self.count_available_choices((new_x, new_y))
                visits = self.visited_count.get((new_x, new_y), 0)
                score = base - (self.choice_bonus * choices) + (self.visit_penalty * visits)
                candidates.append((score, rel_turn, new_direction, (new_x, new_y)))
                # If the candidate cell is a junction, store detailed info.
                if choices > 1:
                    self.junction_info.setdefault((new_x, new_y), []).append(
                        (score, rel_turn, new_direction, (new_x, new_y))
                    )
        return candidates

    def move_forward(self):
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        new_pos = (self.x, self.y)
        self.moves.append(new_pos)
        self.move_history.append(new_pos)
        self._update_visited(new_pos)
        # Update junction history: if new_pos is a junction, store it.
        if self.count_available_choices(new_pos) > 1:
            self.junction_history.append(new_pos)

    def dynamic_threshold_trigger(self) -> bool:
        """
        Computes a cost estimate (steps so far + Manhattan distance).
        Updates self.best_estimate. If the current estimate is considerably
        worse than best_estimate (multiplied by threshold_factor), return True.
        """
        current_estimate = len(self.moves) + self.manhattan_distance((self.x, self.y))
        if current_estimate < self.best_estimate:
            self.best_estimate = current_estimate
        # If current estimate is more than threshold_factor times the best seen, trigger backtracking.
        return current_estimate > self.best_estimate * self.threshold_factor

    def informed_backtrack(self) -> bool:
        """
        Use the stored junction_history to backtrack to a junction that
        still has some unexplored candidate moves.
        Returns True if a backtracking jump is made.
        """
        # Walk through stored junctions from latest to earliest.
        while self.junction_history:
            junc = self.junction_history.pop()
            # Retrieve the stored candidate moves at this junction, if any.
            if junc in self.junction_info and self.junction_info[junc]:
                # Choose the candidate with best score among those not yet chosen.
                # Note: you can refine this decision further.
                candidate_list = self.junction_info[junc]
                candidate_list.sort(key=lambda item: item[0])
                best_candidate = candidate_list[0]
                # Jump to that junction.
                self.x, self.y = junc
                self.backtrack_count += 1
                # Remove used candidate.
                candidate_list.pop(0)
                return True
        return False

    def backtrack(self) -> bool:
        """
        Simple backtracking fallback: if no junction in the informed history is found,
        revert one step (if available).
        """
        if self.moves:
            # Remove the last move (simulate stepping back).
            last = self.moves.pop()
            self.backtrack_count += 1
            if self.moves:
                self.x, self.y = self.moves[-1]
            else:
                # If no moves remain, reset to start.
                self.x, self.y = self.maze.start_pos
            return True
        return False

    def print_statistics(self, time_taken: float):
        print("\n=== Enhanced Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("============================================\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        self.start_time = time.time()
        self.best_estimate = len(self.moves) + self.manhattan_distance((self.x, self.y))
        while (self.x, self.y) != self.maze.end_pos and self.iteration_counter < self.max_iterations:
            self.iteration_counter += 1

            # If dynamic threshold says we're on a high-cost branch, try informed backtracking.
            if self.dynamic_threshold_trigger():
                if not self.informed_backtrack():
                    self.backtrack()
                continue

            candidates = self.get_candidate_moves()
            if candidates:
                # Choose the candidate with the lowest score.
                candidates.sort(key=lambda item: item[0])
                best_candidate = candidates[0]
                self.direction = best_candidate[2]
                self.move_forward()
            else:
                if not self.informed_backtrack():
                    self.backtrack()

        if self.iteration_counter >= self.max_iterations:
            print("Exceeded maximum iterations without finding the exit.")
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        self.print_statistics(total_time)
        return total_time, self.moves
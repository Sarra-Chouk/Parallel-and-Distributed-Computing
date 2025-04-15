import time
import random
import numpy as np
from typing import List, Tuple

class RLExplorer:
    def __init__(self, maze, episodes=500, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.maze = maze
        self.start = maze.start_pos
        self.end = maze.end_pos
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.episodes = episodes
        self.q_table = {}       # Q-values for state-action pairs
        self.path: List[Tuple[int, int]] = []
        self.backtracks = 0     # Optional tracking

    def get_actions(self, pos):
        """Get valid actions (directions) from a position."""
        x, y = pos
        directions = {
            'up': (x, y - 1),
            'down': (x, y + 1),
            'left': (x - 1, y),
            'right': (x + 1, y)
        }
        valid_actions = {}
        for action, (nx, ny) in directions.items():
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and self.maze.grid[ny][nx] == 0:
                valid_actions[action] = (nx, ny)
        return valid_actions

    def choose_action(self, state, actions):
        """Choose an action using epsilon-greedy strategy."""
        if random.random() < self.epsilon:
            return random.choice(list(actions.keys()))
        q_values = [self.q_table.get((state, a), 0) for a in actions]
        max_q = max(q_values)
        best_actions = [a for a in actions if self.q_table.get((state, a), 0) == max_q]
        return random.choice(best_actions)

    def train(self):
        for _ in range(self.episodes):
            state = self.start
            while state != self.end:
                actions = self.get_actions(state)
                if not actions:
                    break
                action = self.choose_action(state, actions)
                next_state = actions[action]
                reward = 100 if next_state == self.end else -1
                old_q = self.q_table.get((state, action), 0)
                next_max_q = max([self.q_table.get((next_state, a), 0) for a in self.get_actions(next_state)], default=0)
                new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
                self.q_table[(state, action)] = new_q
                state = next_state

    def extract_path(self):
        """Follow greedy policy after training to extract path."""
        self.path = []
        state = self.start
        visited = set()
        while state != self.end and state not in visited:
            visited.add(state)
            self.path.append(state)
            actions = self.get_actions(state)
            if not actions:
                break
            best_action = max(actions, key=lambda a: self.q_table.get((state, a), -float('inf')))
            state = actions[best_action]
        self.path.append(self.end)

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        start_time = time.time()
        self.train()
        self.extract_path()
        time_taken = time.time() - start_time
        return time_taken, self.path
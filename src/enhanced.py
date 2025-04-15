"""
MPI-based Distributed Maze Explorer module.
This module defines classes and functions for distributed maze exploration using MPI.
Each worker process (nonzero rank) acts as an explorer agent.
The master (rank 0) coordinates task assignment and global termination.
"""

from collections import deque
from typing import Tuple, List, Set, Optional
from mpi4py import MPI

class ExplorerAgent:
    def __init__(self, maze, start_position: Tuple[int, int]):
        self.maze = maze
        self.x, self.y = start_position
        self.moves: List[Tuple[int, int]] = [start_position]
        self.direction = (1, 0)  # Start facing right
        self.local_visited: Set[Tuple[int, int]] = {start_position}
        self.move_history = deque(maxlen=3)
        self.backtrack_count = 0
        # Assignment task details
        self.target: Optional[Tuple[int, int]] = None
        self.current_path: List[Tuple[int, int]] = []
    
    def current_position(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def turn_right(self):
        dx, dy = self.direction
        self.direction = (-dy, dx)
    
    def turn_left(self):
        dx, dy = self.direction
        self.direction = (dy, -dx)
    
    def can_move_forward(self) -> bool:
        dx, dy = self.direction
        new_x = self.x + dx
        new_y = self.y + dy
        return (0 <= new_x < self.maze.width and
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0)
    
    def move_forward(self):
        dx, dy = self.direction
        self.x += dx
        self.y += dy
        pos = (self.x, self.y)
        self.moves.append(pos)
        self.local_visited.add(pos)
        self.move_history.append(pos)
    
    def compute_path(self, target: Tuple[int, int]) -> List[Tuple[int, int]]:
        # Simple BFS to compute a path from the current position to the target.
        from collections import deque
        start = self.current_position()
        if start == target:
            return []
        q = deque()
        q.append((start, []))
        visited = {start}
        while q:
            current, path = q.popleft()
            x, y = current
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and self.maze.grid[ny][nx] == 0:
                    if next_pos not in visited:
                        visited.add(next_pos)
                        new_path = path + [next_pos]
                        if next_pos == target:
                            return new_path
                        q.append((next_pos, new_path))
        return []
    
    def get_junction_frontiers(self, global_visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        When at a junction (three or more available moves), return adjacent open cells
        that have not yet been visited.
        """
        frontiers = []
        available = 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and self.maze.grid[ny][nx] == 0:
                available += 1
                candidate = (nx, ny)
                if candidate not in global_visited:
                    frontiers.append(candidate)
        if available >= 3:
            return frontiers
        return []
    
    def step(self):
        """
        Perform one move:
          - If a target is assigned and a computed path exists, follow that path.
          - Otherwise, use the right-hand rule.
        """
        if self.target is not None and self.current_path:
            next_cell = self.current_path.pop(0)
            self.x, self.y = next_cell
            self.moves.append(next_cell)
            self.local_visited.add(next_cell)
            self.move_history.append(next_cell)
            # If reached target, clear assignment.
            if next_cell == self.target:
                self.target = None
                self.current_path = []
        else:
            self.turn_right()
            if self.can_move_forward():
                self.move_forward()
            else:
                self.turn_left()  # Undo right turn.
                if self.can_move_forward():
                    self.move_forward()
                else:
                    self.turn_left()
                    if self.can_move_forward():
                        self.move_forward()
                    else:
                        self.turn_left()
                        self.move_forward()
    
    def to_message(self):
        """
        Package the agent's state into a dictionary for communication.
        """
        return {
            'rank': MPI.COMM_WORLD.Get_rank(),
            'pos': self.current_position(),
            'frontiers': list(self.get_junction_frontiers(self.local_visited)),
            'moves': self.moves,
        }


class TaskCoordinatorMPI:
    """
    Coordinator that runs on rank 0.
    It collects update messages from worker processes, aggregates a global visited set and frontier list,
    and assigns tasks (frontier targets) to workers based on Manhattan distance to the exit.
    """
    def __init__(self, maze, num_workers: int):
        self.maze = maze
        self.num_workers = num_workers
        self.global_visited: Set[Tuple[int, int]] = set()
        self.frontier: Set[Tuple[int, int]] = set()
        self.exit = maze.end_pos
        self.comm = MPI.COMM_WORLD

    def assign_tasks(self):
        """
        If any frontier candidates exist, assign them to workers.
        (Here we simply select the frontier with the smallest Manhattan distance to the exit.)
        """
        if not self.frontier:
            return
        # For every worker (assumed to be always waiting for messages), assign one task.
        for worker in range(1, self.num_workers + 1):
            if self.frontier:
                best = min(self.frontier, key=lambda p: abs(p[0] - self.exit[0]) + abs(p[1] - self.exit[1]))
                self.frontier.remove(best)
                # Send the assignment to the worker.
                self.comm.send({'type': 'assignment', 'target': best}, dest=worker, tag=11)

    def run(self):
        """
        Main loop for the coordinator.
        Continuously receives update messages from workers and processes them.
        Terminates when any worker reports that it has reached the maze exit.
        """
        terminated = False
        winning_agent_moves = None
        while not terminated:
            status = MPI.Status()
            msg = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            sender = status.Get_source()
            # Process termination message.
            if msg.get('type') == 'terminate':
                terminated = True
                winning_agent_moves = msg.get('moves')
                # Broadcast termination to all workers.
                for r in range(1, self.num_workers + 1):
                    self.comm.send({'type': 'terminate'}, dest=r, tag=99)
                break
            # Process update message.
            elif msg.get('type') == 'update':
                pos = msg.get('pos')
                frontiers = msg.get('frontiers', [])
                self.global_visited.add(pos)
                for f in frontiers:
                    if f not in self.global_visited:
                        self.frontier.add(f)
                # After processing, assign tasks if available.
                self.assign_tasks()
        return winning_agent_moves


def worker_loop(maze):
    """
    Loop for a worker process (nonzero MPI rank).
    The explorer agent repeatedly performs a step, checks for assignment messages,
    and sends update messages to the coordinator.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    agent = ExplorerAgent(maze, maze.start_pos)
    exit_pos = maze.end_pos
    terminated = False
    while not terminated:
        # Check for messages from the coordinator.
        flag = comm.Iprobe(source=0, tag=MPI.ANY_TAG)
        if flag:
            msg = comm.recv(source=0, tag=MPI.ANY_TAG)
            if msg.get('type') == 'assignment':
                agent.target = msg.get('target')
                agent.current_path = agent.compute_path(agent.target)
            elif msg.get('type') == 'terminate':
                terminated = True
                break
        # Perform a step.
        agent.step()
        # If reached exit, send a termination message.
        if agent.current_position() == exit_pos:
            comm.send({'type': 'terminate', 'rank': rank, 'moves': agent.moves}, dest=0, tag=10)
            terminated = True
            break
        # Send an update message.
        update_msg = agent.to_message()
        update_msg['type'] = 'update'
        comm.send(update_msg, dest=0, tag=10)
    return agent.moves
"""
MPI-based main program for distributed maze exploration.
Usage example:
    mpiexec -n 4 python main_enhanced.py --type static --width 50 --height 50
Rank 0 acts as the coordinator; other ranks act as explorer agents.
"""

import argparse
from mpi4py import MPI
from src.maze import create_maze  # Assumes your maze module provides create_maze()
from right_enhanced import TaskCoordinatorMPI, worker_loop

def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description="MPI Distributed Maze Explorer")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (default: random)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (ignored for static mazes)")
    args = parser.parse_args()
    
    # Create the maze (the same maze is used by all processes).
    maze = create_maze(args.width, args.height, args.type)
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if rank == 0:
        # Rank 0 is the coordinator.
        # The number of worker agents is (size - 1).
        coordinator = TaskCoordinatorMPI(maze, num_workers=size - 1)
        winning_moves = coordinator.run()
        print("\n=== MPI Distributed Maze Exploration Completed ===")
        print(f"Winning agent's total moves: {len(winning_moves) if winning_moves else 'N/A'}")
    else:
        # Worker processes run the explorer loop.
        final_moves = worker_loop(maze)
        # Optionally, each worker could report its move count here.
        # For example: print(f"Worker {rank} finished with {len(final_moves)} moves.")

if __name__ == "__main__":
    main()
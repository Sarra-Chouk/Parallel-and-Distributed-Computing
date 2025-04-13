from mpi4py import MPI
import argparse
from src.maze import create_maze
from src.bfs_explorer import BFSSolver

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MPI Maze Solver using BFS")
parser.add_argument("--type", choices=["random", "static"], default="random",
                    help="Type of maze to generate (default: random)")
parser.add_argument("--width", type=int, default=30,
                    help="Width of the maze (default: 30, ignored for static)")
parser.add_argument("--height", type=int, default=30,
                    help="Height of the maze (default: 30, ignored for static)")
args = parser.parse_args()

# Create a maze instance common to all processes
maze = create_maze(args.width, args.height, args.type)

# Create a BFS solver instance and solve the maze
solver = BFSSolver(maze)
path, time_taken = solver.solve()

moves = len(path) if path is not None else 0
backtracks = 0  # BFS does not backtrack
avg_moves_sec = (moves / time_taken) if time_taken > 0 else 0

# Prepare the result dictionary for this process
result = {
    "rank": rank,
    "time_taken": time_taken,
    "moves": moves,
    "backtracks": backtracks,
    "moves_per_sec": avg_moves_sec
}

# Gather the results from all processes at the root (rank 0)
all_results = comm.gather(result, root=0)

if rank == 0:
    print("\n=== MPI Parallel BFS Maze Solver Summary ===")
    for res in all_results:
        print(f"Solver (Rank {res['rank']}): Time = {res['time_taken']:.2f} s, "
              f"Moves = {res['moves']}, Backtracks = {res['backtracks']}, "
              f"Average Moves/sec = {res['moves_per_sec']:.2f}")
    
    # Identify the best solver run based on the minimal number of moves
    valid_results = [r for r in all_results if r['moves'] is not None]
    if valid_results:
        best = min(valid_results, key=lambda r: r["moves"])
        print(f"\nBest Solver: Rank {best['rank']} with performance:")
        print(f"Time Taken     = {best['time_taken']:.2f} s")
        print(f"Total Moves    = {best['moves']}")
        print(f"Backtracks     = {best['backtracks']}")
        print(f"Moves per Sec  = {best['moves_per_sec']:.2f}")
    else:
        print("No valid solution was found by any process.")
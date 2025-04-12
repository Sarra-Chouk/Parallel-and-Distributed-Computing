from mpi4py import MPI
import argparse
from src.maze import create_maze
from src.explorer import Explorer

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MPI Maze Explorer")
parser.add_argument("--type", choices=["random", "static"], default="random",
                    help="Type of maze to generate (default: random)")
parser.add_argument("--width", type=int, default=30,
                    help="Width of the maze (default: 30, ignored for static)")
parser.add_argument("--height", type=int, default=30,
                    help="Height of the maze (default: 30, ignored for static)")
args = parser.parse_args()

# Each process creates the same maze
maze = create_maze(args.width, args.height, args.type)

# Create an explorer instance without visualization
explorer = Explorer(maze, visualize=False)

# Solve the maze; each process does this independently
time_taken, moves = explorer.solve()

# Compute average moves per second (avoid division by zero)
avg_moves_sec = (len(moves) / time_taken) if time_taken > 0 else 0

# Prepare result dictionary for this process
result = {
    "rank": rank,
    "time_taken": time_taken,
    "moves": len(moves),
    "backtracks": explorer.backtrack_count,
    "moves_per_sec": avg_moves_sec
}

# Gather results from all processes at the root process (rank 0)
all_results = comm.gather(result, root=0)

if rank == 0:
    print("\n=== MPI Parallel Maze Exploration Summary ===")
    for res in all_results:
        print(f"Explorer (Rank {res['rank']}): Time = {res['time_taken']:.2f} s, "
              f"Moves = {res['moves']}, Backtracks = {res['backtracks']}, "
              f"Average Moves/sec = {res['moves_per_sec']:.2f}")
    
    best = min(all_results, key=lambda r: r["moves"])
    print(f"\nBest Explorer: Rank {best['rank']} with the following performance:")
    print(f"Time Taken = {best['time_taken']:.2f} s")
    print(f"Total Moves = {best['moves']}")
    print(f"Backtracks = {best['backtracks']}")
    print(f"Moves per Sec = {best['moves_per_sec']:.2f}\n")

from mpi4py import MPI
import argparse
import time
from src.maze import create_maze, StaticMaze
from src.explorer import Explorer

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="MPI Parallel Maze Explorer")
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

# Solve the maze
start_time = time.time()
time_taken, moves = explorer.solve()
end_time = time.time()

# Calculate actual time taken (more accurate for MPI)
actual_time = end_time - start_time

# Prepare result dictionary for this process
result = {
    "rank": rank,
    "time_taken": actual_time,
    "moves": len(moves),
    "backtracks": explorer.backtrack_count,
    "moves_per_sec": len(moves) / actual_time if actual_time > 0 else 0,
    "maze_type": args.type
}

# Gather results from all processes at the root process (rank 0)
all_results = comm.gather(result, root=0)

# The root process prints a summary of the exploration results
if rank == 0:
    print("\n=== MPI Parallel Maze Exploration Summary ===")
    print(f"Total explorers: {size}")
    print(f"Maze type: {args.type}")
    if args.type == "random":
        print(f"Maze dimensions: {args.width}x{args.height}")
    
    # Print individual results
    for res in all_results:
        print(f"\nExplorer (Rank {res['rank']}):")
        print(f"  Time taken: {res['time_taken']:.4f} seconds")
        print(f"  Total moves: {res['moves']}")
        print(f"  Backtracks: {res['backtracks']}")
        print(f"  Moves per second: {res['moves_per_sec']:.2f}")
    
    # Determine the best performer (one with the minimal number of moves)
    best = min(all_results, key=lambda r: r["moves"])
    
    print("\n=== Best Explorer ===")
    print(f"Rank: {best['rank']}")
    print(f"Time taken: {best['time_taken']:.4f} seconds")
    print(f"Total moves: {best['moves']}")
    print(f"Backtracks: {best['backtracks']}")
    print(f"Moves per second: {best['moves_per_sec']:.2f}")
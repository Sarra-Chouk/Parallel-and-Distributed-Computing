from mpi4py import MPI
import argparse
from src.maze import create_maze
from src.right_explorer import EnhancedExplorer

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Parse command-line arguments.
parser = argparse.ArgumentParser(
    description="MPI Maze Solver using Enhanced (Right-hand) Explorer (headless)"
)
parser.add_argument("--type", choices=["random", "static"], default="random",
                    help="Type of maze to generate (default: random)")
parser.add_argument("--width", type=int, default=30,
                    help="Maze width (default: 30; ignored for static mazes)")
parser.add_argument("--height", type=int, default=30,
                    help="Maze height (default: 30; ignored for static mazes)")
args = parser.parse_args()

# Create a maze instance common to all processes.
maze = create_maze(args.width, args.height, args.type)

# Create an instance of EnhancedExplorer (headless).
explorer = EnhancedExplorer(maze, visualize=False)

# Solve the maze using the enhanced right-hand rule approach.
time_taken, moves = explorer.solve()

# Evaluation metrics:
#   - "moves": the length of the solution path.
#   - "backtracks": the number of backtrack operations performed.
#   - "average moves per second": moves divided by total time.
moves_count = len(moves)
backtracks = explorer.backtrack_count
avg_moves_sec = (moves_count / time_taken) if time_taken > 0 else 0

# Prepare the result dictionary for this MPI process.
result = {
    "rank": rank,
    "time_taken": time_taken,
    "moves": moves_count,
    "backtracks": backtracks,
    "moves_per_sec": avg_moves_sec
}

# Gather results from all processes at the root (rank 0).
all_results = comm.gather(result, root=0)

if rank == 0:
    print("\n=== MPI Parallel Enhanced Maze Explorer Summary ===")
    for res in all_results:
        print(f"Explorer (Rank {res['rank']}): Time = {res['time_taken']:.4f} s, "
              f"Moves = {res['moves']}, Backtracks = {res['backtracks']}, "
              f"Average Moves/sec = {res['moves_per_sec']:.2f}")
    
    valid_results = [r for r in all_results if r["moves"] is not None]
    if valid_results:
        best = min(valid_results, key=lambda r: r["moves"])
        print(f"\nBest Explorer: Rank {best['rank']} with performance:")
        print(f"Time Taken     = {best['time_taken']:.4f} s")
        print(f"Total Moves    = {best['moves']}")
        print(f"Backtracks     = {best['backtracks']}")
        print(f"Average Moves/sec  = {best['moves_per_sec']:.2f}")
    else:
        print("No valid solution was found by any process.")
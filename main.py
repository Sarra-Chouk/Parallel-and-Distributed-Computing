"""
Main entry point for the maze runner game (supports MPI-based parallel execution).
"""

import argparse
from mpi4py import MPI
from src.maze import create_maze
from src.right_explorer import Explorer as RightHandExplorer
from src.bfs_explorer import BFSSolver
from src.astar_explorer import AStarExplorer

def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate")
    parser.add_argument("--width", type=int, default=30,
                        help="Maze width (ignored for static)")
    parser.add_argument("--height", type=int, default=30,
                        help="Maze height (ignored for static)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze solving")
    parser.add_argument("--explorer", choices=["right", "bfs", "astar"], default="right",
                        help="Which solver to use: 'right', 'bfs', or 'astar'")
    args = parser.parse_args()

    if args.auto:
        # All processes generate the same maze for consistency
        maze = create_maze(args.width, args.height, args.type)

        # Choose and run the selected solver
        if args.explorer == "right":
            explorer = RightHandExplorer(maze, visualize=False)
            time_taken, moves = explorer.solve()
            moves_count = len(moves)
            backtracks = explorer.backtrack_count

        elif args.explorer == "bfs":
            solver = BFSSolver(maze)
            path, time_taken = solver.solve()
            moves_count = len(path) if path else 0
            backtracks = 0

        elif args.explorer == "astar":
            solver = AStarExplorer(maze)
            path, time_taken = solver.solve()
            moves_count = len(path) if path else 0
            backtracks = 0

        else:
            raise ValueError(f"Unsupported explorer type: {args.explorer}")

        avg_moves_sec = (moves_count / time_taken) if time_taken > 0 else 0

        # MPI: gather results from all ranks
        result = {
            "rank": rank,
            "time_taken": time_taken,
            "moves": moves_count,
            "backtracks": backtracks,
            "moves_per_sec": avg_moves_sec
        }
        all_results = comm.gather(result, root=0)

        # Output the summary at rank 0
        if rank == 0:
            print(f"\n=== MPI Parallel {args.explorer.upper()} Maze Solver Summary ===")
            for res in all_results:
                print(f"Solver (Rank {res['rank']}): Time = {res['time_taken']:.4f} s, "
                      f"Moves = {res['moves']}, Backtracks = {res['backtracks']}, "
                      f"Average Moves/sec = {res['moves_per_sec']:.2f}")

            best = min(all_results, key=lambda r: r["moves"])
            print(f"\nBest Solver: Rank {best['rank']} with performance:")
            print(f"Time Taken     = {best['time_taken']:.4f} s")
            print(f"Total Moves    = {best['moves']}")
            print(f"Backtracks     = {best['backtracks']}")
            print(f"Moves per Sec  = {best['moves_per_sec']:.2f}")

if __name__ == "__main__":
    main()
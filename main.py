"""
Main entry point for the Maze Runner Game.
This program can run automated maze exploration using one of the following algorithms:
 - "right": the original right-hand rule explorer (from src/right_explorer.py)
 - "bfs": using BFS (see src/bfs_explorer.py)
 - "astar": using A* search (see src/astar_explorer.py)

It also supports running in parallel using mpi4py. In parallel mode each MPI process runs the chosen
explorer independently on the same maze (broadcasted from rank 0) and sends a summary of its performance.
Rank 0 then prints all summaries and details of the best solver (one with the fewest moves).
Note: Visualization is omitted to be able to run the program on my VM.
"""

import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--algorithm", choices=["right", "bfs", "astar"], default="right",
                        help="Explorer algorithm to use: 'right' (right-hand rule), 'bfs', or 'astar'")
    parser.add_argument("--parallel", action="store_true",
                        help="Run explorers in parallel using mpi4py")
    args = parser.parse_args()

    if not args.auto:
        # Run interactive game
        from src.game import run_game
        run_game(maze_type=args.type, width=args.width, height=args.height)
        return

    if args.parallel:
        # Parallel (MPI) mode
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        # Rank 0 creates the maze and broadcasts it to all processes
        if rank == 0:
            from src.maze import create_maze
            maze = create_maze(args.width, args.height, args.type)
        else:
            maze = None
        maze = comm.bcast(maze, root=0)

        # Select and initialize the chosen explorer algorithm
        if args.algorithm == "right":
            from src.right_explorer import Explorer
            explorer = Explorer(maze, visualize=False)
        elif args.algorithm == "bfs":
            from src.bfs_explorer import BFSExplorer
            explorer = BFSExplorer(maze)
        elif args.algorithm == "astar":
            from src.astar_explorer import AStarExplorer
            explorer = AStarExplorer(maze)
        elif args.algorithm == "rl":
            from src.rl_explorer import RLExplorer
            explorer = RLExplorer(maze)
        else:
            raise ValueError("Unknown algorithm")

        # Each process runs its solver
        time_taken, path = explorer.solve()
        moves_count = len(path)
        moves_per_sec = moves_count / time_taken if time_taken > 0 else 0

        summary = {
            'rank': rank,
            'time_taken': time_taken,
            'moves': moves_count,
            'backtracks': getattr(explorer, 'backtracks', 0),
            'moves_per_sec': moves_per_sec
        }

        all_summaries = comm.gather(summary, root=0)

        if rank == 0:
            print("\n=== Parallel Maze Exploration Summaries ===")
            for s in all_summaries:
                print(f"Rank {s['rank']}: Time Taken = {s['time_taken']:.4f} s, Total Moves = {s['moves']}, "
                      f"Backtracks = {s['backtracks']}, Moves per Sec = {s['moves_per_sec']:.2f}")
            best = min(all_summaries, key=lambda x: x['moves'])
            print("\nBest Solver: Rank {} with performance:".format(best['rank']))
            print(f"Time Taken     = {best['time_taken']:.4f} s")
            print(f"Total Moves    = {best['moves']}")
            print(f"Backtracks     = {best['backtracks']}")
            print(f"Moves per Sec  = {best['moves_per_sec']:.2f}")
    else:
        # Non-parallel mode
        from src.maze import create_maze
        maze = create_maze(args.width, args.height, args.type)
        if args.algorithm == "right":
            from src.right_explorer import Explorer
            explorer = Explorer(maze, visualize=False)
        elif args.algorithm == "bfs":
            from src.bfs_explorer import BFSExplorer
            explorer = BFSExplorer(maze)
        elif args.algorithm == "astar":
            from src.astar_explorer import AStarExplorer
            explorer = AStarExplorer(maze)
        elif args.algorithm == "rl":
            from src.rl_explorer import RLExplorer
            explorer = RLExplorer(maze)
        else:
            raise ValueError("Unknown algorithm")

        time_taken, path = explorer.solve()
        moves_count = len(path)
        moves_per_sec = moves_count / time_taken if time_taken > 0 else 0

        print(f"Maze solved in {time_taken:.4f} seconds")
        print(f"Total Moves    = {moves_count}")
        print(f"Backtracks     = {getattr(explorer, 'backtracks', 0)}")
        print(f"Moves per Sec  = {moves_per_sec:.2f}")
        if args.type == "static":
            print("Note: Width and height arguments were ignored for the static maze")

if __name__ == "__main__":
    main()
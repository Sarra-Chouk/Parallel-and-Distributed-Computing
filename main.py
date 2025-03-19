import time
from src.sequential.genetic_algorithm_trial import run_genetic_algorithm
from src.distributed.genetic_algorithm_trial import run_genetic_algorithm_parallel
from mpi4py import MPI

def main():
    """
    Main function to run and time the genetic algorithm.
    """
    # Sequential execution time
    if MPI.COMM_WORLD.Get_rank() == 0:
        start_seq_time = time.time()
        run_genetic_algorithm()
        end_seq_time = time.time()
        seq_time = end_seq_time - start_seq_time
        print(f"\nTotal Sequential Execution Time: {seq_time:.2f} seconds\n")

    # Parallel execution time
    start_parallel_time = time.time()
    run_genetic_algorithm_parallel()
    end_parallel_time = time.time()

    if MPI.COMM_WORLD.Get_rank() == 0:
        parallel_time = end_parallel_time - start_parallel_time
        print(f"\nTotal Parallel Execution Time: {parallel_time:.2f} seconds")
        speedup = seq_time / parallel_time
        efficiency = speedup / MPI.COMM_WORLD.Get_size()
        print(f"Speedup: {speedup:.2f}")
        print(f"Efficiency: {efficiency:.2f}")

if __name__ == "__main__":
    main()
import time
import sys
from mpi4py import MPI
from src.sequential.genetic_algorithm_trial import run_genetic_algorithm
from src.parallel.genetic_algorithm_trial import run_genetic_algorithm_parallel
from src.distributed.genetic_algorithm_trial import run_distributed_genetic_algorithm
from src.extended.genetic_algorithm_trial import run_distributed_genetic_algorithm_extended
   
   
def main():
    """
    Main function to run:
      - Sequential and parallel versions when run with a single process.
      - Distributed MPI version when run with mpirun -n X python main.py.
      - For the extended city map, pass the '--mpi-extended' flag.
      - For multi-machine distributed runs (total cores = 12), pass the '--multi-machine' flag.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # When running in single-process mode, execute sequential and parallel versions.
    if size == 1:
        print("\n===== Sequential Execution =====\n")
        start_seq_time = time.time()
        run_genetic_algorithm()
        end_seq_time = time.time()
        seq_time = end_seq_time - start_seq_time
        print(f"\nTotal Sequential Execution Time: {seq_time:.2f} seconds\n")

        print("\n===== Multiprocessing Execution =====\n")
        start_parallel_time = time.time()
        run_genetic_algorithm_parallel()
        end_parallel_time = time.time()
        parallel_time = end_parallel_time - start_parallel_time
        speedup_parallel = seq_time / parallel_time
        efficiency_parallel = speedup_parallel / 6  # 6 cores assumed in single-machine parallel
        print(f"\nTotal Parallel Execution Time: {parallel_time:.2f} seconds")
        print(f"Speedup: {speedup_parallel:.2f}")
        print(f"Efficiency: {efficiency_parallel:.2f}\n")
    else:
        # Determine total core count based on command-line flag.
        # If '--multi-machine' flag is provided, assume 12 cores; otherwise, assume 6.
        total_cores = 12 if '--multi-machine' in sys.argv else 6

        # Distributed execution across multiple MPI processes.
        if rank == 0:
            print("\n===== Distributed Execution =====\n")
        comm.Barrier()

        # Check for the '--mpi-extended' flag to decide which dataset to use.
        if '--mpi-extended' in sys.argv:
            dist_start = time.time()
            run_distributed_genetic_algorithm_extended()
            comm.Barrier()
            dist_end = time.time()
            dist_time = dist_end - dist_start
            # Baseline sequential time assumed as 25.02 seconds for speedup calculation.
            speedup_dist = 25.02 / dist_time
            efficiency_dist = speedup_dist / total_cores
            if rank == 0:
                print(f"\nTotal Distributed (Extended) Execution Time: {dist_time:.2f} seconds")
                print(f"Speedup: {speedup_dist:.2f}")
                print(f"Efficiency: {efficiency_dist:.2f}\n")
        else:
            dist_start = time.time()
            run_distributed_genetic_algorithm()
            comm.Barrier()
            dist_end = time.time()
            dist_time = dist_end - dist_start
            speedup_dist = 61.5 / dist_time
            efficiency_dist = speedup_dist / total_cores
            if rank == 0:
                print(f"\nTotal Distributed Execution Time: {dist_time:.2f} seconds")
                print(f"Speedup: {speedup_dist:.2f}")
                print(f"Efficiency: {efficiency_dist:.2f}\n")

if __name__ == "__main__":
    main()
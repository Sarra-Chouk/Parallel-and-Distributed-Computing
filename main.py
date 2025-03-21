import time
from mpi4py import MPI
from src.sequential.genetic_algorithm_trial import run_genetic_algorithm
from src.parallel.genetic_algorithm_trial import run_genetic_algorithm_parallel
from src.distributed.genetic_algorithm_trial import run_genetic_algorithm_mpi_multiproc

def main():
    """
    Main function to run either:
    - Sequential and parallel (if run with python main.py), OR
    - Distributed MPI version (if run with mpirun -n X python main.py)
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size == 1:
        # === Sequential Ecexution ===
        print("\n===== Sequential Execution =====\n")
        start_seq_time = time.time()
        run_genetic_algorithm()
        end_seq_time = time.time()
        seq_time = end_seq_time - start_seq_time
        print(f"\nTotal Sequential Execution Time: {seq_time:.2f} seconds\n")

        # === Parallel Ecexution ===
        print("\n===== Multiprocessing Execution =====\n")
        start_parallel_time = time.time()
        run_genetic_algorithm_parallel()
        end_parallel_time = time.time()
        parallel_time = end_parallel_time - start_parallel_time

        print(f"\nTotal Parallel Execution Time: {parallel_time:.2f} seconds")
        speedup = seq_time / parallel_time
        efficiency = speedup / 6
        print(f"Speedup: {speedup:.2f}")
        print(f"Efficiency: {efficiency:.2f}\n")

    else:
        # === Distributed Execution ===
        if rank == 0:
            print("\n===== Distributed Execution =====\n")
        comm.Barrier()

        dist_start = time.time()
        run_genetic_algorithm_mpi_multiproc(broadcast_interval=50, local_pool_size=6)
        comm.Barrier()
        dist_end = time.time()
        dist_time = dist_end - dist_start

        if rank == 0:
            print(f"\nTotal Distributed Execution Time: {dist_time:.2f} seconds\n")

if __name__ == "__main__":
    main()
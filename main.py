import time
from mpi4py import MPI
import sys

# Import experiment functions
from src.sequential.genetic_algorithm_trial import run_genetic_algorithm
from src.parallel.genetic_algorithm_trial import run_parallel_genetic_algorithm
from src.distributed.genetic_algorithm_trial import run_genetic_algorithm_mpi_multiproc

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # When running without MPI (only one process), run sequential and multiprocessing experiments.
    if size == 1:
        if rank == 0:
            print("\n===== Sequential Execution =====\n")
            start_seq = time.time()
            run_genetic_algorithm()
            end_seq = time.time()
            seq_time = end_seq - start_seq
            print(f"Total Sequential Execution Time: {seq_time:.2f} seconds\n")

            print("\n===== Multiprocessed Execution =====\n")
            start_par = time.time()
            run_parallel_genetic_algorithm()
            end_par = time.time()
            par_time = end_par - start_par
            print(f"Total Parallel Execution Time: {par_time:.2f} seconds\n")
            print(f"Speedup (Parallel): {seq_time / par_time:.2f}")
            print(f"Efficiency (Parallel): {(seq_time / par_time) / 6:.2f}\n")
        comm.Barrier()
    else:
        # When running under MPI (size > 1), run only the MPI+Multiprocessing (distributed) experiment.
        if rank == 0:
            print("\n===== Distributed Execution (MPI+Multiprocessing) =====\n")
        start_mpi = time.time()
        # For example, here we use a broadcast_interval=50 and local_pool_size=6.
        run_genetic_algorithm_mpi_multiproc(broadcast_interval=50, local_pool_size=6)
        end_mpi = time.time()
        if rank == 0:
            mpi_time = end_mpi - start_mpi
            print(f"\nTotal Distributed (MPI+Multiproc) Execution Time: {mpi_time:.2f} seconds\n")
    # End of main()

if __name__ == "__main__":
    main()
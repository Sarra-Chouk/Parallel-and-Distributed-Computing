# src/calculate_squares.py
from mpi4py import MPI
import numpy as np
import time

def compute_squares(n):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Determine how many numbers each process will handle.
    # This creates an almost equal distribution.
    counts = [n // size + (1 if i < n % size else 0) for i in range(size)]
    displacements = [sum(counts[:i]) for i in range(size)]
    start = displacements[rank] + 1  # numbers from 1 to n (inclusive)
    end = start + counts[rank]

    local_numbers = np.arange(start, end, dtype=np.int64)
    local_squares = local_numbers ** 2

    # Gather local squares to root process
    all_local_squares = comm.gather(local_squares, root=0)
    if rank == 0:
        # Concatenate results from all processes
        all_squares = np.concatenate(all_local_squares)
        return all_squares
    return None

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    n = int(1e8)
    
    if rank == 0:
        start_time = time.time()
    
    squares = compute_squares(n)
    
    if rank == 0:
        end_time = time.time()
        total_time = end_time - start_time
        print("Total number of squares computed:", squares.size)
        print("Last square is:", squares[-1])
        print(f"Time taken: {total_time:2f} seconds")

if __name__ == "__main__":
    main()


# from mpi4py import MPI
# import numpy as np
# from src.calculate_squares import square
# import time
# import random

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# print(f"which process is this: {rank} and the size is {size}")

# if rank == 0:
#         numbers = np.arange(size, dtype="i")
#         print(numbers)
# else:
#     numbers = None

# number = np.zeros(1, dtype="i")
# comm.Scatter(numbers, number, root=0) 
# # Scatter --> like broadcasting, but one process distributes to all other processes NOT sends like in broadcasting
# # Each process take 1 [number] fron the vector
# print(numbers)
# print(number)

# result = square(number[0])
# print(result)
# time.sleep(random.randint(1, 10))

# request = comm.isend(result, dest=0, tag=rank) # this is non-blocking

# if rank == 0:
#     results = np.zeros(size, dtype="i")
#     for i in range(size):
#         results[i] = comm.irecv(source=i, tag=i).wait() # this is non-blocking also
#     print(f"The results are: {results}")

# # add this if using isend and irecv (non-bloacking)
# request.wait()
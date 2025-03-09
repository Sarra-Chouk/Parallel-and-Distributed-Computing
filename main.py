from mpi4py import MPI
import numpy as np
from src.square import square
import time
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"which process is this: {rank} and the size is {size}")

if rank == 0:
        numbers = np.arange(size, dtype="i")
        print(numbers)
else:
    numbers = None

number = np.zeros(1, dtype="i")
comm.Scatter(numbers, number, root=0) 
# Scatter --> like broadcasting, but one process distributes to all other processes NOT sends like in broadcasting
# Each process take 1 [number] fron the vector
print(numbers)
print(number)

result = square(number[0])
print(result)
time.sleep(random.randint(1, 10))

request = comm.isend(result, dest=0, tag=rank) # this is non-blocking

if rank == 0:
    results = np.zeros(size, dtype="i")
    for i in range(size):
        results[i] = comm.irecv(source=i, tag=i).wait() # this is non-blocking also
    print(f"The results are: {results}")

# add this if using isend and irecv (non-bloacking)
request.wait()
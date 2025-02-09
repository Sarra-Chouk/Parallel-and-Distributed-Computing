from src.sequential import run_sequential
from src.threads import run_threading
from src.processes import run_multiprocessing


# Define the value of n, number of threads and processes
K = int(1e8)
NUM_THREADS = 5
NUM_PROCESSES = 5

print("\n--- Running Sequential Summation ---")
sequential_sum, sequential_time = run_sequential(K)

print("\n--- Running Threaded Summation ---")
threaded_sum, threaded_time = run_threading(K, NUM_THREADS)
threads_speedup = sequential_time / threaded_time
threads_efficiency = threads_speedup / NUM_THREADS
print(f"Speedup: {threads_speedup}")
print(f"Efficiency: {threads_efficiency}")

# print("\n--- Running Multiprocessed Summation ---")
# multiprocesses_sum, multiprocessed_time = run_multiprocessing(K, NUM_PROCESSES)
# processes_speedup = sequential_time / multiprocessed_time
# processes_efficiency = processes_speedup / NUM_PROCESSES
# print(f"Speedup: {processes_speedup}")
# print(f"Efficiency: {processes_efficiency}")

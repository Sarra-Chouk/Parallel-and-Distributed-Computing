from src.sequential import run_sequential
from src.threads import run_threading
from src.processes import run_multiprocessing
import time


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
alpha_threads = 5.7220458984375e-06 / 3.0874314308166504 # sequential time (WITH run_threading commented) / total time (WITHOUT run_threading commented)
p_threads = 1 - alpha_threads
threads_amdahl = 1 / ((1 - p_threads) + (p_threads / 6))
threads_gustafson = 6 + alpha_threads*(1-6)

print(f"Speedup: {threads_speedup}")
print(f"Efficiency: {threads_efficiency}")
print(f"Amdahl's: {threads_amdahl}")
print(f"Gustafson's: {threads_gustafson}")

total_start_time = time.time()
print("\n--- Running Multiprocessed Summation ---")

multiprocesses_sum, multiprocessed_time = run_multiprocessing(K, NUM_PROCESSES)
total_end_time = time.time()
print(total_end_time-total_start_time)
processes_speedup = sequential_time / multiprocessed_time
processes_efficiency = processes_speedup / NUM_PROCESSES
alpha_processes = 5.7220458984375e-06 / 0.7608044147491455 # sequential time (with run_multiprocessing commented) / total time (without run_multiprocessing commented)
p_processes = 1 - alpha_threads
processes_amdahl = 1 / ((1 - p_processes) + (p_processes / 6))
processes_gustafson = 6 + alpha_processes*(1-6)

print(f"Speedup: {processes_speedup}")
print(f"Efficiency: {processes_efficiency}")
print(f"Amdahl's: {processes_amdahl}")
print(f"Gustafson's: {processes_gustafson}")

from src.sequential import run_sequential
from src.threads import run_threads
from src.processes import run_processes

sequential_time = run_sequential()
threading_time = run_threads()
multiprocessing_time = run_processes()

threads_speedup = sequential_time / threading_time
processes_speedup = sequential_time / multiprocessing_time

threads_efficiency = threads_speedup / 4
processes_efficiency = processes_speedup / 4

threads_amdahl = 12 / 17
processes_amdahl = 12 / 17

threads_gustafson = 5 + (6*17)
processes_gustafson = 5 + (6*17)

print(f"Threads Speedup: {threads_speedup}")
print(f"Processes Speedup: {processes_speedup}")
print(f"Threads Efficiency: {threads_efficiency}")
print(f"Processes Efficiency: {processes_efficiency }")
print(f"Threads Amdahl's: {threads_amdahl}")
print(f"Processes Amdahl's: {processes_amdahl}")
print(f"Threads Gustafson's: {threads_gustafson}")
print(f"Processes Gustafson's: {processes_gustafson }")

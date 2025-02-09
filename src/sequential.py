from src.calculate_sum import calculate_sum
import time


# Measure the total time for sum operation
def run_sequential(k = 1000000):
    total_start_time = time.time()
    total_sum = calculate_sum(end=k)
    total_end_time = time.time()
    elapsed_time = total_end_time - total_start_time
    print(f"Sum: {total_sum}\nTotal time taken: {elapsed_time} seconds")
    return total_sum, elapsed_time
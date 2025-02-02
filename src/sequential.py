from src.generate_random import join_random_letters, add_random_numbers
import time


# Measure the total time for both operations
def run_sequential(end_letters = 10000, end_numbers = 100000):
    total_start_time = time.time()
    join_random_letters(end = end_letters)
    add_random_numbers(end = end_numbers)
    total_end_time = time.time()
    print(f"Total time taken (sequential): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time
   
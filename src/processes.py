from src.generate_random import join_random_letters, add_random_numbers
import multiprocessing
import time


# Measure the total time for both operation
def run_processes(n_letters = 100000, n_numbers = 100000):
    total_start_time = time.time()

    # Create processes for both functions
    process_letters_1 = multiprocessing.Process(target=join_random_letters, args=(0, n_letters//2))
    process_letters_2 = multiprocessing.Process(target=join_random_letters, args=(n_letters//2, n_letters))
    process_numbers_1 = multiprocessing.Process(target=add_random_numbers, args=(0, n_numbers//2))
    process_numbers_2 = multiprocessing.Process(target=add_random_numbers, args=(n_numbers//2, n_numbers))

    # Start the processes
    process_letters_1.start()
    process_letters_2.start()
    process_numbers_1.start()
    process_numbers_2.start()

    # Wait for all processes to complete
    process_letters_1.join()
    process_letters_2.join()
    process_numbers_1.join()
    process_numbers_2.join()

    total_end_time = time.time()
    print(f"Total time taken (processes): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time

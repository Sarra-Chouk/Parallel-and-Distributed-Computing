from src.generate_random import join_random_letters, add_random_numbers
import multiprocessing
import time

def run_processes(n_letters=100000, n_numbers=100000):
    total_start_time = time.time()
    
    # Calculate chunk sizes for letters and numbers
    chunk_size_letters = n_letters // 3
    chunk_size_numbers = n_numbers // 3

    # Create 3 processes for join_random_letters
    process_letters_1 = multiprocessing.Process(target=join_random_letters, args=(0, chunk_size_letters))
    process_letters_2 = multiprocessing.Process(target=join_random_letters, args=(chunk_size_letters, 2 * chunk_size_letters))
    process_letters_3 = multiprocessing.Process(target=join_random_letters, args=(2 * chunk_size_letters, n_letters))
    
    # Create 3 processes for add_random_numbers
    process_numbers_1 = multiprocessing.Process(target=add_random_numbers, args=(0, chunk_size_numbers))
    process_numbers_2 = multiprocessing.Process(target=add_random_numbers, args=(chunk_size_numbers, 2 * chunk_size_numbers))
    process_numbers_3 = multiprocessing.Process(target=add_random_numbers, args=(2 * chunk_size_numbers, n_numbers))
    
    # Start all processes
    process_letters_1.start()
    process_letters_2.start()
    process_letters_3.start()
    process_numbers_1.start()
    process_numbers_2.start()
    process_numbers_3.start()
    
    # Wait for all processes to complete
    process_letters_1.join()
    process_letters_2.join()
    process_letters_3.join()
    process_numbers_1.join()
    process_numbers_2.join()
    process_numbers_3.join()
    
    total_end_time = time.time()
    print(f"Total time taken (processes): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time
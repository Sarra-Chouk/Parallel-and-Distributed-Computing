from src.generate_random import join_random_letters, add_random_numbers
import threading 
import time


# Measure the total time for both operations
def run_threads(n_letters = 10000, n_numbers = 100000):
    total_start_time = time.time()
    
    # Create threads for both functions
    thread_letters_1 = threading.Thread(target=join_random_letters, args = (0, n_letters // 2))
    thread_letters_2 = threading.Thread(target=join_random_letters, args = (n_letters // 2, n_letters))
    thread_numbers_1 = threading.Thread(target=add_random_numbers, args = (0, n_numbers // 2))
    thread_numbers_2 = threading.Thread(target=add_random_numbers, args = (n_numbers // 2, n_numbers))

    # Start the threads
    thread_letters_1.start()
    thread_letters_2.start()
    thread_numbers_1.start()
    thread_numbers_2.start()

    # Wait for all threads to complete
    thread_letters_1.join()
    thread_letters_2.join()
    thread_numbers_1.join()
    thread_numbers_2.join()
    
    total_end_time = time.time()
    print(f"Total time taken (threads): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time
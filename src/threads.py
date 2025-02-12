from src.calculate_sum import calculate_sum
import queue
import threading
import time


# Function to run summation using threading
def run_threading(k, num_threads):
    threading_queue = queue.Queue()

    threads = []
    results = [0] * num_threads 
    chunk_size = k // num_threads

    total_start_time = time.time()

    # Creating and starting threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = k if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=calculate_sum, args=(start, end, threading_queue))
        threads.append(thread)
        thread.start()

    # Waiting for all threads to complete
    for thread in threads:
        thread.join()

    # Aggregating results from all threads
    total_sum = 0
    for _ in range(num_threads):
        result = threading_queue.get()
        total_sum += result
    total_end_time = time.time()

    elapsed_time = total_end_time - total_start_time
    print(f"Sum: {total_sum}")
    print(f"Total time taken: {elapsed_time} seconds")

    return total_sum, elapsed_time
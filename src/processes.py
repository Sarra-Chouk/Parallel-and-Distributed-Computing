from src.calculate_sum import calculate_sum
import multiprocessing
import time


def run_multiprocessing(k, num_processes):
    # Create a multiprocessing queue for sharing results
    multiprocessing_queue = multiprocessing.Queue()

    processes = []
    chunk_size = k // num_processes

    total_start_time = time.time()

    # Creating and starting processes
    for i in range(num_processes):
        start = i * chunk_size + 1
        # Ensure the end value is exactly k for the last process
        end = k if i == num_processes - 1 else (i + 1) * chunk_size
        process = multiprocessing.Process(
            target=calculate_sum, 
            args=(start, end, multiprocessing_queue)
        )
        processes.append(process)
        process.start()

    # Waiting for all processes to complete
    for process in processes:
        process.join()

    # Aggregating results from all processes
    total_sum = 0
    for _ in range(num_processes):
        result = multiprocessing_queue.get()
        total_sum += result

    total_end_time = time.time()
    elapsed_time = total_end_time - total_start_time

    print(f"Sum: {total_sum}")
    print(f"Total time taken: {elapsed_time} seconds")

    return total_sum, elapsed_time

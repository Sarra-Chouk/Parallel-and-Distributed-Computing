from src.calculate_sum import calculate_sum
import multiprocessing
import time

# Function to run summation using multiprocessing
def run_multiprocessing(k, num_processes):
    # Use Manager to create a shared list
    with multiprocessing.Manager() as manager:
        results = manager.list([0] * num_processes)

        chunk_size = k // num_processes
        total_start_time = time.time()

        # Create and start processes
        processes = []
        for i in range(num_processes):
            start = i * chunk_size + 1
            end = k if i == num_processes - 1 else (i + 1) * chunk_size
            process = multiprocessing.Process(target=calculate_sum, args=(start, end, results, i))
            processes.append(process)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Aggregate results from all processes
        total_sum = sum(results)
        total_end_time = time.time()

        elapsed_time = total_end_time - total_start_time
        print(f"Sum: {total_sum}")
        print(f"Total time taken (multiprocessing): {elapsed_time} seconds")

    return total_sum, elapsed_time
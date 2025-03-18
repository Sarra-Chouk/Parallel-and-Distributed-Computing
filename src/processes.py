import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from src.compute import square

def worker_square(n, output, index):
    """Worker function to compute squares and store in shared list."""
    output[index] = square(n)

def process_per_number(numbers):
    """Creates one process per number (not recommended for large datasets)."""
    manager = multiprocessing.Manager()
    output = manager.list([0] * len(numbers))
    processes = []

    start_mp1 = time.time()
    for idx, num in enumerate(numbers):
        p = multiprocessing.Process(target=worker_square, args=(num, output, idx))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    end_mp1 = time.time()
    mp1_time = end_mp1 - start_mp1

    print(f"\nProcess per number execution time: {mp1_time:.4f} seconds")

def pool_map(numbers):
    """Multiprocessing using Pool.map()."""
    start_mp2 = time.time()
    with multiprocessing.Pool() as pool:
        results_map = pool.map(square, numbers)
    end_mp2 = time.time()
    mp2_time = end_mp2 - start_mp2

    print(f"\nPooling with map() execution time: {mp2_time:.4f} seconds")

def pool_map_async(numbers):
    """Multiprocessing using Pool.map_async()."""
    start_mp2_async = time.time()
    with multiprocessing.Pool() as pool:
        async_result = pool.map_async(square, numbers)
        results_map_async = async_result.get()
    end_mp2_async = time.time()
    mp2_async_time = end_mp2_async - start_mp2_async

    print(f"\nPooling with map_async() execution time: {mp2_async_time:.4f} seconds")

def pool_apply(numbers):
    """Multiprocessing using Pool.apply()."""
    start_mp3 = time.time()
    results_apply = []
    with multiprocessing.Pool() as pool:
        for n in numbers:
            result = pool.apply(square, (n,))
            results_apply.append(result)
    end_mp3 = time.time()
    mp3_time = end_mp3 - start_mp3

    print(f"\nPooling with apply() execution time: {mp3_time:.4f} seconds")

def pool_apply_async(numbers):
    """Multiprocessing using Pool.apply_async()."""
    start_mp3_async = time.time()
    with multiprocessing.Pool() as pool:
        async_results = [pool.apply_async(square, (n,)) for n in numbers]
        results_apply_async = [r.get() for r in async_results]
    end_mp3_async = time.time()
    mp3_async_time = end_mp3_async - start_mp3_async

    print(f"\nPooling with apply_async() execution time: {mp3_async_time:.4f} seconds")

def process_pool_executor(numbers):
    """Multiprocessing using ProcessPoolExecutor()."""
    start_mp4 = time.time()
    with ProcessPoolExecutor() as executor:
        results_executor = list(executor.map(square, numbers))
    end_mp4 = time.time()
    mp4_time = end_mp4 - start_mp4

    print(f"\nPooling with ProcessPoolExecutor() execution time: {mp4_time:.4f} seconds")
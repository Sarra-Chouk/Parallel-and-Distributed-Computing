from src.compute import generate_numbers
from src.sequential import sequential_execution
from src.processes import (
    process_per_number, pool_map, pool_map_async,
    pool_apply, pool_apply_async, process_pool_executor
)
from src.connection_pool import ConnectionPool, access_database
import multiprocessing

if __name__ == "__main__":
    print("\nGenerating 10⁶ random numbers...")
    numbers6 = generate_numbers()
    
    print("\n--- Running Sequential Execution ---")
    sequential_execution(numbers6)
    
    print("\n--- Running Multiprocessing Tests ---")
    #process_per_number(numbers6)  # WARNING: This may cause memory issues.
    pool_map(numbers6)
    pool_map_async(numbers6)
    pool_apply(numbers6)
    pool_apply_async(numbers6)
    process_pool_executor(numbers6)
    
    print("Generating 10⁷ random numbers...")
    numbers7 = generate_numbers(size=10**7)

    print("\n--- Running Sequential Execution ---")
    sequential_execution(numbers7)

    print("\n--- Running Multiprocessing Tests ---")
    #process_per_number(numbers7)  # WARNING: This may cause memory issues.
    pool_map(numbers7)
    pool_map_async(numbers7)
    pool_apply(numbers7)
    pool_apply_async(numbers7)
    process_pool_executor(numbers7)

    print("\n--- Running Database Connection Pooling Simulation ---")
    
    num_processes = 6
    max_connections = 3
    
    pool_instance = ConnectionPool(max_connections)
    processes = []
    
    for _ in range(num_processes):
        p = multiprocessing.Process(target=access_database, args=(pool_instance,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        
    print("\n--- All tests completed! ---\n")

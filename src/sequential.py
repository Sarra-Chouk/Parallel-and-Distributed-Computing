import time
from src.compute import square

def sequential_execution(numbers):
    """Performs squaring sequentially and measures execution time."""
    start_seq = time.time()
    results_seq = [square(n) for n in numbers]
    end_seq = time.time()
    seq_time = end_seq - start_seq

    print(f"First 10 list elements: {numbers[:10]}")
    print(f"\nFirst 10 result elements: {results_seq[:10]}")
    print(f"\nSequential execution time for {len(numbers)} numbers: {seq_time:.4f} seconds")
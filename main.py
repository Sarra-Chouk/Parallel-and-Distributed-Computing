from src.tasks import power
from src.dispatch_tasks import dispatch
import time

if __name__ == "__main__":
    start_time = time.time()
    results = dispatch()
    end_time = time.time()
    print(results[:10])
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
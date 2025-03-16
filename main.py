from src.tasks import power
from src.dispatch_tasks import dispatch

if __name__ == "__main__":
    results = dispatch()
    print(results[:10])
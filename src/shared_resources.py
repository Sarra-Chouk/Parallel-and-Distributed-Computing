import threading
from queue import Queue

# Shared resources
latest_temperatures = {}   
temperature_averages = {} 
readings_queue = Queue()

# Thread synchronization
lock = threading.RLock()
print_lock = threading.Lock()
import random
import time
import threading
from queue import Queue

latest_temperatures = {}   
temperature_averages = {} 
readings_queue = Queue()

lock = threading.RLock()
print_lock = threading.Lock()

def simulate_sensor(sensor_id):
    """
    Simulates a sensor by generating a random temperature (15-40°C) every second.
    Updates the global latest_temperatures and pushes the reading into the queue.
    """
    while True:
        temp = random.randint(15, 40)
        with lock:
            latest_temperatures[sensor_id] = temp
            readings_queue.put((sensor_id, temp))
        time.sleep(1)

def process_temperatures():
    """
    Processes sensor readings from the queue to compute a running average for each sensor.
    Uses a local dictionary to accumulate readings and then updates the global average.
    """
    sensor_readings = {}
    while True:
        sensor_id, temp = readings_queue.get() 
        sensor_readings.setdefault(sensor_id, []).append(temp)
        avg = sum(sensor_readings[sensor_id]) / len(sensor_readings[sensor_id])
        with lock:
            temperature_averages[sensor_id] = round(avg, 2)
        readings_queue.task_done()

def initialize_display():
    """
    Prints the initial display with placeholders.
    The initial layout (5 lines) shows:
      - A header.
      - Latest Temperatures for sensors 1, 2, and 3 (with placeholder --).
      - Averages for sensors 1, 2, and 3 (with placeholder --).
    """
    print("Current temperatures:")
    print("Latest Temperatures: Sensor 1: --°C  Sensor 2: --°C  Sensor 3: --°C")
    print("Sensor 1 Average:                          --°C")
    print("Sensor 2 Average:                          --°C")
    print("Sensor 3 Average:                          --°C")

def update_latest():
    """
    Updates the 'Latest Temperatures' display line every 1 second.
    Uses ANSI escape codes to move the cursor to line 2 and clear that line.
    """
    while True:
        with print_lock:
            print("\033[2;1H", end="")
            print("\033[K", end="")
            with lock:
                lt1 = latest_temperatures.get(1, "--")
                lt2 = latest_temperatures.get(2, "--")
                lt3 = latest_temperatures.get(3, "--")
            print(f"Latest Temperatures: Sensor 1: {lt1}°C  Sensor 2: {lt2}°C  Sensor 3: {lt3}°C")
            print("\033[6;1H", end="")
        time.sleep(1)

def update_averages():
    """
    Updates the average temperature display (lines 3-5) every 5 seconds.
    Uses ANSI escape codes to update each sensor's average in place.
    """
    while True:
        with print_lock:
            with lock:
                avg1 = temperature_averages.get(1, "--")
                avg2 = temperature_averages.get(2, "--")
                avg3 = temperature_averages.get(3, "--")
            print("\033[3;1H", end="")
            print("\033[K", end="")
            print(f"Sensor 1 Average:                          {avg1}°C")
            print("\033[4;1H", end="")
            print("\033[K", end="")
            print(f"Sensor 2 Average:                          {avg2}°C")
            print("\033[5;1H", end="")
            print("\033[K", end="")
            print(f"Sensor 3 Average:                          {avg3}°C")
            print("\033[6;1H", end="")
        time.sleep(5)

def main():
    print("\033[2J\033[H", end="") 
    
    initialize_display()
    
    for sensor_id in [1, 2, 3]:
        t = threading.Thread(target=simulate_sensor, args=(sensor_id,), daemon=True)
        t.start()
    
    processor_thread = threading.Thread(target=process_temperatures, daemon=True)
    processor_thread.start()
    
    latest_thread = threading.Thread(target=update_latest, daemon=True)
    averages_thread = threading.Thread(target=update_averages, daemon=True)
    latest_thread.start()
    averages_thread.start()
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
     


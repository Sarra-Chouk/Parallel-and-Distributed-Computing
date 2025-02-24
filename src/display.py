import time
from src.shared_resources import latest_temperatures, temperature_averages, lock, print_lock

def initialize_display():
    """
    Prints the initial display with placeholders using a loop.
    """
    num_sensors = 3
    print("Current temperatures:")

    latest_line = "Latest Temperatures: " + "  ".join([f"Sensor {i+1}: --°C" for i in range(num_sensors)])
    print(latest_line)

    for i in range(num_sensors):
        print(f"Sensor {i+1} Average:                          --°C")

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
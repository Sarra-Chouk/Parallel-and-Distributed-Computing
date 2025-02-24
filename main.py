import threading
import time
from src.sensors import simulate_sensor, process_temperatures
from src.display import initialize_display, update_latest, update_averages

def main():
    print("\033[2J\033[H", end="")

    initialize_display()

    # Start sensor threads
    for sensor_id in [1, 2, 3]:
        t = threading.Thread(target=simulate_sensor, args=(sensor_id,), daemon=True)
        t.start()

    # Start processing thread
    processor_thread = threading.Thread(target=process_temperatures, daemon=True)
    processor_thread.start()

    # Start display update threads
    latest_thread = threading.Thread(target=update_latest, daemon=True)
    averages_thread = threading.Thread(target=update_averages, daemon=True)
    latest_thread.start()
    averages_thread.start()

    # Keep main thread running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
import random
import time
import threading
from src.shared_resources import latest_temperatures, temperature_averages, readings_queue, lock

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
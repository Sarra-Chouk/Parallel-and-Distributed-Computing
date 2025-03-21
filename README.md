# Description

This project is Lab 04 part 1 from the DSAI3202 - Parallel and Distributed Computing course. It simulates a real-time temperature monitoring system using multithreading. The simulation demonstrates how concurrent threads can be used to simulate sensors, process data, and update the display.

---

## Breakdown

The program launches multiple sensor threads that continuously generate temperature data. At the same time:

- A processing thread computes statistics from the data.

- Display threads update the terminal with:

  - The most recent temperature values per sensor.
    
  - The running average for each sensor.

---

## How to run

<pre><code>pip install -r requirements.txt 
python main.py</code></pre>

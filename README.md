# Description

This project is Lab 01 from the DSAI3202 - Parallel and Distributed Computing course. It demonstrates how a single computational task performs under different execution strategies:

- Sequential
- Multithreading
- Multiprocessing

The program measures and compares the performance improvements using key parallel computing metrics such as:

- Speedup
- Efficiency
- Amdahl’s Law
- Gustafson’s Law
  
----

## Breakdown

The program:

1. Generates random data using the `generate_random.py` module.
   
2. Runs the task sequentially and times the execution.

3. Runs the same task using threads and measures performance metrics.
   
4. Runs it again using multiprocessing for comparison.

---

## How to run

<pre><code>pip install -r requirements.txt 
python main.py</code></pre>

# Description

This project is Lab 03 part 1 from the DSAI3202 - Parallel and Distributed Computing course. It demonstrates how the same summation task — computing the sum of numbers from 1 to a large number (e.g., 100 million) — performs under different execution strategies:

- Sequential
- Multithreading
- Multiprocessing

The goal is to visualize the performance gains achieved through parallelism and evaluate them using key metrics:

- Speedup
- Efficiency
- Amdahl’s Law
- Gustafson’s Law

---

## Breakdown

`1. Sequential Summation`

The program computes the sum using a single-threaded, linear approach.

`2. Multithreaded Summation`

The sum is split across multiple threads, and the result is aggregated.

`3. Multiprocessing Summation`

Similar to threading, but uses separate processes to take advantage of multiple CPU cores.

`4. Performance Analysis`

After execution, the program calculates Speedup, Efficiency, Amdahl’s Law and Gustafson’s Law.

---

## How to run

<pre><code>pip install -r requirements.txt 
python main.py</code></pre>

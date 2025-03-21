## **Conclusions for Squaring 10⁶ Integers**

#### `Sequential Execution:`
The sequential approach is extremely fast **(0.05 sec)** for squaring 10⁶ numbers because the computation itself is trivial.

#### `Process per Number:`
Creating one process per number is **not feasible** due to **enormous memory overhead**, resulting in a **memory allocation error**.

#### `Multiprocessing Pool:`
- **Pool.map():** The most efficient parallel method tested **(0.14 sec)**, though still slower than sequential execution due to process management overhead.
- **Pool.apply():** Highly **inefficient (164.69 sec)** due to its **blocking nature**.

#### `Concurrent Futures:`
This method suffers from **high overhead (107.75 sec)** compared to **Pool.map()**.

---

## **Conclusions for Squaring 10⁷ Integers**

#### `Sequential Execution:`
The sequential approach remains extremely fast **(0.54 sec)** for squaring 10⁷ numbers because it avoids parallel overhead.

#### `Process per Number:`
Creating one process per number remains **unfeasible** due to **extreme memory overhead**, resulting in an **OSError (memory allocation failure)**.

#### `Multiprocessing Pool:`
- **Pool.map():** Most efficient parallel method **(1.19 sec)**, though still slower than sequential execution due to process overhead.
- **Pool.map_async():** Slightly **improves performance (1.09 sec)** compared to synchronous mapping.
- **Pool.apply():** **Highly inefficient (1684.80 sec)** due to blocking execution.
- **Pool.apply_async():** **Better than `apply()` (533.68 sec)** but much slower than `Pool.map()`.

#### `Concurrent Futures:`
**High overhead (1099.29 sec)** compared to **Pool.map()**, making it inefficient for a simple computation.

### `Final Conclusion:`
For squaring large numbers, **sequential execution is the fastest** due to minimal overhead. **Pool.map() is the best parallel approach**, but multiprocessing adds unnecessary complexity for simple arithmetic tasks.

---

## **Observations on Process Synchronization with Semaphores**

#### `Handling More Processes Than Available Connections:`
When more processes request connections than available, **extra processes wait** until a connection is released. This ensures **only 3 processes access the resource at a time** (according to my example).

#### `Role of Semaphore in Preventing Race Conditions:`
Semaphores **restrict concurrent access** to match available connections. When a process **acquires a connection**, others **must wait** until it is released. This prevents **data corruption and conflicts**, ensuring **safe access**.

---

## How to run

Open the notebbok:

<pre><code>jupyter notebook notebooks/assignment1.part1.ipynb</code></pre>

Or run `.py` files via:

<pre><code>python main.py</code></pre>

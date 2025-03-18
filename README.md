<style>
    .styled-title {
        font-weight: bold;
        font-size: 12px;
        color: #ffffff;
        background: linear-gradient(135deg, #007BFF, #6610f2);
        padding: 5px 10px;
        border-radius: 8px;
        display: inline-block;
    }

    .final-conclusion {
        font-weight: bold;
        font-size: 14px;
        color: #ffffff;
        background-color: #007BFF;
        padding: 10px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
    }
</style>

### **Conclusions for Squaring 10⁶ Integers**

<span class="styled-title">Sequential Execution:</span>

  The sequential approach is extremely fast (0.05 sec) for squaring 10⁶ numbers because the computation itself is trivial.

<span class="styled-title">Process per Number:</span>

  Creating one process per number is not feasible due to enormous memory overhead, resulting in a memory allocation error.

<span class="styled-title">Multiprocessing Pool:</span>

  Using **Pool.map()** is the most efficient among the parallel methods tested (0.14 sec), though it’s still slower than the sequential version because of process management overhead.

  Using **Pool.apply()** is highly inefficient (164.69 sec) due to the blocking nature of each call.

<span class="styled-title">Concurrent Futures:</span>

  This method also suffers from high overhead (107.75 sec) compared to **Pool.map()**.

### **Conclusions for Squaring 10⁷ Integers**

<span class="styled-title">Sequential Execution:</span>

  The sequential approach is also extremely fast (0.54 sec) for squaring 10⁷ numbers because the computation itself is trivial and avoids parallel overhead.

<span class="styled-title">Process per Number:</span>

  Creating one process per number remains unfeasible due to extreme memory overhead, resulting in an **OSError (memory allocation failure)**. This approach is highly inefficient.

<span class="styled-title">Multiprocessing Pool:</span>

  Using **Pool.map()** is again the most efficient parallel approach (1.19 sec), though it is still slower than sequential execution due to process management overhead.

  Using **Pool.map_async()** slightly improves performance compared to the synchronous mapping (1.09 sec), benefiting from asynchronous execution.

  Using **Pool.apply()** is highly inefficient (1684.80 sec) because it blocks execution for each number, making it significantly slower than all other methods.

  Using **Pool.apply_async()** is an improvement over **apply()** (533.68 sec) but still much slower than **Pool.map()** due to individual function calls.

<span class="styled-title">Concurrent Futures:</span>

  This method also suffers from high overhead (1099.29 sec) compared to **Pool.map()**, making it inefficient for such a simple computation.

<span class="final-conclusion">**Final Conclusion:**</span>

For squaring large numbers, **sequential execution remains the fastest** due to minimal overhead. **Pool.map()** is the best parallel approach, but multiprocessing generally adds unnecessary complexity for simple arithmetic operations.

### **Observations on Process Synchronization with Semaphores**

<span class="styled-title">Handling More Processes Than Available Connections:</span>

  When more processes request connections than are available, the extra processes **wait** until a connection is released. This ensures that no more than the allowed number of processes (3 in this case) access the resource simultaneously.

<span class="styled-title">Role of Semaphore in Preventing Race Conditions:</span>

  The semaphore **restricts concurrent access** to the number of available connections. It ensures that when a process acquires a connection, no other process can access the same connection until it is released. This prevents **data corruption and conflicts**, maintaining controlled and safe access.

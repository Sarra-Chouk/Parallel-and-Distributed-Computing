def calculate_sum(start=0,
                  end=1000,
                  queue = None):
    """Computes the sum for a given range and 
    stores it in results[index]."""
    # total = sum(range(start, end + 1))
    total = 0
    for i in range(start, end+1):
        total += i
    if queue:
        queue.put(total)
    else:
        return total
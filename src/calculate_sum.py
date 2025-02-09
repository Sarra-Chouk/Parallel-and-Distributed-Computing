# Function to calculate sum of numbers
# def calculate_sum(k):
#     total = 0
#     for i in range(1, k+1):
#         total += i
#     return total

def calculate_sum(start=0,
                  end=1000,
                  queue = None):
    """Computes the sum for a given range and 
    stores it in results[index]."""
    # total = sum(range(start, end + 1))
    total = 0
    for i in range(start, end):
        total += i
    if queue:
        queue.put(total)
    else:
        return total + end
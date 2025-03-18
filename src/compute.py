import random
import time

def square(n):
    """Returns the square of a number."""
    return n * n

def generate_numbers(size=10**6, low=1, high=100):
    """Generates a list of random integers."""
    return [random.randint(low, high) for _ in range(size)]

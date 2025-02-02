import random
import string

# Function to join 1000 random letters
def join_random_letters(start = 0, end = 1000):
    letters = [random.choice(string.ascii_letters) for _ in range(start, end)]
    joined_letters = "".join(letters)
    return joined_letters

# Function to add 1000 random numbers
def add_random_numbers(start = 0, end = 1000):
    numbers = [random.randint(1, 100) for _ in range(start, end)]
    total_sum = sum(numbers)
    return total_sum
import numpy as np
import pandas as pd
from multiprocessing import Pool
from src.sequential.genetic_algorithms_functions import (
    calculate_fitness,
    select_in_tournament,
    order_crossover,
    mutate,
    generate_unique_population
)

def evolve_chunk(chunk, distance_matrix, num_generations, mutation_rate, stagnation_limit):
    """
    Evolve a sub-population (chunk) for a given number of generations using a Genetic Algorithm.
    
    Parameters:
      - chunk (list): A sub-population (list of routes).
      - distance_matrix (np.ndarray): The distance matrix.
      - num_generations (int): How many generations to evolve.
      - mutation_rate (float): Mutation rate.
      - stagnation_limit (int): Number of generations without improvement before regeneration.
      
    Returns:
      - tuple: (best_solution, best_distance) from this chunk.
    """
    num_nodes = distance_matrix.shape[0]
    population = chunk.copy()
    best_fitness = float('inf')
    stagnation_counter = 0

    # Evolve over generations
    for generation in range(num_generations):
        
        # Evaluate fitness for the current population
        fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
        current_best = np.min(fitness_values)

        # Check for improvement
        if current_best < best_fitness:
            best_fitness = current_best
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stuck (no improvement)
        if stagnation_counter >= stagnation_limit:
            best_individual = population[np.argmin(fitness_values)]
            population = generate_unique_population(len(population) - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue

        # Selection, crossover, and mutation
        selected = select_in_tournament(population, fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                parent1, parent2 = selected[i], selected[i + 1]
                route1 = order_crossover(parent1[1:], parent2[1:])
                offspring.append([0] + route1)

        # Apply mutation
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replace worst individuals with new offspring
        indices = np.argsort(fitness_values)[::-1][:len(mutated_offspring)]
        for i, idx in enumerate(indices):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < len(population):
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(ind) for ind in unique_population]

    # Final evaluation and return best result from this chunk
    fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    best_distance = -calculate_fitness(best_solution, distance_matrix)
    return best_solution, best_distance

def run_genetic_algorithm_parallel():
    """
    Parallel Genetic Algorithm:
    Splits a large population into chunks, runs GA evolution on each in parallel,
    and selects the best overall solution.
    """
    
    # Load distance matrix
    distance_matrix = pd.read_csv('dataset/city_distances.csv').to_numpy()
    num_nodes = distance_matrix.shape[0]

    # GA hyperparameters
    population_size = 10000
    num_chunks = 24
    chunk_size = population_size // num_chunks
    mutation_rate = 0.1
    num_generations = 500
    stagnation_limit = 5

    # Initialize population and divide it into chunks
    np.random.seed(42)
    full_population = generate_unique_population(population_size, num_nodes)
    chunks = [full_population[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)]
    
    # Prepare arguments for multiprocessing
    args = [
        (chunk, distance_matrix, num_generations, mutation_rate, stagnation_limit)
        for chunk in chunks
    ]

    # Run each chunk in parallel using multiprocessing
    with Pool(processes=num_chunks) as pool:
        results = pool.starmap_async(evolve_chunk, args).get()

    # Select the overall best solution across all chunks
    overall_best = None
    overall_distance = float('inf')
    for solution, distance in results:
        if distance < overall_distance:
            overall_distance = distance
            overall_best = solution

    print("Overall Total Distance:", overall_distance)
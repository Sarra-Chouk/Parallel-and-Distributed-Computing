import numpy as np
import pandas as pd
from multiprocessing import Pool
from src.sequential.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, generate_unique_population

def evolve_chunk(chunk, distance_matrix, num_generations, mutation_rate, stagnation_limit):
    """
    Evolve a sub-population (chunk) for a number of generations.
    
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
    population = chunk.copy()  # work on a local copy
    best_fitness = float('inf')
    stagnation_counter = 0
    
    for generation in range(num_generations):
        # Evaluate fitness; note: we use negative fitness so lower distance is better.
        fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
        current_best = np.min(fitness_values)
        if current_best < best_fitness:
            best_fitness = current_best
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate if no improvement for a while.
        if stagnation_counter >= stagnation_limit:
            best_individual = population[np.argmin(fitness_values)]
            # Regenerate all but one individual.
            population = generate_unique_population(len(population) - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue

        # Selection: run tournament selection.
        selected = select_in_tournament(population, fitness_values)
        offspring = []
        # For each pair, perform order crossover.
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                parent1, parent2 = selected[i], selected[i + 1]
                # Use the crossover on the sub-route (excluding the fixed starting node).
                route1 = order_crossover(parent1[1:], parent2[1:])
                offspring.append([0] + route1)
        # Mutate the offspring.
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replacement: replace the worst individuals with the new offspring.
        indices = np.argsort(fitness_values)[::-1][:len(mutated_offspring)]
        for i, idx in enumerate(indices):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness.
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < len(population):
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(ind) for ind in unique_population]

    # After evolution, select the best solution in this chunk.
    fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    best_distance = -calculate_fitness(best_solution, distance_matrix)
    return best_solution, best_distance

def run_parallel_genetic_algorithm():
    """
    Parallel version: divide the full population into 6 chunks, run the GA in parallel on each,
    and select the best overall solution.
    """
    # Load the distance matrix.
    distance_matrix = pd.read_csv('dataset/city_distances.csv').to_numpy()
    num_nodes = distance_matrix.shape[0]

    # GA parameters.
    population_size = 10000
    num_chunks = 6
    chunk_size = population_size // num_chunks
    mutation_rate = 0.1
    num_generations = 200
    stagnation_limit = 5

    np.random.seed(42)
    # Generate the full unique population.
    full_population = generate_unique_population(population_size, num_nodes)
    # Divide population into chunks.
    chunks = [full_population[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)]
    
    # Prepare arguments for each process.
    args = [(chunk, distance_matrix, num_generations, mutation_rate, stagnation_limit) for chunk in chunks]

    # Run evolution on each chunk in parallel.
    with Pool(processes=num_chunks) as pool:
        results = pool.starmap(evolve_chunk, args)

    # Each result is a tuple: (best_solution, best_distance) from that chunk.
    overall_best = None
    overall_distance = float('inf')
    for solution, distance in results:
        if distance < overall_distance:
            overall_distance = distance
            overall_best = solution

    print("Overall Best Solution:", overall_best)
    print("Overall Total Distance:", overall_distance)

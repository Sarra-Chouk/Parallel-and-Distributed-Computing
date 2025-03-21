from mpi4py import MPI
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

    for generation in range(num_generations):
        # Evaluate fitness for the current population
        fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
        current_best = np.min(fitness_values)

        if current_best < best_fitness:
            best_fitness = current_best
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if no improvement
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
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        
        # Replace least fit individuals with offspring
        indices = np.argsort(fitness_values)[::-1][:len(mutated_offspring)]
        for i, idx in enumerate(indices):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < len(population):
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(ind) for ind in unique_population]

    # Final evaluation and return the best individual
    fitness_values = np.array([-calculate_fitness(route, distance_matrix) for route in population])
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    best_distance = -calculate_fitness(best_solution, distance_matrix)
    return best_solution, best_distance

def run_distributed_genetic_algorithm_multiple():
    """
    Distributed Genetic Algorithm:
      - The master (rank 0) loads the dataset and initializes parameters.
      - Each process reads its portion of the data (Parallel I/O).
      - Dynamic load balancing is used to distribute chunks of work.
      - Each process evolves its sub-chunks in parallel using multiprocessing.
      - Finally, the best results are gathered and the overall best solution is selected.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Parallel I/O: Each process reads its portion of the data
    if rank == 0:
        distance_matrix = pd.read_csv('dataset/city_distances.csv').to_numpy()
    else:
        distance_matrix = None
    distance_matrix = comm.bcast(distance_matrix, root=0)

    # Parameters (broadcasted by the master)
    if rank == 0:
        num_nodes = distance_matrix.shape[0]
        population_size = 10000
        num_generations = 500
        mutation_rate = 0.1
        stagnation_limit = 5
        num_chunks = 24
        chunk_size = population_size // num_chunks

        np.random.seed(42)
        full_population = generate_unique_population(population_size, num_nodes)
        chunks = [full_population[i * chunk_size : (i + 1) * chunk_size] for i in range(num_chunks)]
    else:
        num_generations = None
        mutation_rate = None
        stagnation_limit = None
        chunks = None

    # Broadcast parameters to all processes
    num_generations = comm.bcast(num_generations, root=0)
    mutation_rate = comm.bcast(mutation_rate, root=0)
    stagnation_limit = comm.bcast(stagnation_limit, root=0)

    # Dynamic Load Balancing
    if rank == 0:
        chunk_queue = list(chunks)  # Convert chunks to a queue
        results = []
        active_workers = size - 1  # Number of workers (excluding master)

        while active_workers > 0 or chunk_queue:
            status = MPI.Status()
            data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()

            if data == "REQUEST":  # Worker requests a chunk
                if chunk_queue:
                    comm.send(chunk_queue.pop(0), dest=source)  # Send a chunk
                else:
                    comm.send(None, dest=source)  # No more chunks
                    active_workers -= 1
            else:  # Worker sends back results
                results.append(data)
    else:
        while True:
            comm.send("REQUEST", dest=0)  # Request a chunk
            chunk = comm.recv(source=0)

            if chunk is None:  # No more chunks
                break

            # Evolve the chunk
            result = evolve_chunk(chunk, distance_matrix, num_generations, mutation_rate, stagnation_limit)
            comm.send(result, dest=0)  # Send results back to master

    # Master selects the overall best solution
    if rank == 0:
        overall_best_solution = None
        overall_best_distance = float('inf')
        for solution, distance in results:
            if distance < overall_best_distance:
                overall_best_distance = distance
                overall_best_solution = solution
        print("Overall Best Solution:", overall_best_solution)
        print("Overall Best Total Distance:", overall_best_distance)
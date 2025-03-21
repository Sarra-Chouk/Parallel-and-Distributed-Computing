from mpi4py import MPI
import numpy as np
import pandas as pd
import time
from multiprocessing import Pool
from src.distributed.genetic_algorithms_functions import (
    calculate_fitness,            # The “regular” (serial) version used for selection/updating.
    generate_unique_population,
    select_in_tournament,
    order_crossover,
    mutate
)

# --- Vectorized fitness function for a chunk ---
def compute_fitness_chunk(chunk, distance_matrix):
    # Convert the chunk (list of routes) into a NumPy array.
    routes = np.array(chunk, dtype=int)  # shape (m, n)
    # Create a “rolled” version so that for each route the last city connects to the first.
    rolled = np.roll(routes, -1, axis=1)
    # Use advanced indexing to get the distances for each leg of each route.
    distances = distance_matrix[routes, rolled]  # shape (m, n)
    # If any leg equals 10000, mark the entire route as infeasible (apply penalty).
    penalty = 1e6
    invalid = np.any(distances == 10000, axis=1)
    fitness = -np.sum(distances, axis=1)
    fitness[invalid] = -penalty
    return fitness.tolist()

def run_genetic_algorithm_mpi_multiproc(broadcast_interval=20, local_pool_size=4):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # --- Initialization: master loads parameters and initial population ---
    if rank == 0:
        distance_matrix = pd.read_csv('dataset/city_distances.csv').to_numpy(dtype=int)
        num_nodes = distance_matrix.shape[0]
        population_size = 10000
        np.random.seed(42)
        population = generate_unique_population(population_size, num_nodes)
    else:
        distance_matrix = None
        num_nodes = None
        population_size = None
        population = None

    # Broadcast global parameters (blocking bcast for these smaller objects)
    distance_matrix = comm.bcast(distance_matrix, root=0)
    num_nodes = comm.bcast(num_nodes, root=0)
    population_size = comm.bcast(population_size, root=0)

    # Genetic algorithm parameters
    num_tournaments = 4
    mutation_rate = 0.1
    num_generations = 200
    stagnation_limit = 1

    # Only rank 0 holds the master (global) population.
    if rank == 0:
        global_population = population
    else:
        global_population = None

    # Main GA loop in segments (each segment = broadcast_interval generations)
    for seg_start in range(0, num_generations, broadcast_interval):
        # --- Non-blocking broadcast of the global population ---
        # Convert global_population (list of lists) to a NumPy array for broadcast.
        if rank == 0:
            global_population_np = np.array(global_population, dtype=int)
        else:
            global_population_np = np.empty((population_size, num_nodes), dtype=int)
        req = comm.Ibcast(global_population_np, root=0)
        req.Wait()
        # Convert back to list for local processing.
        global_population = global_population_np.tolist()

        # Each process now works on a local copy of the population.
        local_population = list(global_population)
        local_stagnation = 0
        best_local_fitness = float('inf')

        # Create a local multiprocessing pool.
        pool = Pool(processes=local_pool_size)
        for gen in range(broadcast_interval):
            # Split local_population into chunks.
            chunk_size = max(1, len(local_population) // local_pool_size)
            chunks = [local_population[i:i + chunk_size] for i in range(0, len(local_population), chunk_size)]
            # Compute fitness asynchronously over chunks.
            async_result = pool.starmap_async(compute_fitness_chunk,
                                              [(chunk, distance_matrix) for chunk in chunks])
            fitness_lists = async_result.get()  # Wait for completion.
            fitness_values = [val for sublist in fitness_lists for val in sublist]

            current_best = min(fitness_values)
            if current_best < best_local_fitness:
                best_local_fitness = current_best
                local_stagnation = 0
            else:
                local_stagnation += 1

            if local_stagnation >= stagnation_limit:
                best_index = fitness_values.index(min(fitness_values))
                best_individual = local_population[best_index]
                local_population = generate_unique_population(population_size - 1, num_nodes)
                local_population.append(best_individual)
                local_stagnation = 0

            fitness_values = np.array(fitness_values)
            selected = select_in_tournament(local_population, fitness_values)
            offspring = []
            for i in range(0, len(selected) - 1, 2):
                # For crossover, skip the fixed first node.
                child = order_crossover(selected[i][1:], selected[i + 1][1:])
                offspring.append([0] + child)
            mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

            # Replace worst individuals with offspring.
            worst_indices = np.argsort(fitness_values)[::-1][:len(mutated_offspring)]
            for j, idx in enumerate(worst_indices):
                local_population[idx] = mutated_offspring[j]

            # Ensure local population uniqueness.
            unique_local = set(tuple(ind) for ind in local_population)
            while len(unique_local) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_local.add(tuple(individual))
            local_population = [list(ind) for ind in unique_local]
        pool.close()
        pool.join()

        # Each MPI process finds its best candidate.
        local_fitness = [ -calculate_fitness(route, distance_matrix) for route in local_population ]
        local_best_index = np.argmin(local_fitness)
        local_best = local_population[local_best_index]
        local_best_fitness = min(local_fitness)

        # Gather best candidates from all processes at master.
        all_best = comm.gather((local_best_fitness, local_best), root=0)
        if rank == 0:
            best_overall = min(all_best, key=lambda x: x[0])
            print(f"After generation {seg_start + broadcast_interval}, global best fitness: {best_overall[0]}")
            # For the next segment, set the global population to the best candidate repeated.
            global_population = [best_overall[1]] * population_size
        global_population = comm.bcast(global_population, root=0)

    # Final evaluation: only master prints result.
    if rank == 0:
        final_fitness = np.array([-calculate_fitness(route, distance_matrix) for route in global_population])
        best_idx = np.argmin(final_fitness)
        best_solution = global_population[best_idx]
        print("MPI+Multiproc Best Solution:", best_solution)
        print("MPI+Multiproc Total Distance:", -calculate_fitness(best_solution, distance_matrix))

if __name__ == "__main__":
    run_genetic_algorithm_mpi_multiproc(broadcast_interval=20, local_pool_size=4)
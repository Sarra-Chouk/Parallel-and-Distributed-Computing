import numpy as np
import pandas as pd
from mpi4py import MPI
from src.distributed.genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament, order_crossover, mutate, generate_unique_population
)

def run_genetic_algorithm_parallel():
    """
    Run the genetic algorithm in parallel using MPI.
    """
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Load the distance matrix (only by the root process)
    if rank == 0:
        distance_matrix = pd.read_csv('dataset/city_distances.csv').to_numpy()
    else:
        distance_matrix = None

    # Broadcast the distance matrix to all processes
    distance_matrix = comm.bcast(distance_matrix, root=0)

    # Parameters
    num_nodes = distance_matrix.shape[0]
    population_size = 10000
    num_tournaments = 4
    mutation_rate = 0.1
    num_generations = 200
    infeasible_penalty = 1e6
    stagnation_limit = 5

    # Generate initial population (only by the root process)
    if rank == 0:
        np.random.seed(42)  # For reproducibility
        population = generate_unique_population(population_size, num_nodes)
    else:
        population = None

    # Scatter the population across processes
    if rank == 0:
        population_chunks = np.array_split(population, size)
    else:
        population_chunks = None

    local_population = comm.scatter(population_chunks, root=0)

    # Initialize variables for tracking stagnation
    best_fitness = -1e6
    stagnation_counter = 0

    # Main GA loop
    for generation in range(num_generations):
        # Evaluate fitness locally
        local_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in local_population])

        # Gather fitness values every 10 generations
        if generation % 10 == 0:
            all_fitness_values = comm.gather(local_fitness_values, root=0)

            # Root process checks for stagnation and regenerates population if necessary
            if rank == 0:
                all_fitness_values = np.concatenate(all_fitness_values)
                current_best_fitness = np.max(all_fitness_values)

                if current_best_fitness > best_fitness:
                    best_fitness = current_best_fitness
                    stagnation_counter = 0
                else:
                    stagnation_counter += 1

                if stagnation_counter >= stagnation_limit:
                    print(f"Regenerating population at generation {generation} due to stagnation")
                    best_individual = population[np.argmax(all_fitness_values)]
                    population = generate_unique_population(population_size - 1, num_nodes)
                    population.append(best_individual)
                    stagnation_counter = 0

            # Broadcast the updated population and stagnation counter
            population = comm.bcast(population, root=0)
            stagnation_counter = comm.bcast(stagnation_counter, root=0)

        # Selection, crossover, and mutation locally
        selected = select_in_tournament(local_population, local_fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replace the worst individuals in the local population
        for i, idx in enumerate(np.argsort(local_fitness_values)[::-1][:len(mutated_offspring)]):
            local_population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in local_population)
        while len(unique_population) < len(local_population):
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        local_population = [list(individual) for individual in unique_population]

        # Print best fitness (only by the root process)
        if rank == 0 and generation % 10 == 0:
            print(f"Generation {generation}: Best fitness = {current_best_fitness}")

    # Gather the final population and fitness values from all processes
    final_population = comm.gather(local_population, root=0)
    final_fitness_values = comm.gather(local_fitness_values, root=0)

    # Output the best solution (only by the root process)
    if rank == 0:
        combined_population = [ind for sublist in final_population for ind in sublist]
        combined_fitness_values = np.concatenate(final_fitness_values)

        best_idx = np.argmax(combined_fitness_values)
        best_solution = combined_population[best_idx]
        print("Best Solution:", best_solution)
        print("Total Distance:", -combined_fitness_values[best_idx])


if __name__ == "__main__":
    run_genetic_algorithm_parallel()
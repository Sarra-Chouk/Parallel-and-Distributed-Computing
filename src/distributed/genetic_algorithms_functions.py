import numpy as np

def calculate_fitness(route, distance_matrix):
    num_nodes = distance_matrix.shape[0]
    if len(route) != num_nodes or set(route) != set(range(num_nodes)):
        return float(-1e6)
    total_distance = 0
    for i in range(len(route) - 1):
        node1, node2 = int(route[i]), int(route[i + 1])
        distance = distance_matrix[int(node1), int(node2)]
        if distance == 10000:
            return float(-1e6)
        total_distance += distance
    distance = distance_matrix[int(route[-1]), int(route[0])]
    if distance == 10000:
        return -1e6
    total_distance += distance
    return -total_distance

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    selected = []
    for _ in range(number_tournaments):
        idx = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = idx[np.argmax(scores[idx])]
        selected.append(population[best_idx])
    return selected

def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(np.random.choice(range(size), 2, replace=False))
    offspring = [None] * size
    offspring[start:end + 1] = parent1[start:end + 1]
    fill_values = [x for x in parent2 if x not in offspring[start:end + 1]]
    idx = 0
    for i in range(size):
        if offspring[i] is None:
            offspring[i] = fill_values[idx]
            idx += 1
    return offspring

def mutate(route, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        i, j = np.random.choice(len(route), 2, replace=False)
        route[i], route[j] = route[j], route[i]
    return route

def generate_unique_population(population_size, num_nodes):
    population = set()
    while len(population) < population_size:
        individual = [0] + list(map(int, np.random.permutation(np.arange(1, num_nodes))))
        population.add(tuple(individual))
    return [list(ind) for ind in population]

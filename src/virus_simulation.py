from mpi4py import MPI
import numpy as np

def spread_virus(population, spread_chance, vaccination_rate):
    new_population = population.copy()
    # Infection probability reduced by vaccination rate.
    infection_prob = spread_chance * (1 - vaccination_rate)
    # For every uninfected individual, infect with probability infection_prob.
    randoms = np.random.random(population.shape)
    new_infections = (population == 0) & (randoms < infection_prob)
    new_population[new_infections] = 1
    return new_population

def simulate_virus(population, spread_chance, vaccination_rate, num_steps=10):
    for _ in range(num_steps):
        population = spread_virus(population, spread_chance, vaccination_rate)
    return population

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Parameters
    population_size = 100  # size of population per process
    spread_chance = 0.3
    # Set a different seed for each process to get varied vaccination rates.
    np.random.seed(42 + rank)
    vaccination_rate = np.random.uniform(0.1, 0.5)

    # Initialize population: all individuals uninfected (0).
    population = np.zeros(population_size, dtype=np.int32)
    
    # Only rank 0 infects a small percentage of individuals initially.
    if rank == 0:
        initial_infected_count = int(0.1 * population_size)
        infected_indices = np.random.choice(population_size, initial_infected_count, replace=False)
        population[infected_indices] = 1

    # Broadcast the initial population from rank 0 to all processes.
    population = comm.bcast(population, root=0)

    # Each process simulates virus spread independently.
    final_population = simulate_virus(population, spread_chance, vaccination_rate, num_steps=10)

    # Calculate infection rate for the process.
    total_infected = np.sum(final_population)
    infection_rate = total_infected / population_size

    # Gather infection rates at root.
    all_infection_rates = comm.gather(infection_rate, root=0)

    if rank == 0:
        for i, rate in enumerate(all_infection_rates):
            print(f"Process {i} Infection Rate: {rate:.2f}")

if __name__ == "__main__":
    main()
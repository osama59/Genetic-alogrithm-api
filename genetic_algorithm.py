import random
import copy

MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.75
GENERATIONS = 500


def init_population(products_data, population_size, genome_length):
    population = [
        products_data[i * genome_length : (i + 1) * genome_length]
        for i in range(population_size - 1)
    ]
    mutation_pool = products_data[
        (population_size - 1) * genome_length : (population_size) * genome_length
    ]

    return population, mutation_pool


def fitness(genome):
    total_score = 0

    for product in genome:
        interaction_score = (
            (product["viewd"] * 2)
            + (product["clicked"] * 5)
            + (product["purchased"] * 10)
        )

        rating_score = product["rating"] * 1.5

        total_score += interaction_score + rating_score

    # If all 5 items are from the same category, we penalize the score to encourage variety.
    categories = [p["category"] for p in genome]
    unique_categories = len(set(categories))

    if unique_categories == 1:
        total_score -= 15  # Heavy penalty for being boring
    elif unique_categories >= 3:
        total_score += 10  # Bonus for high variety

    return total_score


# Roulete wheel style selection
def select_parent(population, fitness_values):
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, fitness_values):
        current += fitness_value
        if current > pick:
            return individual


def crossover(parent1, parent2, genome_length):
    if random.random() < CROSSOVER_RATE:
        crossover_point = random.randint(1, genome_length - 1)

        return (
            parent1[:crossover_point] + parent2[crossover_point:],
            parent2[:crossover_point] + parent1[crossover_point:],
        )
    else:
        return parent1, parent2


def mutate(genome, mutation_pool):
    for i in range(len(genome)):
        if random.random() < MUTATION_RATE:
            old_product = genome[i]
            new_product = random.choice(mutation_pool)
            genome[i] = new_product
            mutation_pool.remove(new_product)
            mutation_pool.append(old_product)
    return genome


def run_genetic_algorithm(products_data, user_profile):
    genome_length = 5
    population_size = len(products_data) // genome_length

    population, mutation_pool = init_population(
        products_data, population_size, genome_length
    )

    for generation in range(GENERATIONS):
        fitness_values = [fitness(genome) for genome in population]

        new_population = []
        for _ in range(population_size // 2):
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)

            parent1 = copy.deepcopy(parent1)
            parent2 = copy.deepcopy(parent2)

            offspring1, offspring2 = crossover(parent1, parent2, genome_length)
            new_population.extend(
                [
                    mutate(offspring1, mutation_pool),
                    mutate(offspring2, mutation_pool),
                ]
            )

        population = new_population
        fitness_values = [fitness(genome) for genome in population]

    best_fitness = max(fitness_values)
    best_index = fitness_values.index(best_fitness)
    best_solution = [product["id"] for product in population[best_index]]
    return best_solution

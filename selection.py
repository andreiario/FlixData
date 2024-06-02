from random import uniform, choice
from operator import attrgetter

## Fitness proportionate selection (roulette wheel)

def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    if population.optim == "max":
        total_fitness = sum([i.fitness for i in population])
        r = uniform(0, total_fitness)
        position = 0
        for individual in population:
            position += individual.fitness
            if position > r:
                return 
            
    elif population.optim == "min":
        total_fitness = sum([(1 / i.fitness) for i in population])
        r = uniform (0, total_fitness)
        position = 0
        for individual in population:
            position += (1 / individual.fitness)
            if position > r:
                return individual
    else:
        raise Exception(f"Optimization not specified (max/min)")
    
## Tournament selection

def tournament_sel(population, tour_size = 2):
    """Tournament selection implementation.
    
    Args:
        population (Population): The population we want to select from.
        
    Returns:
        Individual: selected individual.
    """

    # completely random
    tournament = [choice(population) for _ in range(tour_size)]

    if population.optim == 'max':
        return max(tournament, key=attrgetter('fitness'))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter('fitness'))
    
## Ranking selection

def rank_selection(population):
    """Rank-based selection implementation.
    
    Args:
        population (Population): The population we want to select from.
        
    Returns:
        Individual: selected individual.
    """
    # Step 1: Rank the individuals
    ranked_population = sorted(population, key=attrgetter('fitness'), reverse=(population.optim == 'min'))
    
    # Step 2: Calculate selection probabilities
    total_ranks = sum(range(1, len(ranked_population) + 1))
    rank_probabilities = [(rank + 1) / total_ranks for rank in range(len(ranked_population))]
    
    # Step 3: Perform selection based on these probabilities
    r = uniform(0, sum(rank_probabilities))
    position = 0
    for individual, probability in zip(ranked_population, rank_probabilities):
        position += probability
        if position > r:
            return individual
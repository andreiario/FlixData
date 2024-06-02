from random import sample, shuffle, randint
import random

# Random Swap Mutation
'''
This mutation operator randomly selects two positions within each route and swaps the cities at those positions.
It is a simple and effective mutation method that introduces diversity by rearranging the order of cities in the route.
'''
def random_swap_mutation(offspring):
    # Create a copy of the offspring to avoid modifying the original
    mutated_offspring = offspring.copy()
    # Iterate over each route in the offspring
    for i, route in enumerate(mutated_offspring):
        # Select two random indices within the route
        idx1, idx2 = sample(range(len(route)), 2)
        # Swap the elements at the selected indices
        route[idx1], route[idx2] = route[idx2], route[idx1]
    return mutated_offspring


# Shuffle Mutation
'''
The shuffle mutation randomly shuffles the order of cities within each route.
It is similar to random swap mutation but may result in different permutations within the same route.
'''
def shuffle_mutation(offspring):
    # Create a copy of the offspring to avoid modifying the original
    mutated_offspring = offspring.copy()
    # Shuffle each route in the offspring
    for i, route in enumerate(mutated_offspring):
        shuffle(route)
    return mutated_offspring


# Route Swap Mutation
'''
In route swap mutation, two random routes are selected, and two random cities, one from each route, are swapped.
This mutation method can explore different combinations of routes in the population.
'''
def route_swap_mutation(offspring):
    # Create a copy of the offspring to avoid modifying the original
    mutated_offspring = [route.copy() for route in offspring]

    # Iterate over each route
    for i, route1 in enumerate(mutated_offspring):
        
        # Select a random route to swap with
        route_idx2 = randint(0, len(offspring) - 1)
        route2 = mutated_offspring[route_idx2]

        # Select two distinct cities, one from each route
        city_idx1, city_idx2 = sample(range(len(route1)), 2)
        city1, city2 = route1[city_idx1], route2[city_idx2]

        # Ensure selected cities are not already present in the other route
        if city1 not in route2 and city2 not in route1:
            # Swap the cities between the routes
            mutated_offspring[i][city_idx1] = city2
            mutated_offspring[route_idx2][city_idx2] = city1

    return mutated_offspring


# Scramble Mutation
'''
Scramble mutation randomly selects a subset of cities within each route and shuffles their order.
It can disrupt the order of cities within a route, potentially leading to new and diverse solutions.

'''
def scramble_mutation(individual, mutation_rate=0.1):
    # Create a copy of the individual to avoid mutating the original
    mutated_individual = [sublist[:] for sublist in individual]

     # Loop over each sublist
    for sublist in mutated_individual:
        # Check if a mutation should occur based on the mutation rate
        if random.random() < mutation_rate:
            # Select a random start and end position for scrambling
            start = random.randint(0, len(sublist) - 1)
            end = random.randint(start, len(sublist) - 1)
            # Scramble the sublist within the selected range
            sublist[start:end + 1] = random.sample(sublist[start:end + 1], len(sublist[start:end + 1]))

    return mutated_individual

# Insertion Mutation
'''
Insertion mutation selects two random positions within each sublist and moves the element at one position to the other position.
It is another method to introduce small changes in the order of elements within each sublist.
'''
def insertion_mutation(individual, mutation_rate=0.1):
    # Create a copy of the individual to avoid mutating the original
    mutated_individual = [sublist[:] for sublist in individual]

    # Loop over each sublist
    for sublist in mutated_individual:
        if random.random() < mutation_rate:
            # Select two random positions for insertion
            pos1 = random.randint(0, len(sublist) - 1)
            pos2 = random.randint(0, len(sublist) - 1)
             # Remove an element from pos1 and insert it into pos2
            item = sublist.pop(pos1)
            sublist.insert(pos2, item)

    return mutated_individual

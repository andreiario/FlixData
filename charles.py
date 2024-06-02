from random import choice, random, shuffle
from operator import attrgetter
from copy import copy

# Defining Individual (representation + fitness):
class Individual:
    # we always initialize
    def __init__(self, representation=None, route_size=None, number_routes=None, valid_set=None, fuel_cities=None, distance_matrix=None):
        """
        Initializes an Individual object.

        Args:
            representation (list, optional): The route configuration of the individual. Defaults to None.
            route_size (int): The size of each route.
            number_routes (int): The number of routes.
            valid_set (list): List of valid cities.
            fuel_cities (list): List of fuel cities.
            distance_matrix (list of lists): Matrix containing distances between cities.
        """
        if representation is None:
            # Check if there are enough routes to cover all cities
            if number_routes * route_size < len(valid_set):
                raise ValueError('Not enough routes to cover all cities.')
            # Generate routes if representation is not provided
            self.representation = self.generate_routes(route_size, number_routes, valid_set, fuel_cities, distance_matrix)
        else:
            # Use the provided representation
            self.representation = representation
        # Calculate fitness for the individual
        self.fitness = self.get_fitness()

    def generate_routes(self, route_size, number_routes, valid_set, fuel_cities, distance_matrix):
        """
        Generates route configurations for the individual.

        Args:
            route_size (int): The size of each route.
            number_routes (int): The number of routes.
            valid_set (list): List of valid cities.
            fuel_cities (list): List of fuel cities.
            distance_matrix (list of lists): Matrix containing distances between cities.

        Returns:
            list of lists: The generated route configurations.
        """
        # Create copies of the valid_set and fuel_cities lists
        unused_cities = valid_set[:] # List containing all unused cities
        unused_city_fuel = fuel_cities.copy() # List containing unused fuel cities
        final_representation = [] # Initialize the final representation of routes

        # Generate the required number of routes
        for _ in range(number_routes):
            route = [] # Initialize a new route
            distance = 0 # Initialize distance as zero

            # Continue adding cities to the route until it reaches the specified size
            while len(route) < route_size: 

                 # If the route is empty, choose a city randomly
                if not route: 
                    city = choice(unused_cities)
                else:
                    last_city = route[-1] # Get the last added city
                    index_last_city = valid_set.index(last_city) # Get the index of the last city
                    # Find candidate cities that can be added to the route based on distance constraints
                    candidates = [city for city in unused_cities if distance + distance_matrix[index_last_city][valid_set.index(city)] <= 500]
                    
                    # If no candidate cities are found and there are fuel cities available
                    if not candidates and unused_city_fuel:
                        city = choice(unused_city_fuel) # Choose a fuel city
                    # If candidate cities are available
                    elif candidates:
                        city = choice(candidates) # Choose a candidate city
                    else:
                        city = choice(unused_cities) # Choose any city if no candidates are available
                route.append(city) # Add the chosen city to the route
            
                if city in unused_cities:
                    unused_cities.remove(city) # Remove the chosen city from the list of unused cities
                if city in unused_city_fuel:
                    unused_city_fuel.remove(city) # Remove the chosen city from the list of unused fuel cities
                    distance = 0 # Reset the distance to zero as the route refuels
                else:
                    if len(route) > 1: # Calculate distance only if there are at least two cities in the route
                        prev_city = route[-2] # Get the second-to-last city added to the route
                        index_prev_city = valid_set.index(prev_city) # Get the index of the second-to-last city
                        index_city = valid_set.index(city) # Get the index of the current city
                        distance += distance_matrix[index_prev_city][index_city] # Update the total distance for the route
            final_representation.append(route) # Add the completed route to the final representation list
        
        return final_representation # Return the generated routes

    # methods for the class
    def get_fitness(self): # Calculates the fitness score of the individual.
        raise NotImplementedError("You need to monkey patch the fitness function.")

    def __len__(self): # Returns the length of the representation.
        return len(self.representation)

    def __getitem__(self, position): # Returns the element at the specified position in the representation.
        return self.representation[position]

    def __setitem__(self, position, value): # Sets the element at the specified position in the representation to the given value.
        self.representation[position] = value

    def __repr__(self): # Returns a string representation of the individual.
        return f"Representation: {self.representation}; Fitness: {self.fitness}"


class Population:
    """
    Represents a population of individuals.

    Attributes:
        size (int): The size of the population.
        optim (str): The optimization type ('max' or 'min').
        individuals (list): List of Individual objects representing the population.
    """
    def __init__(self, size, optim, **kwargs):
        """
        Initializes a Population object.

        Args:
            size (int): The size of the population.
            optim (str): The optimization type ('max' or 'min').
            **kwargs: Additional keyword arguments.
        """
        # Initialize Population attributes
        self.size = size 
        self.optim = optim
        # Initialize a list of Individuals for the population
        self.individuals = [ 
            Individual(
                route_size=kwargs["route_size"], # Size of each route in the individual
                valid_set=kwargs["valid_set"], # List of valid cities
                number_routes=kwargs["number_routes"], # Number of routes per individual
                fuel_cities=kwargs["fuel_cities"], # List of fuel cities
                distance_matrix=kwargs["distance_matrix"] # Distance matrix between cities
            ) for _ in range(size) # Create 'size' number of individuals
        ]

    def evolve(self, gens, xo_prob, mut_prob, select, xo, mutate, elitism, fitness_sharing):
        """
        Evolves the population over a specified number of generations.

        Args:
            gens (int): The number of generations.
            xo_prob (float): The crossover probability.
            mut_prob (float): The mutation probability.
            select (function): The selection function.
            xo (function): The crossover function.
            mutate (function): The mutation function.
            elitism (bool): Whether to use elitism.
            fitness_sharing (bool): Whether to use fitness sharing.

        Returns:
            list: List of fitness scores for the best individual in each generation.
        """
        # Initialize an empty list to store fitness values of the best individuals in each generation
        fitnesses = []

        # Loop through generations
        for gen in range(gens):
            new_population = [] # Initialize an empty list for the new population of individuals

            # If elitism is enabled, select the best individual from the current population
            if elitism:
                elite = max(self.individuals, key=attrgetter('fitness')) if self.optim == 'max' else min(self.individuals, key=attrgetter('fitness'))

             # Populate the new population until it reaches the desired size
            while len(new_population) < self.size:
                # Select parents for crossover
                parent1, parent2 = select(self), select(self)
               
                # Crossover 
                if random() < xo_prob:
                    offspring1, offspring2 = xo(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1.representation, parent2.representation

                # Mutation 
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                # Create new individuals with the offspring representations
                new_population.append(Individual(representation=offspring1))
                if len(new_population) < self.size:
                    new_population.append(Individual(representation=offspring2))

            # Apply elitism if enabled
            if elitism:
                # Find the worst individual in the new population
                worst = min(new_population, key=attrgetter('fitness')) if self.optim == 'max' else max(new_population, key=attrgetter('fitness'))
                
                # Replace the worst individual with the elite if the elite is better
                if (elite.fitness > worst.fitness if self.optim == 'max' else elite.fitness < worst.fitness):
                    new_population.pop(new_population.index(worst))
                    new_population.append(elite)

            # Replace the current population with the new population
            self.individuals = new_population

            # Determine the best individual in the current generation based on optimization criteria
            best_individual = max(self, key=attrgetter('fitness')) if self.optim == 'max' else min(self, key=attrgetter('fitness'))
            print(f"Best individual of gen #{gen + 1}: {best_individual}")
            # Append the fitness of the best individual to the list of fitnesses
            fitnesses.append(best_individual.fitness)

            # Apply fitness sharing if enabled
            if fitness_sharing:
                self.individuals = self.apply_fitness_sharing(new_population)


        # Return the list of fitness values for each generation
        return fitnesses

    # Function to apply fitness sharing to a population
    def apply_fitness_sharing(self, population):
        
        def hamming_distance(route1, route2):
            return sum(el1 != el2 for el1, el2 in zip(route1, route2))

        def normalize_distances(distances, length):
            return [d / length for d in distances]

        def sharing_function(distance):
            return 1 - distance

        # Iterate over each individual in the population
        for i, ind1 in enumerate(population):
            distances = []
            for j, ind2 in enumerate(population):
                if i != j:
                    total_distance = 0
                    for route1, route2 in zip(ind1.representation, ind2.representation):
                        total_distance += hamming_distance(route1, route2)
                    distances.append(total_distance)
        
        # Normalize distances
        length = 24 # number of cities
        normalized_distances = normalize_distances(distances, length)
        
        # Calculate sharing coefficient
        sharing_coefficient = sum(sharing_function(d) for d in normalized_distances)
        
        if sharing_coefficient > 0:
            ind1.fitness = ind1.fitness / sharing_coefficient
        else:
            ind1.fitness += 1000   # Penalize individual if no sharing occurs

        return population

    # Define the length of the population (number of individuals)
    def __len__(self):
        return len(self.individuals)
    
    # Get an individual from the population by index
    def __getitem__(self, position):
        return self.individuals[position]

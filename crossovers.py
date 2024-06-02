import random
from random import randint

# OX CROSSOVER
"""
OX crossover randomly selects two crossover points.
Then it copies the segment between the crossover points from parent1 to child1 and from parent2 to child2.
After, it fills the remaining positions in the children with the cities from the other parent in the order they appear, starting from the position right after the second crossover point and wrapping around to the beginning if necessary.
To  mantain the route structure, we split the flattened offspring back into the original route structure of the parents.
"""

def order_crossover(parent1, parent2):
    def order_route(route1, route2): # Function that performs Order Crossover on individual routes."""
        size = len(route1)
        
        # Initialize empty children with None values
        child1 = [None] * size
        child2 = [None] * size

        # Choose two random crossover points
        cx_point1 = random.randint(0, size - 1)
        cx_point2 = random.randint(0, size - 1)

        # Ensure that cx_point1 is less than cx_point2 to clearly define a segment in the parent routes between these two points. 
        if cx_point1 > cx_point2:
            cx_point1, cx_point2 = cx_point2, cx_point1

        # Copy the selected slice from the first parent to the first child
        child1[cx_point1:cx_point2+1] = route1[cx_point1:cx_point2+1]
        child2[cx_point1:cx_point2+1] = route2[cx_point1:cx_point2+1]

        def fill_remaining(child, route, start, end): # Fill the remaining positions in the child with the cities from the other parent
            pos = (end + 1) % size # Start filling positions after the second crossover point
            for city in route:
                if city not in child:
                    while child[pos] is not None:
                        pos = (pos + 1) % size
                    child[pos] = city # Only add cities that are not already in the child

        # Fill the remaining positions in child1 and child2
        fill_remaining(child1, route2, cx_point1, cx_point2)
        fill_remaining(child2, route1, cx_point1, cx_point2)

        return child1, child2

    def flatten_routes(routes): # Function to flatten the route structure into a single list of cities.
        return [city for route in routes for city in route]

    def split_routes(flattened, original): # Function to split the flattened list back into the original route structure.
        split_points = [0] + [len(route) for route in original]
        split_points = [sum(split_points[:i+1]) for i in range(len(split_points))]
        return [flattened[split_points[i]:split_points[i+1]] for i in range(len(original))]

    def ensure_all_cities(child_routes, all_cities): # Function to ensure all cities are visited and no duplicates are present in the child routes.
        # Flatten the child routes
        flat_child = flatten_routes(child_routes)
        missing_cities = set(all_cities) - set(flat_child)
        duplicate_cities = [city for city in flat_child if flat_child.count(city) > 1]

        for duplicate in duplicate_cities:
            for i, route in enumerate(child_routes):
                if duplicate in route:
                    duplicate_index = route.index(duplicate)
                    if missing_cities:
                        route[duplicate_index] = missing_cities.pop()
                    break

        return child_routes

    # Flatten both parents
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)

    # Perform OX on the flattened parents
    flat_child1, flat_child2 = order_route(flat_parent1, flat_parent2)

    # Split the flat children back into routes
    child1 = split_routes(flat_child1, parent1)
    child2 = split_routes(flat_child2, parent2)

    # Ensure all cities are visited and no duplicates
    all_cities = flatten_routes(parent1)
    child1 = ensure_all_cities(child1, all_cities)
    child2 = ensure_all_cities(child2, all_cities)

    return child1, child2



# PMX CROSSOVER
"""
PMX randomly chooses two crossover points, ensuring the first point is less than the second.
Then, creates an offspring by copying segments between the crossover points from one parent to the other.
After, we fill in the remaining cities without duplicating any cities. 
For each position outside the copied segment, if the city is not already in the child, place it. If it is, follow the mapping to find its correct position.
PMX crossover fills any remaining positions with cities from the corresponding parent.
To retain the rout structure we Flatten both parents, perform PMX on the flattened lists, and then split the offspring back into the original route structure.
"""
from random import randint

import random

def pmx_crossover(parent1, parent2): # PMX crossover between two parents to produce two offspring.
    def pmx_route(route1, route2): #Perform PMX on individual routes.
        size = len(route1)
        
        # Choose two crossover points
        cx_point1 = random.randint(0, size - 1)
        cx_point2 = random.randint(0, size - 1)
        if cx_point1 > cx_point2: # Ensure cx_point1 is less than cx_point2 to clearly define a segment in the parent routes between these two points.
            cx_point1, cx_point2 = cx_point2, cx_point1
        
        # Create placeholders for offspring
        child1 = [-1] * size
        child2 = [-1] * size
        
        # Copy the segment between the crossover points from parent2 to child1 and from parent1 to child2
        child1[cx_point1:cx_point2] = route2[cx_point1:cx_point2]
        child2[cx_point1:cx_point2] = route1[cx_point1:cx_point2]
        
        # Fill the remaining positions with PMX logic
        def fill_remaining(child, parent_segment, start, end):
            for i in range(start, end):
                if parent_segment[i] not in child:
                    pos = i
                    while child[pos] != -1:
                        pos = parent_segment.index(child[pos])
                    child[pos] = parent_segment[i]
        
        # Fill the remaining positions for both children
        fill_remaining(child1, route1, cx_point1, cx_point2)
        fill_remaining(child2, route2, cx_point1, cx_point2)
        
        # Fill the remaining gaps in the children with the remaining cities from the respective parents
        def fill_gaps(child, parent):
            for i in range(size):
                if child[i] == -1:
                    child[i] = parent[i]
        
        fill_gaps(child1, route1)
        fill_gaps(child2, route2)
        
        return child1, child2
    
    def flatten_routes(routes): # Function to flatten the route structure into a single list of cities.
        return [city for route in routes for city in route]
    
    def split_routes(flattened, original): # Function to split the flattened list back into the original route structure.
        split_points = [0] + [len(route) for route in original]
        split_points = [sum(split_points[:i+1]) for i in range(len(split_points))]
        return [flattened[split_points[i]:split_points[i+1]] for i in range(len(original))]
    
    # Flatten both parents into single lists of cities
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)
    
    # PMX on the flattened parents
    flat_child1, flat_child2 = pmx_route(flat_parent1, flat_parent2)
    
    # Split the flat children back into routes the original route structure
    child1 = split_routes(flat_child1, parent1)
    child2 = split_routes(flat_child2, parent2)
    
    return child1, child2


# CX CROSSOVER (CYCLE)
"""
Cycle crossover identifies cycles between the two parents. 
A cycle is a sequence of indices where the city in parent1 at a given index appears in the same position in parent2.
Then, cx will alternate the cycles between the two parents. 
The first cycle’s cities are copied from parent1 to child1 and from parent2 to child2. The next cycle’s cities are copied from parent2 to child1 and from parent1 to child2, and so on.
To restore the Route Structure we flattened both parents, perform CX on the flattened lists, and then split the offspring back into the original route structure.
"""

def cycle_crossover(parent1, parent2): # Cycle Crossover (CX) between two parents to produce two offspring.
    def cycle_route(route1, route2): # Perform Cycle Crossover (CX) on individual routes.
        size = len(route1) # Get the size of the route
        
        # Create placeholders for offspring initialized to -1
        child1 = [-1] * size
        child2 = [-1] * size
        
        cycle = 0 # Initialize cycle counter
        indices = list(range(size)) # Create a list of indices from 0 to size-1 to keep track of the positions that have not yet been processed
        
        # Process cycles until all indices are handled
        while indices: # Continue until all indices are processed
            idx = indices[0]
            while True: # Assign cities to children based on current cycle
                child1[idx] = route1[idx] if cycle % 2 == 0 else route2[idx]
                child2[idx] = route2[idx] if cycle % 2 == 0 else route1[idx]
                
                idx = route1.index(route2[idx]) # Move to the index in the other parent
                
                if child1[idx] != -1: # If we return to the start of the cycle, break the loop.
                    break
            
            cycle += 1 # Move to the next cycle
            indices = [i for i in indices if child1[i] == -1] # Update indices to exclude processed positions
        
        return child1, child2
    
    def flatten_routes(routes): # Function to flatten the route structure into a single list of cities.
        return [city for route in routes for city in route]
    
    def split_routes(flattened, original): # Function to split the flattened list back into the original route structure.
        split_points = [0] + [len(route) for route in original] # Calculate the split points
        split_points = [sum(split_points[:i+1]) for i in range(len(split_points))] # Cumulative sum of split points
        return [flattened[split_points[i]:split_points[i+1]] for i in range(len(original))] # Split the flattened list back into the original structure of routes
    
    # Flatten both parents into single lists of cities
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)
    
    # CX on the flattened parents
    flat_child1, flat_child2 = cycle_route(flat_parent1, flat_parent2)
    
    # Split the flat children back into routes
    child1 = split_routes(flat_child1, parent1)
    child2 = split_routes(flat_child2, parent2)
    
    return child1, child2



###### Other important Functions

def check_no_repeated_cities(offspring):
    for i, route in enumerate(offspring):
        city_count = {}
        for city in route:
            if city is not None:
                city_count[city] = city_count.get(city, 0) + 1
                if city_count[city] > 1:
                    return False
    return True

def is_all_cities_covered(offspring):
    all_cities = {city for route in offspring for city in route}
    return len(all_cities) == 24  

def fill_offspring(offspring, parent):
    all_cities = set(city for route in parent for city in route)
    for i, route in enumerate(offspring):
        if None in route:
            filled_cities = set(route[:route.index(None)])  # Exclude retained cities
            uncovered_cities = [city for city in parent[i] if city not in filled_cities]
            #print("Uncovered cities for route", i + 1, ":", uncovered_cities)
            for j in range(route.index(None), len(route)):
                if uncovered_cities:
                    next_city = None
                    if j < len(route) - 1 and route[j - 1] in parent[i]:
                        next_city_idx = parent[i].index(route[j - 1]) + 1
                        if next_city_idx < len(parent[i]):
                            next_city = parent[i][next_city_idx]
                    if next_city and next_city in uncovered_cities:
                        route[j] = next_city
                        uncovered_cities.remove(next_city)
                    else:
                        route[j] = uncovered_cities.pop(0)
                else:
                    remaining_cities = list(all_cities - filled_cities)
                    random.shuffle(remaining_cities)  # Shuffle to introduce randomness
                    route[j] = remaining_cities.pop(0)
                
                #print("Route", i + 1, "after filling:", route)
            #print("Route", i + 1, "completed.")
    return offspring


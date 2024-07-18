import pandas as pd
import numpy as np
import random
from math import radians, sin, cos, sqrt

# Function to calculate Haversine distance between two points given their latitude and longitude
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Radius of the Earth in kilometers

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * np.arcsin(sqrt(a))

    distance = R * c
    return distance

# Function to extract customer IDs excluding the depot
def extract_customer_ids(customers_df, depot_id):
    customer_ids = customers_df['CustomerId'].tolist()
    customer_ids.remove(depot_id)  # Remove the depot from customer IDs
    return customer_ids

# Function to generate a random population of routes
def generate_initial_population(customer_ids, population_size):
    population = [random.sample(customer_ids, len(customer_ids)) for _ in range(population_size)]
    return population

# Function to format a route as a string
def format_route(route, depot_id):
    return f'{depot_id} -> ' + ' -> '.join(route) + f' -> {depot_id}'

# Function to calculate the fitness of a route
def calculate_fitness(route, customers_df, depot_id):
    total_distance = 0.0
    depot = customers_df[customers_df['CustomerId'] == depot_id].iloc[0]

    # Calculate distance from depot to first customer
    prev_customer = depot
    for customer_id in route:
        customer = customers_df[customers_df['CustomerId'] == customer_id].iloc[0]
        total_distance += haversine(prev_customer['Longitude'], prev_customer['Latitude'],
                                    customer['Longitude'], customer['Latitude'])
        prev_customer = customer

    # Add distance from last customer back to depot
    total_distance += haversine(prev_customer['Longitude'], prev_customer['Latitude'],
                                depot['Longitude'], depot['Latitude'])

    fitness = 1 / total_distance  # Inverse of total distance as fitness
    return total_distance, fitness

# Genetic Algorithm Functions

# Function to perform roulette wheel selection
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    r = random.uniform(0, total_fitness)
    current_sum = 0
    for i, fitness in enumerate(fitness_scores):
        current_sum += fitness
        if current_sum > r:
            return population[i]
    return population[-1]

# Function to perform single-point crossover
def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

# Function for mutation
def mutate(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

# Main function to run the genetic algorithm
def genetic_algorithm(customers_df, depot_id, population_size, generations):
    customer_ids = extract_customer_ids(customers_df, depot_id)
    population = generate_initial_population(customer_ids, population_size)
    best_route = None
    best_fitness = -1
    best_distance = float('inf')

    for gen in range(generations):
        # Evaluate fitness of each route in the population
        fitness_scores = []
        for route in population:
            route_with_depot = [depot_id] + route + [depot_id]
            total_distance, fitness = calculate_fitness(route, customers_df, depot_id)
            fitness_scores.append(fitness)
            # Track the best route found so far
            if fitness > best_fitness:
                best_fitness = fitness
                best_distance = total_distance
                best_route = route

        # Perform selection, crossover, and mutation
        new_population = []
        for _ in range(population_size // 2):
            # Selection
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            # Crossover
            child1, child2 = single_point_crossover(parent1, parent2)

            # Mutation
            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population

    # Return the best route with depot at both start and end, along with its distance and fitness
    best_route_with_depot = [depot_id] + best_route + [depot_id]
    return format_route(best_route, depot_id), best_distance, best_fitness

def calculate_optimal_route(df, depot_id):
    population_size = 10
    generations = 100
    best_route, best_distance, best_fitness = genetic_algorithm(df, depot_id, population_size, generations)
    return best_route, best_distance, best_fitness



# import pandas as pd
# import numpy as np
# import random
# from math import radians, sin, cos, sqrt

# # Function to calculate Haversine distance between two points given their latitude and longitude
# def haversine(lon1, lat1, lon2, lat2):
#     R = 6371  # Radius of the Earth in kilometers

#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

#     dlon = lon2 - lon1
#     dlat = lon2 - lon1

#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * np.arcsin(sqrt(a))

#     distance = R * c
#     return distance

# # Function to extract customer IDs excluding the depot
# def extract_customer_ids(customers_df, depot_id):
#     customer_ids = customers_df['CustomerId'].tolist()
#     customer_ids.remove(depot_id)  # Remove the depot from customer IDs
#     return customer_ids

# # Function to generate a random population of routes
# def generate_initial_population(customer_ids, population_size):
#     population = [random.sample(customer_ids, len(customer_ids)) for _ in range(population_size)]
#     return population

# # Function to format a route as a string
# def format_route(route, depot_id):
#     return f'{depot_id} -> ' + ' -> '.join(route) + f' -> {depot_id}'

# # Function to calculate the fitness of a route
# def calculate_fitness(route, customers_df, depot_id):
#     total_distance = 0.0
#     depot = customers_df[customers_df['CustomerId'] == depot_id].iloc[0]

#     # Calculate distance from depot to first customer
#     prev_customer = depot
#     for customer_id in route:
#         customer = customers_df[customers_df['CustomerId'] == customer_id].iloc[0]
#         total_distance += haversine(prev_customer['Longitude'], prev_customer['Latitude'],
#                                     customer['Longitude'], customer['Latitude'])
#         prev_customer = customer

#     # Add distance from last customer back to depot
#     total_distance += haversine(prev_customer['Longitude'], prev_customer['Latitude'],
#                                 depot['Longitude'], depot['Latitude'])

#     fitness = 1 / total_distance  # Inverse of total distance as fitness
#     return total_distance, fitness

# # Genetic Algorithm Functions

# # Function to perform roulette wheel selection
# def roulette_wheel_selection(population, fitness_scores):
#     total_fitness = sum(fitness_scores)
#     r = random.uniform(0, total_fitness)
#     current_sum = 0
#     for i, fitness in enumerate(fitness_scores):
#         current_sum += fitness
#         if current_sum > r:
#             return population[i]
#     return population[-1]

# # Function to perform single-point crossover
# def single_point_crossover(parent1, parent2):
#     crossover_point = random.randint(1, len(parent1) - 1)
#     child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
#     child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
#     return child1, child2

# # Function for mutation
# def mutate(route):
#     idx1, idx2 = random.sample(range(len(route)), 2)
#     route[idx1], route[idx2] = route[idx2], route[idx1]
#     return route

# def genetic_algorithm(customers_df, depot_id, population_size, generations):
#     customer_ids = extract_customer_ids(customers_df, depot_id)
#     population = generate_initial_population(customer_ids, population_size)
#     best_route = None
#     best_fitness = -1
#     best_distance = float('inf')

#     for gen in range(generations):
#         # Evaluate fitness of each route in the population
#         fitness_scores = []
#         for route in population:
#             total_distance, fitness = calculate_fitness(route, customers_df, depot_id)
#             fitness_scores.append(fitness)
#             # Track the best route found so far
#             if fitness > best_fitness:
#                 best_fitness = fitness
#                 best_distance = total_distance
#                 best_route = route

#         # Perform selection, crossover, and mutation
#         new_population = []
#         for _ in range(population_size // 2):
#             # Selection
#             parent1 = roulette_wheel_selection(population, fitness_scores)
#             parent2 = roulette_wheel_selection(population, fitness_scores)

#             # Crossover
#             child1, child2 = single_point_crossover(parent1, parent2)

#             # Mutation
#             child1 = mutate(child1)
#             child2 = mutate(child2)

#             new_population.append(child1)
#             new_population.append(child2)

#         population = new_population

#     # Return the best route with depot at both start and end, along with its distance and fitness
#     best_route_with_depot = [depot_id] + best_route + [depot_id]
    
#     # Get coordinates and names of the route
#     route_coords = []
#     route_names = []
#     for customer_id in best_route_with_depot:
#         customer = customers_df[customers_df['CustomerId'] == customer_id].iloc[0]
#         route_coords.append((customer['Latitude'], customer['Longitude']))
#         route_names.append(customer['CustomerId'])
    
#     return format_route(best_route, depot_id), best_distance, best_fitness, route_coords, route_names
# def calculate_optimal_route(df, depot_id):
#     population_size = 10
#     generations = 100
#     best_route, best_distance, best_fitness, route_coords, route_names = genetic_algorithm(df, depot_id, population_size, generations)
#     return best_route, best_distance, best_fitness, route_coords, route_names

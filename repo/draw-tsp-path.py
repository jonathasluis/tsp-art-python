"""Modified code from https://developers.google.com/optimization/routing/tsp#or-tools """
# Copyright Matthew Mack (c) 2020 under CC-BY 4.0: https://creativecommons.org/licenses/by/4.0/

from __future__ import print_function
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from PIL import Image, ImageDraw
import os
import sys
import algGenetico
import copy


# Change these file names to the relevant files.
points = sys.argv[1]
ORIGINAL_IMAGE = "images/logo.jpg"
IMAGE_TSP = "images/logo-"+points+"-stipple.tsp"

# Cria o modelo com as coordenadas
def create_data_model():
    """Stores the data for the problem."""
    # Extracts coordinates from IMAGE_TSP and puts them into an array
    list_of_nodes = []
    with open(IMAGE_TSP) as f:
        for _ in range(6):
            next(f)
        for line in f:
            i,x,y = line.split()
            list_of_nodes.append((int(float(x)),int(float(y))))
    data = {}
    # Locations in block units
    data['locations'] = list_of_nodes # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

# Calcula a distancia euclidiana entre os pontos
def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances

# ortools
def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)

# ortools
def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
      index = routing.Start(route_nbr)
      route = [manager.IndexToNode(index)]
      while not routing.IsEnd(index):
        index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
      routes.append(route)
    return routes[0]

# desenha as rotas, gera a arte
def draw_routes(nodes, path):
    """Takes a set of nodes and a path, and outputs an image of the drawn TSP path"""
    tsp_path = []
    for location in path:
        tsp_path.append(nodes[int(location)])

    original_image = Image.open(ORIGINAL_IMAGE)
    width, height = original_image.size

    tsp_image = Image.new("RGBA",(width,height),color='white')
    tsp_image_draw = ImageDraw.Draw(tsp_image)
    #tsp_image_draw.point(tsp_path,fill='black')
    tsp_image_draw.line(tsp_path,fill='black',width=1)
    tsp_image = tsp_image.transpose(Image.FLIP_TOP_BOTTOM)
    FINAL_IMAGE = IMAGE_TSP.replace("-stipple.tsp","-tsp.png")
    tsp_image.save(FINAL_IMAGE)
    print("TSP solution has been drawn and can be viewed at", FINAL_IMAGE)

# Vizinho mais proximo
def nn_tsp(distance):
    # ponto inicial
    tour = [0] 
    
    # enquanto o tamanho do caminho for menor que a quantidade de pontos
    while len(tour) < int(points):
        
        A = tour[-1]  # Ultima posiçao de tour
        
        C = min(distance[A], key=distance[A].get) # Na matriz de distancia, calcula o ponto mais proximo de A
        
        # Enquanto C estiver em tour, remove-se C da matriz e calcula o ponto mais proximo
        while C in tour:
            del distance[A][C]
            C = min(distance[A], key=distance[A].get)

        #print(C)
        tour.append(C) # Adiciona o ponto mais proximo no caminho
    
    tour.append(0) # adiciona o ponto inicial para fechar o ciclo
    return tour

def main():

    op = int(sys.argv[2])

    """Entry point of the program."""
    # Instantiate the data problem.
    print("Step 1/5: Initialising variables")
    data = create_data_model()

    # Create the routing index manager.
    if op == 1:
        manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

    print("Step 2/5: Computing distance matrix")
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    if op == 1:
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Setting first solution heuristic.
        print("Step 3/5: Setting an initial solution")
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        print("Step 4/5: Solving")
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            #print_solution(manager, routing, solution)
            print("Step 5/5: Drawing the solution")
            routes = get_routes(solution, routing, manager)
            draw_routes(data['locations'],routes)
        else:
            print("A solution couldn't be found :(")

    if op == 2:
        print("Step 3/4: Solving")
        routes = nn_tsp(distance_matrix)

        print("Step 4/4: Drawing the solution")
        draw_routes(data['locations'],routes)

    if op == 3:
        print("Step 3/4: Solving")

        rotaBase = nn_tsp(copy.deepcopy( distance_matrix))
        ag = algGenetico.AG(int(points) ,50,distance_matrix,rotaBase)

        routes = ag.gerarCaminho()
        print("Step 4/4: Drawing the solution")
        draw_routes(data['locations'],routes)

if __name__ == '__main__':
    main()

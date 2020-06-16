import sys
import math
import numpy as np
import matplotlib.pyplot as plt 

from common import print_tour, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

#Calculate the total length of a path
def path_length(tour, dist):
    value = 0
    for i in range(len(tour)-1):
        value += dist[tour[i]][tour[i+1]]
    value += dist[tour[0]][tour[-1]]
    return value

#determine if two line segments have intersections
def intersection_det(point1, point2, point3, point4):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x3 = point3[0]
    y3 = point3[1]
    x4 = point4[0]
    y4 = point4[1]
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if den != 0:
        x = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))/den
        y = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4))/den
        x_range_1 = sorted([x1, x2])
        x_range_2 = sorted([x3, x4])
        y_range_1 = sorted([y1, y2])
        y_range_2 = sorted([y3, y4])
        if (x_range_1[0]<=x<=x_range_1[1] and y_range_1[0]<=y<=y_range_1[1]) and (x_range_2[0]<=x<=x_range_2[1] and y_range_2[0]<=y<=y_range_2[1]):
            return True
    return False

def solve(cities):
    N = len(cities)

    #Construct the distance matrix
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    #Construct the random initial path using greedy search
    #current_city = np.int(np.ceil(np.random.rand()*(N-1)))
    current_city = 0
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    current_length = path_length(tour,dist)
    best_length = current_length


    #Apply SA algorithm -> an algorithm depends on "random number" so the result should look different each time you run it
    alpha = 0.999 #annealing rate
    initial_t = 7  #initial temperature
    final_t = 1 #final teperature
    iteration = 50000

    current_path = tour.copy()
    best_path = tour.copy()
    visualize = []

    while initial_t > final_t:
        print(initial_t)
        print(best_length)
        for i in range(iteration):
            random_number = np.random.rand()
            #Generate two different random numbers
            while True:
                pos1 = np.int(np.ceil(np.random.rand()*(N-1)))
                pos2 = np.int(np.ceil(np.random.rand()*(N-1)))
                if pos1 != pos2:
                    break
            #Three ways to choose from by chance
            #First one
            #Swap two elements
            if random_number < 0.3:
                tour[pos1], tour[pos2] = tour[pos2], tour[pos1]
            #Second one
            #Reverse the vertex between two random positions in the tour list
            elif 0.3 <= random_number < 0.6:
                tour[pos1:pos2] = reversed(tour[pos1:pos2])
            #Third one, insert pos1 after pos2
            else:
                tour.remove(tour[tour.index(pos1)])
                tour.insert(tour.index(pos2)+1, pos1)

            #calculate new length
            temp_length = path_length(tour,dist)
            #if the new length is smaller than the current length, update
            if temp_length < current_length:
                current_length = temp_length
                current_path = tour.copy()
                # if it's better than the best_length, update
                if temp_length < best_length:
                    best_length = temp_length
                    best_path = tour.copy()
            else:
                #update by chance when new length is larger than the current length (possibility becomes smaller when t decreases)
                if np.random.rand() < np.exp(-(temp_length-current_length)/initial_t):
                    current_length = temp_length
                    current_path = tour.copy()
                #no update
                else:
                    tour = current_path.copy()
        #anneal
        initial_t *= alpha
        visualize.append(best_length)

    #to see how path length decreases
    plt.plot(np.array(visualize))
    plt.show()
    print(best_length)
    tour = best_path.copy()

    #if there are intersections, flip them
    while True:
        no_intersection = True
        for i in range(N):
            for j in range(i+2, N-1):
                det = intersection_det(cities[tour[i]], cities[tour[i+1]], cities[tour[j]], cities[tour[j+1]])
                if det and tour[i]!=tour[j+1]:
                    no_intersection = False
                    #exchange the position of the ending point of line segment 1 and the starting point of line segment 2
                    tour[i+1], tour[j] = tour[j], tour[i+1]
                    #reverse the order for points that are between ending point of line segment 1 and the starting point of line segment 2 so that a cycle can be formed
                    tour[i+2:j] = reversed(tour[i+2:j])
                    break
        if no_intersection == True:
            break

    #calculate cost, update if the cost becomes smaller
    if path_length(tour,dist) < best_length:
        best_path = tour.copy()

    return best_path


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

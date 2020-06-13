#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

#Determine if two line segments have intersection point
#First determine if two lines have intersection point, then determine if the intersection point is on the line segment
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

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    minn_path = []
    minn_cost = float('inf')
    
    #greedy search, check every starting point
    for i in range(N):
        print(i)
        current_cost = 0
        current_city = i
        unvisited_cities = set(range(0, N))
        unvisited_cities.remove(current_city)
        tour = [current_city]

        while unvisited_cities:
            next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city
        tour.append(tour[0])

        #check if there are lines that intersect with each other
        while True:
            no_intersection = True
            for i in range(N):
                for j in range(i+2, N):
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

        #calculate cost, update if the cost becomes smaller for current starting vertex
        for i in range(N-1):
            current_cost += dist[tour[i]][tour[i+1]]
        current_cost += dist[tour[-1]][tour[0]]

        if current_cost < minn_cost:
            minn_cost = current_cost
            minn_path = tour.copy()

    return minn_path
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

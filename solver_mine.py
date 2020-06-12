#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    minn_path = []
    minn_cost = float('inf')
    
    for i in range(N):
        print(i)
        current_cost = 0
        current_city = i
        unvisited_cities = set(range(0, N))
        unvisited_cities.remove(current_city)
        tour = [current_city]

        while unvisited_cities:
            next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
            current_cost += dist[current_city][next_city]
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city

        if current_cost < minn_cost:
            minn_cost = current_cost
            minn_path = tour.copy()
    return minn_path
    


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

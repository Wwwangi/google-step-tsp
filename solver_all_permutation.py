#Only valid for challenge 0 and 1 due to running time (time complexity)

import sys
import math
import itertools

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    
    permutation = [x for x in range(N)]
    minn_path = []
    minn_cost = float('inf')
    
    #iterate through all possible paths
    for perm in itertools.permutations(permutation,N):
        list_perm = list(perm)
        current_cost = 0

        #Calculate the total cost for one path
        for i in range(N-1):
            current_cost += dist[list_perm[i]][list_perm[i+1]]
        current_cost += dist[list_perm[-1]][list_perm[0]]

        #if smaller cost found, update
        if current_cost < minn_cost:
            print(perm)
            minn_cost = current_cost
            minn_path = list_perm.copy()
            print(minn_cost)
    return minn_path
    


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

#only work for challenge 0 1 2

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)
    tour = []

    #Construct the N*N distance table, i.e. dist[i][j] is the distance cost from city i to city j
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    #Construct the dp table, number of rows = city number, number of columns = 2^(city number -1)
    dp_table = [[0] * (2**(N-1)) for _ in range(N)]
    
    #initialze the dp_table, dp_table[i][0] means the distance from city i to the starting city 0
    for i in range(1,N):
        dp_table[i][0] = dist[i][0]

    #loop through dp_table columns (from 1 to 2^(N-1)) because the cost for set i that has more vertex to pass should depend on the cost for set i that has less vertex to pass
    for i in range(1, 2**(N-1)):
        #loop through dp_table rows (from 1 to N)
        #Goal: To check if the city j is in the set i. If not, we can update dp[j][i]
        for j in range(1, N):
            # e.g. if we want to check if city 4 is in set i, then we left shift 3 bits for 1 which results in 1000, and do & operation with binary representation for set i. If it's 0, it means city 4 is not in set i
            if not (1 << (j-1)) & i :
                min_cost = float('inf')
                #loop through city 1 to N again.
                #Goal: to compare the costs for different path
                for k in range(1, N):
                    #Ensure that city k is in the set i. Path: j->k->...->0
                    if (1 << (k-1)) & i:
                        #remove k from set i
                        temp = i - (1 << (k-1))
                        current_cost = dist[j][k] + dp_table[k][temp]
                        if current_cost < min_cost:
                            min_cost = current_cost
                            dp_table[j][i] = min_cost
    
    #To find the final cost
    min_cost = float('inf')
    temp_city = 0
    #Remove one vertex each time and update the cost if it becomes smaller
    for i in range(1, N):
        #The "path" contains all vertex except for the removed one i.e. departure city -> removed city -> rest city -> departure city
        path = (1 << (N-1)) - 1 - (1 << (i-1))
        if dist[0][i] + dp_table[i][path] < min_cost:
            min_cost = dist[0][i] + dp_table[i][path]
            temp_city = i
    dp_table[0][-1]  = min_cost
    tour.append(temp_city)

    #back tracking to find the optimal path
    unvisited = set([x for x in range(1,N)])
    unvisited.remove(temp_city)
    while unvisited:
        #calculate the binary representation of current unvisited set
        temp = 0
        for node in unvisited:
            temp += (1 << (node - 1))
        #check which vertex is the previous vertex
        for node in unvisited:
            path = temp - (1 << (node - 1))
            if dist[temp_city][node] + dp_table[node][path] == dp_table[temp_city][temp]:
                tour.append(node)
                temp_city = node
                unvisited.remove(node)
                break
    tour.append(0)

    '''print the fully updated dp_table
    for i in range(len(dp_table)):
        print(dp_table[i])
    '''

    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

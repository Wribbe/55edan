import sys
import re
import numpy as np

def main(args):
    print("loading matrix data ...")
    N, adjacency_matrix = load_data(args[0])

    print("creating HD ...")
    HD = create_HD(adjacency_matrix,N)
    HD = np.array(HD)

    print("creating P ...")
    P = create_P(HD, N)

    print("counting steps until stable ...")
    count, newP = nsteps(P, N)

    print("step count=", count)
    print(newP)
    return 0

def print_row_sums(matrix, N):
    for row in range(N):
        row_sum = 0
        for col in range(N):
            row_sum += matrix[row][col]
        print("row_sum=", row_sum)

def nsteps(P,N):
    count = 1
    lastP = P
    newP = np.dot(P,P)
    current_diff = diff(newP,lastP,N)

    while current_diff > 0.005:
        print("current_diff=", current_diff)
        lastP = newP
        newP = np.dot(P,newP)
        count += 1
        current_diff = diff(newP,lastP,N)

    return count,newP

def diff(P,P2,N):
    max_dif = 0
    for row in range(N):
        for col in range(N):
            current = abs(P[row][col]-P2[row][col])
            max_dif = max(max_dif,current)
    return max_dif

def create_P(HD, N):
    alpha = 85/100.0
    ones = np.array([np.ones(N) for _ in range(N)])
    P = alpha * HD + ((1-alpha)/N)*ones
    return P

def create_HD(adjacency_matrix,N):
    HD = [[0 for j in range(N)] for i in range(N)]
    for row in range(N):
        deg = degree(adjacency_matrix,row, N)
        for col in range(N):
            if  deg != 0:
                HD[row][col] = adjacency_matrix[row][col] / float(deg)
            else:
                HD[row][col] = 1.0/N
    return HD

def degree(adjacency_matrix, vertex, N):
    total = 0
    for col in range(N):
        total += adjacency_matrix[vertex][col]
    return total

def load_data(filename):
    print(filename)
    #try:
    if 0 == 0:
        with open(filename, 'r') as fp:
            lines = [line.strip() for line in fp.readlines()]
            N = int(lines.pop(0))
            adjacency_matrix = [[0 for j in range(N)] for i in range(N)]
            nodes = []
            for line in lines:
                nodes = [n for n in line.split('\t') if n != '\t']
                i = 0
                while i < len(nodes):
                    adjacency_matrix[int(nodes[i])][int(nodes[i+1])]+=1
                    i+=2
            return [N, adjacency_matrix]
   # except FileNotFoundError:
    #    return []

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

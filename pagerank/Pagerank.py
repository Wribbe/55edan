import sys
import random

def main(args):
    current_node = 0
    iterations = int(args[1])
    N, edges = load_data(args[0])
    visit_counter = [0]*N
    print(edges)
    for i in range(0,iterations):
        current_node = get_next_node(edges,N,current_node)
        visit_counter[current_node] += 1
        print(current_node)
    for v in range(0,len(visit_counter)):
        print("Frequency {}: {}".format(v,float(visit_counter[v])/float(iterations)))

def load_data(filename):
    try:
        with open(filename, 'r') as fp:
            lines = [line.strip() for line in fp.readlines()]
            N = int(lines.pop(0))
            edges = [[] for _ in range(N)]
            for string in lines:
                nodes = string.split(' ')
                while '' in nodes:
                    nodes.remove('')
                i = 0
                while i < len(nodes):
                    edges[int(nodes[i])] +=[int(nodes[i+1])]
                    i+=2
            #Edges[k] is a list off all nodes that node k has an outgoing edge to.
            #Several edges to the same nodes are allowed.
            return [N, edges]
    except FileNotFoundError:
        return []

def get_next_node(edges,N,index):
    if random.randint(1,100) > 85 or len(edges[index]) == 0:
        print("picking random")
        return random.randint(0,N-1)
    else:
        r = random.randint(0,len(edges[index])-1)
        return edges[index][r]

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

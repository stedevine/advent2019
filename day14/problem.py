def problem1(input_file):
    graph = {}
    with open(input_file) as file:
        for line in file:
            key = line.split('=>')[0].split(', ')
            key = list(map(lambda x: split_key(x), key))
            count, element = line.split('=>')[1].strip().split(' ')
            graph[(int(count), element)] = key
    print(graph)
    return graph

def make_substitutes(graph):
    formula = ''
    for k in graph:
        if k[1] == 'FUEL':
            formula = graph[k]

    # substitute E

    #f = formula.split

    print(formula)


def split_key(key):
    n = key.split(' ')
    return (int(n[0]),n[1])

graph = problem1('./input1.txt')
make_substitutes(graph)

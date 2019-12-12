def get_layers(input, width, height):
    layers = []
    # total number of digits/layer = width * height
    input = list(input)
    layer_size = width * height
    generator = (digit for digit in input)
    for i in range(0, int(len(input) / layer_size)):
        layers.append(list(next(generator) for _ in range(layer_size)))
    return layers

# Find the layer with the smallest count of zeros
def find_min_zeros(layers, width, height):
    result = None
    # max possible value is width * height
    min_count = (width * height) + 1
    for layer in layers:
        count = len(list(filter(lambda x: x == '0', layer)))
        if (count < min_count):
            result = layer
            min_count = count
    return result

def one_by_two(input,width,height):
    layers = get_layers(input, width, height)
    #print(layers)
    zero_layer = find_min_zeros(layers, width, height)
    one_count = len(list(filter(lambda x: x == '1', zero_layer)))
    two_count = len(list(filter(lambda x: x == '2', zero_layer)))
    return one_count * two_count

input = '003456781012'
print(one_by_two(input,3,2))

with open('./input.txt') as file:
    puzzle = file.read().strip()
    print(one_by_two(puzzle,25,6))

def get_layers(input, width, height):
    layers = []
    # total number of digits/layer = width * height
    input = list(map(lambda a: int(a), input))
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
        count = len(list(filter(lambda x: x == 0, layer)))
        if (count < min_count):
            result = layer
            min_count = count
    return result

def one_by_two(input,width,height):
    layers = get_layers(input, width, height)
    zero_layer = find_min_zeros(layers, width, height)
    one_count = len(list(filter(lambda x: x == 1, zero_layer)))
    two_count = len(list(filter(lambda x: x == 2, zero_layer)))
    return one_count * two_count

def get_image(input, width, height):
    layers = get_layers(input, width, height)

    # for each index in the output_layer
    # get the first non-transparent pixel from the layers
    index = 0
    layer_size = width * height
    output_layer = [None] * layer_size
    for index in range(0, layer_size):
        for layer in layers:
            # get the first non-transparent pixel from the layers
            if (layer[index] == 0 or layer[index] == 1):
                # make the output clearer
                if (layer[index] == 1):
                    output_layer[index] = 'x'
                else:
                    output_layer[index] = ' '
                break

    result = []
    gen = (digit for digit in output_layer)
    for i in range(0, int(len(output_layer) / width)):
        result.append(list(next(gen) for _ in range(width)))

    # print out the result
    for line in result:
        print(''.join(str(element) for element in line))

    return None


input = '003456781012'
print('test 1 {} '.format(one_by_two(input,3,2)))

input = '0222112222120000'
get_image(input,2,2)

with open('./input.txt') as file:
    puzzle = file.read().strip()
    print(one_by_two(puzzle,25,6))
    print()
    get_image(puzzle,25,6)

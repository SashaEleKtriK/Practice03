import json
from copy import copy

from PIL import ImageDraw, Image, ImageFont


def read_config():
    with open('config.json', 'r') as j:
        json_data = json.load(j)
        return json_data


def save_config(config):
    with open('config.json', 'w') as j:
        json.dump(config, j)


def generate_field_empty(size):
    field = []
    for i in range(0, size):
        raw = []
        for k in range(0, size):
            raw.append(0)
        field.append(raw)
    return field


def load_field(size, alive_cells):
    field = generate_field_empty(size)
    for cell in alive_cells:
        field[cell[0]][cell[1]] = cell[2]
    return field


def step(field):

    new_field = generate_field_empty(len(field))
    for i in range(0, len(new_field)):
        for k in range(0, len(new_field)):
            new_field[i][k] = field[i][k]
            n_count = neighbours_count(i, k, field)
            if n_count == 3 and field[i][k] == 0:
                new_field[i][k] = 1
            elif 2 <= n_count <= 3 and not (field[i][k] == 0):
                new_field[i][k] += 1
            else:
                new_field[i][k] = 0

    return new_field


def neighbours_count(x, y, field):
    n_count = 0
    try:
        for xx in range(x - 1, x + 2):
            for yy in range(y - 1, y + 2):
                if not (field[xx][yy] == 0):
                    if not(xx == x) or not(yy == y):
                        n_count += 1

    except IndexError:
        n_count = 0

    return n_count

def get_alive_list(field):
    alive_cells = []
    for i in range(0, len(field)):
        for k in range(0, len(field)):
            if not(field[i][k] == 0):
                alive_cells.append([i, k, field[i][k]])
    return alive_cells


def print_img(field, color):

    img = Image.new('RGB', (len(field) * 100, len(field) * 100), 'White')
    font = ImageFont.truetype('arial.ttf', size=18)
    for i in range(0, len(field)):
        for k in range(0, len(field)):
            if not (field[i][k] == 0):
                idraw = ImageDraw.Draw(img)

                idraw.rectangle((k*100, i*100, k*100+100,  i*100+100), fill=f'{color}')
                idraw.text((k*100 + 10, i*100 + 10), f'Age {field[i][k]}', font=font)

    for j in range(0, len(field)):
        idraw = ImageDraw.Draw(img)
        idraw.line(((0, 100 * j), (10000, 100 * j)), 'black', 2)
        idraw.line(((100 * j, 0), (100 * j, 10000)), 'black', 2)

    img.save('Test.png')
    img = Image.open('Test.png')
    img.show()



if __name__ == '__main__':
    j_data = read_config()
    steps = j_data['steps']
    a_cells = j_data['starting cells']
    my_size = j_data['size']
    color = j_data['color']
    my_field = load_field(my_size, a_cells)
    print_img(my_field, color)
    for i in range(0, steps):
        my_field = step(my_field)
        print_img(my_field, color)

    j_data['starting cells'] = get_alive_list(my_field)
    save_config(j_data)

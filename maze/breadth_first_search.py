import turtle
import json


with open('configuration.json', 'r') as configuration:
    data = json.load(configuration)

LAYOUT = data['layout']
SIZE   = data['size']
HEIGHT = len(LAYOUT)
WIDTH  = len(LAYOUT[0])

paths, visited, frontier, route = list(), list(), list(), list()
x_start, y_start, x_end, y_end = int(), int(), int(), int()
collection = dict()


class Square(turtle.Turtle):
    def __init__(self, color:str) -> None:
        turtle.Turtle.__init__(self)
        self.shapesize(SIZE/22, SIZE/22, SIZE/22)
        self.shape('square')
        self.color(color)
        self.penup()
        self.speed(0)
        self.hideturtle()

screen = turtle.Screen()
screen.title('BFS - Breadth First Search')
screen.setup(1.1*SIZE*WIDTH, 1.1*SIZE*HEIGHT)

writing = turtle.Turtle()
writing.color('blue')
writing.hideturtle()

black = Square('black')
gray  = Square('gray')
red   = Square('red')
green = Square('green')
blue  = Square('blue')


def matrix_to_screen(x_matrix:int, y_matrix:int) -> tuple:
    x_screen = + (SIZE * x_matrix) + (SIZE / 2) - (SIZE * WIDTH / 2)
    y_screen = - (SIZE * y_matrix) - (SIZE / 2) + (SIZE * HEIGHT / 2)
    return (int(x_screen), int(y_screen))

def screen_to_matrix(x_screen:int, y_screen:int) -> tuple:
    x_matrix = + (x_screen / SIZE) - (1 / 2) + (WIDTH / 2)
    y_matrix = - (y_screen / SIZE) - (1 / 2) - (HEIGHT / 2)
    return (int(x_matrix), int(y_matrix))


def setup_maze() -> None:

    global x_start, y_start, x_end, y_end

    for y in range(HEIGHT):
        for x in range(WIDTH):

            x_screen, y_screen = matrix_to_screen(x, y)
            character = LAYOUT[y][x]

            if character in ['X']:
                black.goto(x_screen, y_screen)
                black.stamp()

            elif character in ['s', 'e']:
                green.goto(x_screen, y_screen)
                green.stamp()
                paths.append((x, y))
                if character == 's':
                    x_start, y_start = x, y
                if character == 'e':
                    x_end, y_end = x, y

            elif character in [' ']:
                paths.append((x, y))


# method
def searching_algorithm() -> None:

    start = (x_start, y_start)
    end   = (x_end, y_end)

    frontier.append(start)
    collection[start] = start

    # successor function
    while len(frontier) > 0:

        x_matrix, y_matrix = frontier.pop(0)
        x_screen, y_screen = matrix_to_screen(x_matrix, y_matrix)
        visited.append((x_matrix, y_matrix))

        current = (x_matrix+0, y_matrix+0)
        up      = (x_matrix+0, y_matrix-1)
        right   = (x_matrix+1, y_matrix+0)
        down    = (x_matrix+0, y_matrix+1)
        left    = (x_matrix-1, y_matrix+0)

        if current not in [start, end]:
            gray.goto(x_screen, y_screen)
            gray.stamp()

        if up in paths and up not in visited:
            visited.append(up)
            frontier.append(up)
            collection[up] = current

        if right in paths and right not in visited:
            visited.append(right)
            frontier.append(right)
            collection[right] = current

        if down in paths and down not in visited:
            visited.append(down)
            frontier.append(down)
            collection[down] = current

        if left in paths and left not in visited:
            visited.append(left)
            frontier.append(left)
            collection[left] = current


# goal test
def get_solution() -> None:
    x_matrix, y_matrix = x_end, y_end
    x_screen, y_screen = matrix_to_screen(x_matrix, y_matrix)
    route.append((x_matrix, y_matrix))
    red.goto(x_screen, y_screen)
    red.stamp()
    while (x_matrix, y_matrix) != (x_start, y_start):
        x_matrix, y_matrix = collection[x_matrix, y_matrix]
        x_screen, y_screen = matrix_to_screen(x_matrix, y_matrix)
        route.append((x_matrix, y_matrix))
        red.goto(x_screen, y_screen)
        red.stamp()
    # path cost
    writing.write(f'Length: {len(route)}', font=('arial', SIZE, 'bold'), align='center')


setup_maze()
searching_algorithm()
get_solution()


screen.exitonclick()
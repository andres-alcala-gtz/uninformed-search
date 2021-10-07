import json


U = 'UP'
D = 'DOWN'
L = 'LEFT'
R = 'RIGHT'


with open('configuration.json', 'r') as configuration:
    data = json.load(configuration)

START = data['start']
END   = data['end']
N     = int(pow(len(START), 1/2)) if len(START) == len(END) else None

node_goal = None


class PuzzleState:
    def __init__(self, state, parent, move) -> None:
        self.state  = state
        self.parent = parent
        self.move   = move
        self.string = ' '.join(str(value) for value in state) if state else None


# successor function
def perform_movement(state:list, move:str) -> list:

    new_state = state[:]
    allowed   = []

    index  = new_state.index(0)
    row    = index // N
    column = index % N

    if row > 0:
        allowed.append(U)
    if row < N-1:
        allowed.append(D)
    if column > 0:
        allowed.append(L)
    if column < N-1:
        allowed.append(R)

    if move not in allowed:
        return None
    elif move == U:
        new_state[index], new_state[index-N] = new_state[index-N], new_state[index]
    elif move == D:
        new_state[index], new_state[index+N] = new_state[index+N], new_state[index]
    elif move == L:
        new_state[index], new_state[index-1] = new_state[index-1], new_state[index]
    elif move == R:
        new_state[index], new_state[index+1] = new_state[index+1], new_state[index]

    return new_state


def child_nodes(node:PuzzleState) -> list:

    children = []
    children.append(PuzzleState(perform_movement(node.state, U), node, U))
    children.append(PuzzleState(perform_movement(node.state, D), node, D))
    children.append(PuzzleState(perform_movement(node.state, L), node, L))
    children.append(PuzzleState(perform_movement(node.state, R), node, R))

    paths = []
    for child in children:
        if child.state != None:
            paths.append(child)

    return paths


# method
def searching_algorithm() -> None:

    global node_goal

    frontier = [PuzzleState(START, None, None)]
    visited  = set()

    while frontier:

        node = frontier.pop(0)
        visited.add(node.string)

        # goal test
        if node.state == END:
            node_goal = node
            return None

        paths = child_nodes(node)
        for path in paths:
            if path.string not in visited:
                frontier.append(path)
                visited.add(path.string)


searching_algorithm()

# path cost
movements = []
while node_goal.state != START:
    movements.insert(0, node_goal.move)
    node_goal = node_goal.parent


summary = {}
summary['Method'] = 'IDS - Iterative Deepening Search'
summary['Start'] = START
summary['End'] = END
summary['Movements'] = movements
summary['Length'] = len(movements)

with open('report.json', 'w') as report:
    json.dump(summary, report, indent=4)
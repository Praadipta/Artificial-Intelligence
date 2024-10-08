import sys
import heapq  # To implement a priority queue

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class GreedyFrontier:
    def __init__(self):
        self.frontier = []
        self.counter = 0  # To track insertion order for tie-breaking in heap

    def add(self, node, heuristic):
        # Add node with heuristic value, used for sorting
        heapq.heappush(self.frontier, (heuristic, self.counter, node))
        self.counter += 1

    def contains_state(self, state):
        # Check if any node in the frontier contains this state
        return any(node.state == state for (_, _, node) in self.frontier)

    def empty(self):
        # Return True if the frontier is empty
        return len(self.frontier) == 0

    def remove(self):
        # Remove and return the node with the smallest heuristic value
        if self.empty():
            raise Exception("empty frontier")
        else:
            _, _, node = heapq.heappop(self.frontier)
            return node

# Heuristic function (Manhattan distance) to estimate distance to the goal
def manhattan_distance(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

class Maze:
    def __init__(self, filename):
        # Load maze from file and set start/goal positions
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1 or contents.count("B") != 1:
            sys.exit("Maze must have exactly one start point (A) and one goal (B)")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        start = Node(state=self.start, parent=None, action=None)
        frontier = GreedyFrontier()
        frontier.add(start, manhattan_distance(self.start, self.goal))

        self.explored = set()
        self.num_explored = 0

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child, manhattan_distance(state, self.goal))

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        img = Image.new("RGBA", (self.width * cell_size, self.height * cell_size), "white")
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                x = j * cell_size
                y = i * cell_size

                if col:
                    fill = (40, 40, 40)  # Wall
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Start
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Goal
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Solution path
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Explored nodes
                else:
                    fill = (237, 240, 252)  # Empty space

                draw.rectangle(
                    [(x + cell_border, y + cell_border), (x + cell_size - cell_border, y + cell_size - cell_border)],
                    fill=fill
                )

        img.save(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    maze = Maze(sys.argv[1])
    print("Maze:")
    maze.print()
    print("Solving...")
    maze.solve()
    print("Solution:")
    maze.print()
    maze.output_image("maze_solution.png", show_solution=True, show_explored=True)

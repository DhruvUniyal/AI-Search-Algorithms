import time
from node import Node
from structures import Stack
from PIL import Image, ImageDraw

class DepthFirstSearch():
    def __init__(self, filename):
        with open(filename) as f:
            lines = f.read()

        if lines.count("A") != 1:
            raise Exception("Error! Maze has no start nodes or has more than 1 start nodes")
        if lines.count("B") != 1:
            raise Exception("Error! Maze has no end nodes or has more than 1 end nodes")

        # Determine height and width of maze
        lines = lines.splitlines()
        # print(lines)
        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if lines[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif lines[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif lines[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
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
        # Keep track of number of states explored
        self.num_explored = 0
        self.path_length = 0
        self.time_taken = 0
        startTime = time.time()

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = Stack()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
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
                self.time_taken = time.time()-startTime
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
            
    
    def output_image(self, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (46, 41, 41)

                # Start
                elif (i, j) == self.start:
                    fill = (0, 0, 255)
                    self.num_explored += 1

                # Goal
                elif (i, j) == self.goal:
                    fill = (1, 148, 1)
                    self.num_explored += 1

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (252,60,60)
                    self.num_explored += 1
                    self.path_length += 1

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (255, 165, 165)
                    self.num_explored += 1

                # Empty cell
                else:
                    fill = (255, 255, 255)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        if(show_explored):
            img.save("images/DFS.png")
        else:
            img.save("images/DFS-noexplored.png")
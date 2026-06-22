# Importing necessary libraries
import heapq  # Provides the functionality for a priority queue, used in the A* algorithm
import tkinter as tk  # Library for creating graphical user interfaces (GUI)
from typing import List  # Allows type hinting for lists
import time  # Used to introduce delays for animations in the GUI

# Defining the goal state of the 8-puzzle as a 3x3 grid where the empty space is represented by 0
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Class to represent a node in the search tree
class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        # Current state of the puzzle (a 3x3 grid)
        self.state = state
        # Pointer to the parent node (the state from which this node was reached)
        self.parent = parent
        # g is the cost from the start node to this node
        self.g = g
        # h is the heuristic value estimating the cost to the goal
        self.h = h
        # f is the total cost (g + h), used for prioritizing nodes in the A* algorithm
        self.f = g + h

    # Define the comparison behavior for nodes, prioritizing lower f-values in the priority queue
    def __lt__(self, other):
        return self.f < other.f

    # Locate the position of the zero (empty space) in the puzzle grid
    def find_zero(self):
        for i in range(3):  # Loop through rows
            for j in range(3):  # Loop through columns
                if self.state[i][j] == 0:  # Check if the current tile is zero
                    return i, j  # Return the row and column index of zero

# Calculate the Manhattan distance heuristic for the given state
def manhattan_distance(state: List[List[int]]) -> int:
    distance = 0  # Initialize the total distance to zero
    for i in range(3):  # Iterate over rows
        for j in range(3):  # Iterate over columns
            if state[i][j] != 0:  # Skip the empty space
                x, y = divmod(state[i][j] - 1, 3)  # Compute the target position of the tile in the goal state
                # Add the Manhattan distance (vertical + horizontal moves) to the total
                distance += abs(x - i) + abs(y - j)
    return distance

# Calculate the Hamming distance heuristic for the given state
def hamming_distance(state: List[List[int]]) -> int:
    distance = 0  # Initialize the count of misplaced tiles
    for i in range(3):  # Iterate through rows
        for j in range(3):  # Iterate through columns
            # Check if the tile is not in its goal position (excluding the empty space)
            if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j]:
                distance += 1  # Increment the count of misplaced tiles
    return distance

# Generate all possible moves (neighboring states) from the current state
def generate_moves(node: Node) -> List[Node]:
    moves = []  # List to store all possible moves
    x, y = node.find_zero()  # Locate the zero's position in the grid
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Possible moves: up, down, left, right
    for dx, dy in directions:  # Iterate through all possible moves
        nx, ny = x + dx, y + dy  # Calculate the new position of zero
        if 0 <= nx < 3 and 0 <= ny < 3:  # Check if the new position is within the grid bounds
            # Create a deep copy of the current state to modify
            new_state = [row[:] for row in node.state]
            # Swap the zero with the adjacent tile
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            # Create a new node for the resulting state and add it to the list of moves
            moves.append(Node(new_state, parent=node, g=node.g + 1))
    return moves

# Perform the A* search algorithm to solve the puzzle
def a_star_search(start: List[List[int]], heuristic) -> List[Node]:
    open_set = []  # Priority queue to store nodes to be explored
    start_node = Node(start, g=0, h=heuristic(start))  # Create the initial node with the chosen heuristic
    heapq.heappush(open_set, start_node)  # Add the initial node to the open set
    closed_set = set()  # Set to store visited states
    closed_set.add(tuple(map(tuple, start)))  # Convert the initial state to a hashable type and mark it as visited

    while open_set:  # Continue until there are no nodes left to explore
        current = heapq.heappop(open_set)  # Get the node with the lowest f-value
        if current.state == GOAL_STATE:  # Check if the goal state has been reached
            path = []  # List to reconstruct the solution path
            while current:  # Trace back from the goal node to the start node
                path.append(current)
                current = current.parent
            return path[::-1]  # Return the path in the correct order (from start to goal)

        # Generate all possible moves from the current state
        for neighbor in generate_moves(current):
            neighbor_tuple = tuple(map(tuple, neighbor.state))  # Convert the state to a hashable type
            if neighbor_tuple in closed_set:  # Skip the state if it has already been visited
                continue
            neighbor.h = heuristic(neighbor.state)  # Calculate the heuristic value for the neighbor
            neighbor.f = neighbor.g + neighbor.h  # Update the total cost (g + h)
            heapq.heappush(open_set, neighbor)  # Add the neighbor to the priority queue
            closed_set.add(neighbor_tuple)  # Mark the state as visited

    return None  # Return None if no solution is found


# GUI class for the 8-puzzle solver
class PuzzleGUI:
    def __init__(self, root):
        # Initialize the root Tkinter window
        self.root = root
        self.root.title("8-Puzzle Solver")  # Set the title of the application window
        self.start_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Default initial state of the puzzle
        self.solution_path = None  # Placeholder to store the solution path

        # Create 3x3 grids for user input, the solving process, and the goal state
        self.input_grid = [[None for _ in range(3)] for _ in range(3)]  # Grid for user input
        self.solve_grid = [[None for _ in range(3)] for _ in range(3)]  # Grid for displaying the solving process
        self.goal_grid = [[None for _ in range(3)] for _ in range(3)]  # Grid for displaying the goal state

        # Labels to indicate the purpose of each grid
        tk.Label(root, text="Enter Start State").grid(row=0, column=0)  # Label for the input grid
        tk.Label(root, text="Solving Process").grid(row=0, column=1)  # Label for the solving grid
        tk.Label(root, text="Goal State").grid(row=0, column=2)  # Label for the goal grid

        # Frames to hold the grids, each with a border for clarity
        input_frame = tk.Frame(root, borderwidth=2, relief="solid")  # Frame for input grid
        input_frame.grid(row=1, column=0, padx=5, pady=5)  # Position the input frame in the GUI
        solve_frame = tk.Frame(root, borderwidth=2, relief="solid")  # Frame for solving process grid
        solve_frame.grid(row=1, column=1, padx=5, pady=5)  # Position the solving frame in the GUI
        goal_frame = tk.Frame(root, borderwidth=2, relief="solid")  # Frame for goal state grid
        goal_frame.grid(row=1, column=2, padx=5, pady=5)  # Position the goal frame in the GUI

        # Initialize the individual grids within their respective frames
        self.create_input_grid(self.input_grid, input_frame)  # Create the input grid
        self.create_grid(self.solve_grid, solve_frame)  # Create the solving grid
        self.create_grid(self.goal_grid, goal_frame)  # Create the goal grid

        # Display the predefined goal state in the goal grid
        self.display_state(self.goal_grid, GOAL_STATE)

        # Dropdown menu to allow users to select a heuristic (Manhattan or Hamming)
        self.heuristic_var = tk.StringVar(value="Manhattan")  # Default heuristic is Manhattan
        heuristic_menu = tk.OptionMenu(root, self.heuristic_var, "Manhattan", "Hamming")  # Dropdown menu
        heuristic_menu.grid(row=2, column=0, columnspan=1, sticky="ew")  # Position the dropdown in the GUI

        # Buttons for solving the puzzle and resetting the interface
        solve_button = tk.Button(root, text="Solve", command=self.solve_puzzle)  # Button to trigger the solve process
        solve_button.grid(row=4, column=0, columnspan=1, sticky="ew")  # Position the solve button
        reset_button = tk.Button(root, text="Reset", command=self.reset_puzzle)  # Button to reset the interface
        reset_button.grid(row=4, column=1, columnspan=1, sticky="ew")  # Position the reset button

    def create_input_grid(self, grid_frames, parent_frame):
        """Creates a 3x3 grid of entry widgets for user input."""
        for i in range(3):  # Loop through rows
            for j in range(3):  # Loop through columns
                # Create an entry widget with a large font for input
                entry = tk.Entry(parent_frame, font=("Helvetica", 18), width=2, justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)  # Position the entry widget in the grid
                grid_frames[i][j] = entry  # Store the widget in the grid frame

    def create_grid(self, grid_frames, parent_frame):
        """Creates a 3x3 grid of labels for displaying states."""
        for i in range(3):  # Loop through rows
            for j in range(3):  # Loop through columns
                # Create a frame to hold each label, with a border for better visibility
                frame = tk.Frame(parent_frame, width=60, height=60, borderwidth=1, relief="solid")
                frame.grid(row=i, column=j, padx=5, pady=5)  # Position the frame in the grid
                # Create a label for displaying a single tile value
                label = tk.Label(frame, text="", font=("Helvetica", 18), width=2, height=1)
                label.pack()  # Place the label inside the frame
                grid_frames[i][j] = label  # Store the label in the grid frame

    def display_state(self, grid_frames, state):
        """Updates a 3x3 grid to display a given state."""
        for i in range(3):  # Loop through rows
            for j in range(3):  # Loop through columns
                # Update the text of each grid cell to show the state's value (empty space as blank)
                grid_frames[i][j].config(text=str(state[i][j]) if state[i][j] != 0 else "")

    def get_initial_state(self):
        """Reads the initial state entered by the user from the input grid."""
        initial_state = []  # List to store the parsed input state
        for i in range(3):  # Loop through rows
            row = []  # Temporary list to store a single row
            for j in range(3):  # Loop through columns
                try:
                    # Try to parse the input value as an integer; use 0 for invalid entries
                    value = int(self.input_grid[i][j].get())
                except ValueError:
                    value = 0  # Default to 0 if the input is invalid
                row.append(value)  # Add the parsed value to the row
            initial_state.append(row)  # Add the row to the initial state
        return initial_state  # Return the complete initial state

    def solve_puzzle(self):
        """Solves the puzzle using the selected heuristic and displays the solution."""
        self.start_state = self.get_initial_state()  # Retrieve the initial state from user input
        # Choose the heuristic function based on the user's selection
        heuristic = manhattan_distance if self.heuristic_var.get() == "Manhattan" else hamming_distance
        self.solution_path = a_star_search(self.start_state, heuristic)  # Run the A* search algorithm
        if self.solution_path:  # Check if a solution was found
            self.animate_solution()  # Animate the solution path in the solving grid
        else:
            print("No solution found.")  # Print a message if no solution exists

    def animate_solution(self):
        """Animates the solution path step-by-step in the solving grid."""
        for step, node in enumerate(self.solution_path, start=1):  # Iterate through each step in the solution path
            print(f"Step {step}:\n{node.state}\n")  # Print the state of the puzzle at each step
            self.display_state(self.solve_grid, node.state)  # Display the current state in the solving grid
            self.root.update()  # Refresh the GUI to show the updated state
            time.sleep(0.5)  # Pause briefly to create an animation effect

    def reset_puzzle(self):
        """Resets the input grid and the solving grid to their default states."""
        for i in range(3):  # Loop through rows
            for j in range(3):  # Loop through columns
                self.input_grid[i][j].delete(0, tk.END)  # Clear the input field
        # Clear the solving grid by displaying an empty state
        self.display_state(self.solve_grid, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.solution_path = None  # Reset the solution path

# Main execution block to start the GUI application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter application window
    puzzle_gui = PuzzleGUI(root)  # Initialize the PuzzleGUI class to set up the interface
    root.mainloop()  # Start the Tkinter event loop to run the application


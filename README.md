# 8-Puzzle Solver Using A* Search Algorithm

## Overview

This project is an Artificial Intelligence application that solves the classic 8-Puzzle problem using the A* Search Algorithm.

The application allows users to:

* Enter a custom puzzle configuration
* Choose between Manhattan Distance and Hamming Distance heuristics
* Solve the puzzle using A*
* Visualize each step of the solution path through an animated graphical interface
* Detect invalid and unsolvable puzzle configurations

The project was developed as part of the **CSAI 350 – Introduction to Artificial Intelligence** course at the American University of Ras Al Khaimah (AURAK).

---

## Project Objective

The objective of this project was to implement an informed search algorithm capable of efficiently solving the 8-Puzzle problem while providing an intuitive graphical interface for user interaction and visualization.

The project demonstrates:

* Artificial Intelligence Search Techniques
* Heuristic-Based Problem Solving
* State Space Exploration
* GUI Development
* User Input Validation
* Algorithm Visualization

---

## About the 8-Puzzle Problem

The 8-Puzzle consists of a 3×3 grid containing eight numbered tiles and one blank space.

The goal is to move the tiles until the puzzle reaches the target configuration:

```
1 2 3
4 5 6
7 8 0
```

where 0 represents the blank tile.

---

## Technologies Used

* Python
* Tkinter
* Heap Queue (heapq)
* Object-Oriented Programming
* A* Search Algorithm

---

## Key Features

### A* Search Algorithm

The application uses A* search to find the shortest path from the initial state to the goal state.

The evaluation function is:

``-
f(n) = g(n) + h(n)
```

where:

* g(n) = Cost from start node
* h(n) = Estimated cost to goal

---

### Multiple Heuristics

#### Manhattan Distance

Calculates the total distance each tile must travel to reach its goal position.

Benefits:

* More informed heuristic
* Usually explores fewer states
* Faster solution discovery

#### Hamming Distance

Counts the number of misplaced tiles.

Benefits:

* Simpler calculation
* Easy to understand and implement

---

### Interactive GUI

The application includes:

* Start State Grid
* Solving Process Grid
* Goal State Grid
* Heuristic Selection Dropdown
* Solve Button
* Reset Button

---

### Animated Solution Visualization

Users can watch the puzzle being solved step-by-step through a dynamic animation.

The solving grid updates automatically as the algorithm progresses toward the goal state.

---

### Input Validation

The system validates user input by checking:

* Numbers are between 0 and 8
* No duplicate values exist
* All required values are present
* Input format is valid

Invalid configurations are rejected before solving begins.

---

### Unsolvable Puzzle Detection

The application handles unsolvable puzzle configurations and informs the user when no solution exists.

This is based on the mathematical concept of inversion parity.

---

## Understanding Inversion Parity

Not every 8-Puzzle configuration can be solved.

A puzzle is solvable only if the number of inversions is even.

An inversion occurs when:

```text
A larger tile appears before a smaller tile.
```

Example:

```
4 2 1
5 7 6
8 3 0
```

This configuration contains an odd number of inversions and therefore cannot reach the goal state.

When an unsolvable configuration is entered, the system returns:

```text
No Solution Found
```

---

#### Node Class

Represents a puzzle state and stores:

* Current State
* Parent State
* Path Cost (g)
* Heuristic Cost (h)
* Total Cost (f)

---

#### Heuristic Functions

* Manhattan Distance
* Hamming Distance

---

#### Search Engine

Implements:

* Open Set (Priority Queue)
* Closed Set (Visited States)
* State Expansion
* Path Reconstruction

---

#### GUI Layer

Built using Tkinter and responsible for:

* User interaction
* Puzzle visualization
* Animation
* Input validation

---

## Results

The application successfully:

* Solves valid 8-Puzzle configurations
* Finds optimal solution paths
* Supports multiple heuristics
* Detects invalid inputs
* Handles unsolvable states
* Visualizes every step of the solving process

---

## Challenges Encountered

### Handling Unsolvable Configurations

A significant challenge was understanding why certain puzzle states could never be solved.

Research into inversion parity revealed the mathematical conditions required for solvability, which was then integrated into the project analysis.

---

### Input Validation

Incorrect or incomplete user inputs occasionally caused runtime errors.

Additional validation checks were implemented to ensure all puzzle states met the requirements before execution.

---

### Animation and Visualization

Creating a smooth visualization of the solving process required synchronizing GUI updates with algorithm execution.

Tkinter's update mechanism combined with timed delays enabled a clear step-by-step animation.

---

## Learning Outcomes

Through this project, I gained hands-on experience in:

* Artificial Intelligence
* Search Algorithms
* A* Search
* Heuristic Functions
* State Space Search
* GUI Development
* Input Validation
* Problem Solving
* Algorithm Visualization

---


---

## Team Members

* Jannat Waqass
* Hana Rahiman
* Jana Shehata
* Lana Zanneh
* Urita Sadallah

---

## Course Information

**Course:** CSAI 350 – Introduction to Artificial Intelligence

---

## Future Enhancements

Potential future improvements include:

* Support for 15-Puzzle (4×4 Grid)
* Additional Heuristic Functions
* Puzzle Randomizer
* Performance Statistics Dashboard
* Search Tree Visualization
* Dark Mode Interface
* Web-Based Deployment

---

## License

This project is intended for academic and educational purposes.

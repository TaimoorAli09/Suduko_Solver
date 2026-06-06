
## **AI-Powered Multi-Level Sudoku Solver and Evaluator**



---

### Complex Computing Problem (CCP)

#### **Course Code & Title**: CSC202 Artificial Intelligence

---

## Submitted By

**Name:** Taimoor Ali  
**Roll Number:** 2024_CS_609_(SECTION_A_)


---


## 1. Project Overview

This project implements an AI-powered Sudoku benchmarking system that generates, solves, and evaluates 9x9 Sudoku puzzles across four difficulty levels: Easy, Medium, Hard, and Expert. The implementation is built in Python and is organized into modular components for puzzle generation, solver logic, constraint handling, backend API, and frontend dashboard.

The primary objective is to compare multiple search strategies and provide measurable performance metrics for each algorithm. The system demonstrates how uninformed, informed, local search, and constraint propagation techniques behave under varied puzzle complexity.

---

## 2. Course Learning Outcome Alignment

- **CLO 3:** Perform informed, uninformed search, adversarial, and local search strategy algorithms to solve goal-oriented problems.
- **Bloom's Taxonomy Level:** Evaluate (Level 5)

This project aligns with CLO 3 by implementing and evaluating different search strategies for the Sudoku constraint satisfaction problem (CSP), and by conducting comparative analysis of algorithm efficiency.

---

## 3. CCP Attributes

### A2 Depth of Analysis Required
The Sudoku solver has no obvious one-step solution. It requires formal CSP modeling, heuristic analysis, and design of multiple search strategies to solve and compare puzzles of varying difficulty.

### A3 Depth of Knowledge Required
The system uses in-depth AI search knowledge, including backtracking, MRV heuristics, local search, and constraint propagation principles, to implement practical solvers and benchmark them.

### A8 Interdependence
The architecture is modular and interdependent. Puzzle generation, CSP modeling, solver algorithms, frontend interaction, and performance reporting all depend on each other and must function together.

---

## 4. Problem Formulation

### 4.1 Sudoku as a CSP
Sudoku is formulated as a constraint satisfaction problem with:

- **Variables:** Each of the 81 cells in a 9x9 grid.
- **Domains:** Integer values from 1 to 9 for empty cells.
- **Constraints:**
  - Each row must contain unique digits 1 through 9.
  - Each column must contain unique digits 1 through 9.
  - Each 3x3 sub-grid must contain unique digits 1 through 9.

The objective is to assign valid values to all empty cells while satisfying these constraints.

### 4.2 Difficulty Levels
Difficulty is defined by the number of pre-filled cells and the complexity of the resulting search space:

- Easy: more clues, fewer empty cells
- Medium: moderate number of clues and search depth
- Hard: fewer clues and greater branching factor
- Expert: minimal clues and maximum search pressure

The implementation uses pre-filled clue counts to generate puzzles with varying difficulty.

---

## 5. System Architecture

The system is organized into four main modules:

1. **Puzzle Generator:** `puzzle_generator.py`
2. **Solver Logic:** `solverlogic.py`
3. **Backend API:** `main.py`
4. **Frontend UI:** `SudukoUI/index.html`, `SudukoUI/script.js`, `SudukoUI/style.css`

### 5.1 Module Responsibilities

- `puzzle_generator.py`: Generates a complete valid Sudoku board then removes cells according to difficulty.
- `solverlogic.py`: Implements solver algorithms and metrics collection.
- `main.py`: Exposes REST API endpoints for generating, solving, and comparing puzzles.
- `SudukoUI/`: Provides a user interface for selecting difficulty and algorithm, visualizing the solve process, and viewing performance metrics.

---

## 6. Algorithm Design and Justification

This implementation includes four solver strategies:

### 6.1 Uninformed Search: Backtracking
- Implemented in `SudokuSolver.solve_backtracking()`.
- Uses depth-first search through empty cells.
- Explores the full state space with constraint checking but without heuristic guidance.
- Serves as the baseline algorithm.

### 6.2 Informed Search: MRV Heuristic
- Implemented in `SudokuSolver.solve_mrv()`.
- Selects the empty cell with the Minimum Remaining Values (MRV).
- MRV heuristics reduce branching by solving the most constrained variable first.
- This method still uses constraint checking and recursive search.

### 6.3 Local Search: Hill Climbing
- Implemented in `SudokuSolver.solve_hill()`.
- Starts from a randomly filled grid and iteratively reduces constraint violations.
- Uses a cost function measuring duplicate values in rows.
- Accepts only changes that do not increase the cost, thus climbing toward a valid solution.

### 6.4 Constraint Propagation: Forward Checking
- Exposed in `SudokuSolver.solve_forward()`.
- In the current codebase, this method routes to the backtracking solver.
- The intention is to preserve a modular structure so an independent forward checking solver can be added later.

### 6.5 Algorithm Comparison
- `main.py` implements the `/compare` endpoint.
- It solves the same input board using all four strategies.
- Metrics recorded for each algorithm include:
  - Execution time
  - States explored
  - Backtracks performed
  - Success flag

---

## 7. Implementation Details

### 7.1 Puzzle Generator (`puzzle_generator.py`)

- Uses recursive backtracking to fill a complete board.
- After generating a complete solution, it removes cells to match difficulty-level clue counts.
- Difficulty mapping:
  - Easy: 45 clues
  - Medium: 35 clues
  - Hard: 28 clues
  - Expert: 20 clues

### 7.2 Solver Logic (`solverlogic.py`)

Key methods:

- `find_empty()`: Finds the next empty cell.
- `is_valid(num, pos)`: Validates a number against row, column, and 3x3 sub-grid constraints.
- `get_candidates(r, c)`: Returns valid numbers for a position.
- `find_mrv()`: Picks the empty position with the fewest valid candidates.

Solver metrics:

- `states_explored`: Incremented each recursive or search step.
- `backtracks`: Incremented when a placement is undone.
- `steps`: Logged to enable frontend animation.

### 7.3 Backend API (`main.py`)

API endpoints:

- `POST /generate`: Returns a new board for the requested difficulty.
- `POST /solve`: Solves a given board with the specified algorithm.
- `POST /compare`: Runs all four algorithms on the same board and returns comparative metrics.

The FastAPI backend handles cross-origin requests with CORS enabled, allowing the frontend to call the API from a browser.

### 7.4 Frontend UI (`SudukoUI/`)

The web interface allows users to:

- Select difficulty and algorithm
- Generate puzzles
- Solve puzzles with animation
- Compare algorithm performance
- View metrics for time, states, and backtracks

The frontend communicates with the API endpoints using `fetch()` and renders results dynamically in the browser.

---

## 8. Performance Reporting

### 8.1 Metrics Collected

For each solve operation, the system records:

- `executionTime`: Clock time for the solver
- `statesExplored`: Number of search states visited
- `backtracksPerformed`: Number of backtracking undo operations
- `success`: Whether the solver found a valid solution

### 8.2 Comparative Dashboard

The frontend displays comparison results in a table format. Each row includes:

- Algorithm name
- Execution time
- States explored
- Backtracks
- Success status

This enables side-by-side evaluation of algorithm performance on the same puzzle.

---

## 9. Testing Evidence

Testing includes:

- Generating puzzles for each difficulty level
- Solving the same board with all four algorithms
- Validating output against Sudoku constraints
- Logging solver responses and metrics in the browser console

Screenshots or logs from the demo can be captured from the browser UI and API console output.

---

## 10. Challenges and Solutions

### 10.1 Ensuring Modular Design
The project separates responsibilities into generator, solver, API, and UI modules to support maintainability and extensibility.

### 10.2 Balancing Solver Complexity
The hill climbing solver uses a simple cost function and randomized assignment to demonstrate local search behavior, while backtracking and MRV provide structured search baselines.

### 10.3 Integrating Frontend and Backend
A CORS-enabled FastAPI backend was used to allow the browser frontend to interact with the solver and generator endpoints.

---

## 11. Future Improvements

Potential enhancements include:

- Implementing a dedicated AC-3 arc consistency module
- Completing a true forward checking solver with candidate pruning
- Adding an adversarial race mode for two algorithms solving the same puzzle concurrently
- Extending the UI with charts for deeper comparative analysis

---

## 12. Conclusion

This project delivers a working AI-driven Sudoku benchmarking system that is aligned with the CCP requirements and CLO 3. It provides a professional, modular implementation of multiple search strategies, a generation pipeline, and a visual comparison interface for algorithm performance.

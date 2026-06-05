# Sudoku Solver & AI Benchmarking

A hybrid Sudoku project with a browser-based UI and a Python FastAPI backend. The app can generate Sudoku puzzles at multiple difficulty levels, solve them using several algorithms, and compare solver performance metrics.

## Features

- Generate Sudoku boards at `easy`, `medium`, `hard`, and `expert` difficulties
- Solve puzzles using:
  - Backtracking
  - MRV / Informed search
  - Forward checking (currently routed through backtracking)
  - Hill climbing
- Animate solving steps in the browser
- Compare algorithm performance with execution time, state count, and backtrack count
- Simple web frontend in `SudukoUI/`
- Python API backend in the project root

## Repository structure

- `main.py` — FastAPI application exposing `/generate`, `/solve`, and `/compare` endpoints
- `puzzle_generator.py` — random Sudoku puzzle generator with difficulty-based clue removal
- `solverlogic.py` — solver implementation with multiple search algorithms and metrics tracking
- `SudukoUI/` — frontend files for UI, including `index.html`, `script.js`, and `style.css`
- `requirement.txt` — Python dependencies for the backend
- `backend_suduko/` — optional .NET backend project included in the repository

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirement.txt
```

3. Start the backend API:

```powershell
uvicorn main:app --reload
```

4. Serve the frontend from `SudukoUI/`.
   Using a local static server is recommended to avoid browser file restrictions:

```powershell
cd SudukoUI
python -m http.server 5500
```

5. Open the UI in your browser:

```text
http://127.0.0.1:5500
```

## Usage

- Use the dropdowns to select difficulty and algorithm
- Click `Generate` to create a new board
- Click `Solve` to solve the current board with the selected algorithm
- Click `Compare` to run all algorithms and display benchmark results
- Click `Clear` to reload the page and reset the grid

## Notes

- The UI expects the backend API to run at `http://127.0.0.1:8000`
- If `style.css` does not appear, verify that the browser is loading the file from the same `SudukoUI` folder
- `solve_forward()` currently uses backtracking logic; you can update it later with a dedicated forward-checking implementation

## Optional C# backend

The repository includes `backend_suduko/` for a separate .NET-based Sudoku backend. The primary frontend currently communicates with the Python FastAPI backend in the repository root.

## License

This project is provided as-is for learning and experimentation.

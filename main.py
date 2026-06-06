from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from time import perf_counter

from solverlogic import SudokuSolver
from puzzle_generator import PuzzleGenerator



app = FastAPI()



# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# REQUEST MODELS
# =====================


class SudokuRequest(BaseModel):
    board: List[List[int]]
    algorithm: str
    difficulty: str


class GenerateRequest(BaseModel):
    difficulty: str


# =====================
# GENERATE PUZZLE
# =====================


@app.post("/generate")
def generate_puzzle(req: GenerateRequest):

    generator = PuzzleGenerator()
    board = generator.generate(req.difficulty)

    return {"board": board}


# =====================
# SOLVE PUZZLE
# =====================


@app.post("/solve")
def solve_sudoku(req: SudokuRequest):

    solver = SudokuSolver([row[:] for row in req.board])

    start = perf_counter()

    algo = req.algorithm.lower()

    if algo == "backtracking":
        success = solver.solve_backtracking()

    elif algo == "informed":
        success = solver.solve_mrv()

    elif algo == "forward":
        success = solver.solve_forward()

    elif algo == "hill":
        success = solver.solve_hill()

    else:
        return {"success": False, "error": "Invalid algorithm"}

    end = perf_counter()

    

    return {
        "solution": solver.board if success else None,
        "success": success,
        "steps": solver.steps,
        "metrics": {
            "executionTime": end - start,
            "statesExplored": solver.states_explored,
            "backtracksPerformed": solver.backtracks,
        },
    }


# =====================
# COMPARE ALGORITHMS
# =====================


@app.post("/compare")
def compare(req: SudokuRequest):

    algorithms = ["backtracking", "informed", "forward", "hill"]
    results = []

    for algo in algorithms:

        solver = SudokuSolver([row[:] for row in req.board])

        start = perf_counter()

        if algo == "backtracking":
            success = solver.solve_backtracking()
        elif algo == "informed":
            success = solver.solve_mrv()
        elif algo == "forward":
            success = solver.solve_forward()
        elif algo == "hill":
            success = solver.solve_hill()

        end = perf_counter()

        results.append(
            {
                "algorithm": algo,
                "executionTime": round(end - start, 5),
                "statesExplored": solver.states_explored,
                "backtracks": solver.backtracks,
                "success": success,
            }
        )

    return results


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app)

# # run:
# must bind with port 8000 to match frontend fetch URL
# uvicorn main:app --reload --port 8000

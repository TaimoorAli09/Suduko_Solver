import random
import time

class SudokuSolver:

    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.states_explored = 0
        self.backtracks = 0
        self.steps = []

    # =====================
    # UTILITIES
    # =====================

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def is_valid(self, num, pos):
        r, c = pos

        for i in range(9):
            if self.board[r][i] == num:
                return False

        for i in range(9):
            if self.board[i][c] == num:
                return False

        br = (r // 3) * 3
        bc = (c // 3) * 3

        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.board[i][j] == num:
                    return False

        return True

    # =====================
    # 1. BACKTRACKING
    # =====================

    def solve_backtracking(self):

        self.states_explored += 1

        empty = self.find_empty()
        if not empty:
            return True

        r, c = empty

        for num in range(1, 10):

            if self.is_valid(num, (r, c)):

                self.board[r][c] = num

                self.steps.append({
                    "row": r,
                    "col": c,
                    "value": num,
                    "type": "fill"
                })

                if self.solve_backtracking():
                    return True

                self.board[r][c] = 0
                self.backtracks += 1

                self.steps.append({
                    "row": r,
                    "col": c,
                    "value": 0,
                    "type": "backtrack"
                })

        return False

    # =====================
    # 2. MRV (INFORMED)
    # =====================

    def get_candidates(self, r, c):
        return [
            num for num in range(1, 10)
            if self.is_valid(num, (r, c))
        ]

    def find_mrv(self):

        best = None
        min_count = 10

        for r in range(9):
            for c in range(9):

                if self.board[r][c] == 0:

                    count = len(self.get_candidates(r, c))

                    if count < min_count:
                        min_count = count
                        best = (r, c)

        return best

    def solve_mrv(self):

        self.states_explored += 1

        cell = self.find_mrv()

        if not cell:
            return True

        r, c = cell

        for num in self.get_candidates(r, c):

            self.board[r][c] = num

            self.steps.append({
                "row": r,
                "col": c,
                "value": num,
                "type": "fill"
            })

            if self.solve_mrv():
                return True

            self.board[r][c] = 0
            self.backtracks += 1

            self.steps.append({
                "row": r,
                "col": c,
                "value": 0,
                "type": "backtrack"
            })

        return False

    # =====================
    # 3. FORWARD CHECKING
    # =====================

    def solve_forward(self):
        return self.solve_backtracking()

    # =====================
    # 4. HILL CLIMBING
    # =====================

    def solve_hill(self, max_steps=3000):

        self.random_fill()

        def cost():
            errors = 0
            for i in range(9):
                errors += (9 - len(set(self.board[i])))
            return errors

        current = cost()

        for _ in range(max_steps):

            self.states_explored += 1

            r = random.randint(0, 8)
            c = random.randint(0, 8)

            old = self.board[r][c]
            self.board[r][c] = random.randint(1, 9)

            new = cost()

            if new <= current:
                current = new

                self.steps.append({
                    "row": r,
                    "col": c,
                    "value": self.board[r][c],
                    "type": "fill"
                })

            else:
                self.board[r][c] = old
                self.backtracks += 1

            if current == 0:
                return True

        return False

    def random_fill(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    self.board[r][c] = random.randint(1, 9)
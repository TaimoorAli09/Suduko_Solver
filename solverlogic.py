



import random
from collections import deque


class SudokuSolver:

    def __init__(self, board):

        # Create deep copy of puzzle
        # to avoid modifying original board
        self.board = [row[:] for row in board]

        # Performance metrics
        self.states_explored = 0
        self.backtracks = 0

        # Used for frontend animation
        self.steps = []

        # Store original puzzle clues
        # These cells must NEVER change
        # during local search
        self.fixed_cells = set()

        for r in range(9):
            for c in range(9):

                if board[r][c] != 0:
                    self.fixed_cells.add((r, c))

    # ==================================================
    # BASIC UTILITIES
    # ==================================================

    def find_empty(self):

        """
        Find first empty cell (0)
        Returns:
            (row, col)
        """

        for r in range(9):
            for c in range(9):

                if self.board[r][c] == 0:
                    return (r, c)

        return None

    def is_valid(self, num, pos):

        """
        Check if placing number is valid
        according to Sudoku constraints.

        Constraints:
        1. Row uniqueness
        2. Column uniqueness
        3. 3x3 box uniqueness
        """

        r, c = pos

        # Row check
        for i in range(9):

            if i != c and self.board[r][i] == num:
                return False

        # Column check
        for i in range(9):

            if i != r and self.board[i][c] == num:
                return False

        # 3x3 Box check
        br = (r // 3) * 3
        bc = (c // 3) * 3

        for i in range(br, br + 3):
            for j in range(bc, bc + 3):

                if (i, j) != pos and self.board[i][j] == num:
                    return False

        return True

    # ==================================================
    # CSP UTILITIES
    # ==================================================

    def get_neighbors(self, row, col):

        """
        Returns all constrained neighboring cells.

        Neighbor means:
        - same row
        - same column
        - same 3x3 box

        Used in:
        - Forward Checking
        - Degree Heuristic
        - AC3
        """

        neighbors = set()

        # Row neighbors
        for c in range(9):

            if c != col:
                neighbors.add((row, c))

        # Column neighbors
        for r in range(9):

            if r != row:
                neighbors.add((r, col))

        # Box neighbors
        br = (row // 3) * 3
        bc = (col // 3) * 3

        for r in range(br, br + 3):
            for c in range(bc, bc + 3):

                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def get_candidates(self, r, c):

        """
        Returns all possible valid values
        for a given cell.
        """

        return [
            num
            for num in range(1, 10)
            if self.is_valid(num, (r, c))
        ]

    # ==================================================
    # 1. BACKTRACKING (UNINFORMED SEARCH)
    # ==================================================

    def solve_backtracking(self):

        """
        Classic DFS Backtracking.

        Explores complete state space
        without heuristics.
        """

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

                # Undo move
                self.board[r][c] = 0
                self.backtracks += 1

                self.steps.append({
                    "row": r,
                    "col": c,
                    "value": 0,
                    "type": "backtrack"
                })

        return False

    # ==================================================
    # 2. INFORMED SEARCH
    # AC3 + MRV + DEGREE HEURISTIC
    # ==================================================

    def degree(self, row, col):

        """
        Degree heuristic:
        Select variable that constrains
        maximum number of unassigned cells.
        """

        count = 0

        for r, c in self.get_neighbors(row, col):

            if self.board[r][c] == 0:
                count += 1

        return count

    def find_mrv(self):

        """
        Minimum Remaining Values (MRV)

        Select cell with smallest domain.

        Tie breaker:
        Degree heuristic.
        """

        best = None
        min_candidates = 10
        best_degree = -1

        for r in range(9):
            for c in range(9):

                if self.board[r][c] == 0:

                    candidates = self.get_candidates(r, c)
                    count = len(candidates)

                    deg = self.degree(r, c)

                    # MRV
                    if count < min_candidates:

                        min_candidates = count
                        best_degree = deg
                        best = (r, c)

                    # Degree heuristic tie break
                    elif count == min_candidates:

                        if deg > best_degree:
                            best_degree = deg
                            best = (r, c)

        return best

    def revise(self, xi, xj):

        """
        AC3 revise step.
        Removes inconsistent values.
        """

        revised = False

        r1, c1 = xi
        r2, c2 = xj

        if self.board[r1][c1] != 0:
            return revised

        domain_xi = self.get_candidates(r1, c1)

        for value in domain_xi[:]:

            consistent = False

            if self.board[r2][c2] != 0:

                if value != self.board[r2][c2]:
                    consistent = True

            else:

                domain_xj = self.get_candidates(r2, c2)

                for val2 in domain_xj:

                    if value != val2:
                        consistent = True
                        break

            if not consistent:
                revised = True

        return revised

    def ac3(self):

        """
        AC3 Algorithm

        Makes domains arc consistent
        before solving.
        """

        queue = deque()

        for r in range(9):
            for c in range(9):

                if self.board[r][c] == 0:

                    for neighbor in self.get_neighbors(r, c):
                        queue.append(((r, c), neighbor))

        while queue:

            xi, xj = queue.popleft()

            if self.revise(xi, xj):

                r, c = xi

                if len(self.get_candidates(r, c)) == 0:
                    return False

                for neighbor in self.get_neighbors(r, c):

                    if neighbor != xj:
                        queue.append((neighbor, xi))

        return True

    def solve_mrv(self):

        """
        Informed Search:
        AC3 + MRV + Degree Heuristic
        """

        self.states_explored += 1

        if not self.ac3():
            return False

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

    # ==================================================
    # 3. FORWARD CHECKING
    # ==================================================

    def forward_check(self, row, col):

        """
        Checks future domains.

        If any neighboring cell has
        zero valid candidates,
        fail immediately.
        """

        for r, c in self.get_neighbors(row, col):

            if self.board[r][c] == 0:

                candidates = self.get_candidates(r, c)

                if len(candidates) == 0:
                    return False

        return True

    def solve_forward(self):

        """
        Backtracking + Forward Checking

        Prunes impossible states early.
        """

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

                # Forward checking
                if self.forward_check(r, c):

                    if self.solve_forward():
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

    # ==================================================
    # 4. HILL CLIMBING (LOCAL SEARCH)
    # ==================================================

    def solve_hill(self, max_steps=5000):

        """
        Local Search:
        Hill Climbing

        Starts from random assignment
        and reduces conflicts.
        """

        self.random_fill()

        def cost():

            errors = 0

            # Row conflicts
            for r in range(9):
                errors += 9 - len(set(self.board[r]))

            # Column conflicts
            for c in range(9):

                col = [
                    self.board[r][c]
                    for r in range(9)
                ]

                errors += 9 - len(set(col))

            # Box conflicts
            for br in range(0, 9, 3):
                for bc in range(0, 9, 3):

                    nums = []

                    for r in range(br, br + 3):
                        for c in range(bc, bc + 3):
                            nums.append(self.board[r][c])

                    errors += 9 - len(set(nums))

            return errors

        current = cost()

        mutable = []

        for r in range(9):
            for c in range(9):

                if (r, c) not in self.fixed_cells:
                    mutable.append((r, c))

        for _ in range(max_steps):

            self.states_explored += 1

            r, c = random.choice(mutable)

            old = self.board[r][c]

            self.board[r][c] = random.randint(1, 9)

            new_cost = cost()

            if new_cost <= current:

                current = new_cost

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

        """
        Fill empty cells randomly.
        Used to initialize local search.
        """

        for r in range(9):
            for c in range(9):

                if self.board[r][c] == 0:
                    self.board[r][c] = random.randint(1, 9)
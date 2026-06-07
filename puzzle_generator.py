import random
from copy import deepcopy


class PuzzleGenerator:

    def __init__(self):
        pass

    # ==================================================
    # CHECK VALIDITY
    # ==================================================

    def is_valid(self, board, row, col, num):

        # Row check
        if num in board[row]:
            return False

        # Column check
        for r in range(9):
            if board[r][col] == num:
                return False

        # Box check
        br = (row // 3) * 3
        bc = (col // 3) * 3

        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if board[r][c] == num:
                    return False

        return True

    # ==================================================
    # GENERATE FULL SOLVED BOARD (BACKTRACKING)
    # ==================================================

    def fill_board(self, board):

        for r in range(9):
            for c in range(9):

                if board[r][c] == 0:

                    nums = list(range(1, 10))
                    random.shuffle(nums)

                    for n in nums:

                        if self.is_valid(board, r, c, n):

                            board[r][c] = n

                            if self.fill_board(board):
                                return True

                            board[r][c] = 0

                    return False

        return True

    # ==================================================
    # SOLUTION COUNTER (FOR UNIQUENESS CHECK)
    # ==================================================

    def count_solutions(self, board, limit=2):

        """
        Counts number of solutions.
        Stops early if more than 1 found.
        """

        empty = None

        for r in range(9):
            for c in range(9):

                if board[r][c] == 0:
                    empty = (r, c)
                    break
            if empty:
                break

        if not empty:
            return 1

        r, c = empty
        count = 0

        for num in range(1, 10):

            if self.is_valid(board, r, c, num):

                board[r][c] = num

                count += self.count_solutions(board, limit)

                board[r][c] = 0

                if count >= limit:
                    return count

        return count

    # ==================================================
    # REMOVE CELLS WITH UNIQUENESS GUARANTEE
    # ==================================================

    def remove_cells(self, board, difficulty):

        """
        Removes numbers based on difficulty
        BUT ensures puzzle remains uniquely solvable.
        """

        clues = {
            "easy": 45,
            "medium": 35,
            "hard": 28,
            "expert": 25
        }

        puzzle = deepcopy(board)

        keep = clues.get(difficulty.lower(), 35)

        remove = 81 - keep

        while remove > 0:

            r = random.randint(0, 8)
            c = random.randint(0, 8)

            if puzzle[r][c] == 0:
                continue

            # temporarily remove
            temp = puzzle[r][c]
            puzzle[r][c] = 0

            # check uniqueness
            copy_board = deepcopy(puzzle)

            if self.count_solutions(copy_board, limit=2) != 1:
                # revert (not unique)
                puzzle[r][c] = temp
            else:
                remove -= 1

        return puzzle

    # ==================================================
    # MAIN GENERATE FUNCTION
    # ==================================================

    def generate(self, difficulty):

        """
        Step 1: generate full valid Sudoku solution
        Step 2: remove numbers while keeping uniqueness
        """

        board = [[0 for _ in range(9)] for _ in range(9)]

        self.fill_board(board)

        return self.remove_cells(board, difficulty)
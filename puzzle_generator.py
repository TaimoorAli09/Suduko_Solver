import random
from copy import deepcopy

class PuzzleGenerator:

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, board, row, col, num):

        if num in board[row]:
            return False

        for r in range(9):
            if board[r][col] == num:
                return False

        br = (row // 3) * 3
        bc = (col // 3) * 3

        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if board[r][c] == num:
                    return False

        return True

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

    def remove_cells(self, board, difficulty):

        clues = {"easy": 45, "medium": 35, "hard": 28, "expert": 20}

        puzzle = deepcopy(board)

        keep = clues.get(difficulty.lower(), 35)
        remove = 81 - keep

        while remove > 0:

            r = random.randint(0, 8)
            c = random.randint(0, 8)

            if puzzle[r][c] != 0:
                puzzle[r][c] = 0
                remove -= 1

        return puzzle

    def generate(self, difficulty):

        board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board(board)
        return self.remove_cells(board, difficulty)
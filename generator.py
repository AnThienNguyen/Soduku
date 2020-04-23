from solver import solve, valid, print_board
import random

board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


# generates new board
def generate(bo, nums=20):
    i = 0
    # places random values in 10 random cells
    while i < 10:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        val = random.randint(1, 9)

        # checks if value is valid in cell
        if bo[row][col] == 0 and valid(bo, val, (row, col)):
            bo[row][col] = val
            i += 1

    # populate the rest of the board
    solve(bo)

    # randomly removes/resets value of cells
    x = 81
    while x > nums:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        # only remove if not empty
        if not bo[row][col] == 0:
            bo[row][col] = 0
            x -= 1

# generates random values in a diagonal pattern vs random
def generate2(bo):
    col = 0
    row = 0

    while col < 9:
        val = random.randint(1, 9)

        if bo[row][col] == 0 and valid(bo, val, (row, col)):
            bo[row][col] = val
            col += 1
            row += 1


print_board(board)
generate(board)
print()
print_board(board)

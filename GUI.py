import pygame
# from solver import solve, valid
import time
import random
#from generator import generate
pygame.font.init()


class Grid:
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
    answer = [
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

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.generate()
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def generate(self):
        i = 0
        # places random values in 10 random cells
        while i < 10:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            val = random.randint(1, 9)

            # checks if value is valid in cell
            if self.board[row][col] == 0 and valid(self.board, val, (row, col)):
                self.board[row][col] = val
                i += 1

        self.solve()

        self.answer = [[self.board[i][j] for j in range(self.cols)] for i in range(self.rows)]

        x = 81
        while x > 24:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            # only remove if not empty
            if not self.board[row][col] == 0:
                self.board[row][col] = 0
                x -= 1

    # updates the board/model with the values stored in cubes
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # backtracking algorithm
    def solve(self):
        find = find_empty(self.board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.board, i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                # backtrack to last element
                self.board[row][col] = 0
        return False

    # checks if value is valid before adding it to the board
    def place(self, val, hint=False):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val, hint)
            self.update_model()

            # if valid(self.model, val, (row, col)) and self.solve():
            if self.model[row][col] == self.answer[row][col]:
                self.update_model()
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def hint(self, clue=True):
        found = False
        i = 1
        while not found and i < 10:
            if self.place(i, clue):
                found = True
            i += 1

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Unselect all cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        # selects chosen cell
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # deletes temp value in cell
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_board(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i, True)
                # write in value
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)

                if self.solve_board():
                    return True

                # backtrack to last element
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(50)
        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.hint = False

    def draw(self, win):
        fnt = pygame.font.SysFont("arial", 35)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # temp value
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        # written value
        elif not (self.value == 0):
            if self.hint:
                text = fnt.render(str(self.value), 1, (0, 150, 255))
            else:
                text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        # selected tile
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("arial", 35)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        # change value
        text = fnt.render(str(self.value), 1, (0, 150, 255))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, value, hint=False):
        self.value = value
        self.hint = hint

    def set_temp(self, value):
        self.temp = value


# find next empty spot in board
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


# Check if number is valid in that spot
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    # loop through box
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def redraw_window(win, board, time, strikes, hints):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("arial", 35)

    # Time
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (340, 555))

    # Strikes
    text = font.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 555))

    # Hints
    font = pygame.font.SysFont("arial", 30)
    if hints >= 0:
        text = font.render("o " * hints, 1, (240, 175, 0))
    elif -1 > hints >= -2:
        text = font.render("No more", 1, (240, 125, 0))
    elif -3 > hints >= -4:
        text = font.render("Stop it", 1, (240, 75, 0))
    elif -5 > hints >= -7:
        text = font.render("No >:c", 1, (240, 0, 0))
    else:
        text = font.render("No hints", 1, (240, 125, 0))
    win.blit(text, (200, 555))

    # Grid + Board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    min = secs // 60

    time = (str(min) if min > 9 else "0" + str(min)) + ":" + (str(sec) if sec > 9 else "0" + str(sec))
    return time


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    hints = 3

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solve_board()
                # hints
                if event.key == pygame.K_h:
                    i, j = board.selected
                    if board.cubes[i][j].value == 0:
                        hints -= 1
                        if hints >= 0:
                            start -= 30
                            board.hint()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0 and board.cubes[i][j].value == 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if strikes > 2:
                            print("You Lose")
                            run = False

                        if board.is_finished():
                            print("You won!")
                            run = False

            # clicking on cell
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes, hints)
        pygame.display.update()


main()
pygame.quit()

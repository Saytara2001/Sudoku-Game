import pygame
import math
import Boards
from Button import Button


class Cell:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y


WIDTH = 550
HEIGHT = 650

background_color = (220, 220, 220)
originGridElement_color = (50, 50, 50)
answerGridElement_color = (80, 91, 255)

easyColor = (105, 255, 0)
mediumColor = (246, 255, 0)
hardColor = (255, 0, 0)

whiteColor = (230, 230, 230)
blackColor = (50, 50, 50)
blueColor = (50, 50, 255)
redColor = (255, 50, 50)

isSlowMotion = False
intervalMotion = 100


def CheckValidCellRowAndColumn(board, number, rowIndex, columnIndex):
    return CheckValidCellColumn(board, number, columnIndex) and CheckValidCellRow(board, number, rowIndex)


def CheckValidCellColumn(board, number, columnIndex):
    row = 0
    while row < 9:
        if board[row][columnIndex] == number:
            return False
        row += 1
    return True


def CheckValidCellRow(board, number, rowIndex):
    column = 0
    while column < 9:
        if board[rowIndex][column] == number:
            return False
        column += 1
    return True


# function --> Check If Valid Number In 3x3 Cells
def CheckValid3X3Cells(board, number, rowIndex, columnIndex):
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)

    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            if board[i][j] == number:
                return False
    return True


# function --> Backtracking Algorithm Solution
def BacktrackingSolution(board, myFont, screen, color, orgCells, listOfNumbers=None, row=0, column=0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
    if listOfNumbers is None:
        listOfNumbers = []
    if row == 8 and column == 9:  # check range board
        return listOfNumbers
    elif column == 9:
        row += 1
        column = 0

    if board[row][column] == 0:
        for generatedNumber in range(1, 10):
            if CheckValid3X3Cells(board, generatedNumber, row, column) and \
                    CheckValidCellRowAndColumn(board, generatedNumber, row, column):
                board[row][column] = generatedNumber
                currentCell = Cell(board[row][column], row, column)
                listOfNumbers.append(currentCell)
                if isSlowMotion:
                    PrintDesignBoard(screen)
                    PrintNumbersOnBoard(screen, myFont, orgCells, originGridElement_color)
                    PrintNumbersOnBoard(screen, myFont, listOfNumbers, color)
                    pygame.time.delay(intervalMotion)
                if BacktrackingSolution(board, myFont, screen, color, orgCells, listOfNumbers, row, column + 1) is None:
                    board[row][column] = 0
                    listOfNumbers.remove(currentCell)
                    if isSlowMotion:
                        PrintDesignBoard(screen)
                        PrintNumbersOnBoard(screen, myFont, orgCells, originGridElement_color)
                        PrintNumbersOnBoard(screen, myFont, listOfNumbers, color)
                        pygame.time.delay(intervalMotion)
                else:
                    return listOfNumbers
        if board[row][column] == 0:
            return None
    else:
        return BacktrackingSolution(board, myFont, screen, color, orgCells, listOfNumbers, row, column + 1)

def PrintDesignBoard(screen):
    screen.fill(background_color)
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 5) # color start_postion End_postion
            pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 5)

        pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 1)
        pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 1)


def PrintNumbersOnBoard(screen, myFont, listOfNumbers, color):
    for cell in listOfNumbers:
        value = myFont.render(str(cell.value), True, color)
        screen.blit(value, ((cell.y + 1) * 50 + 15, (cell.x + 1) * 50))
        pygame.display.update()


def main(__level="easy", __slowMotion=False):
    global isSlowMotion
    isSlowMotion = __slowMotion
    originGrid = Boards.easy_board
    if __level == "medium":
        originGrid = Boards.Project_Main_Board
    elif __level == "hard":
        originGrid = Boards.hard_board

    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Backtracking Solver")
    win.fill(background_color)
    myFont = pygame.font.SysFont("Comic Sans MS", 35)
    PrintDesignBoard(win)

    originCells = []
    for i in range(0, len(originGrid[0])):
        for j in range(0, len(originGrid[0])):
            if originGrid[i][j] > 0:
                originCells.append(Cell(originGrid[i][j], i, j))

    PrintNumbersOnBoard(win, myFont, originCells, originGridElement_color)

    copyGrid = [[originGrid[i][j] for j in range(len(originGrid[0]))] for i in range(len(originGrid))]

    isStartedBackTrack = False
    isPrintedFinalSolution = False
    finalSolution = None
    currentState = __level

    half_screen_width = WIDTH / 2
    easy_btn = Button(pygame, win, easyColor, (half_screen_width - (half_screen_width / 2) - 50, 545), font=myFont,
                      text="Easy",
                      text_color=blackColor,
                      hover_color_degree=25)
    medium_btn = Button(pygame, win, mediumColor, (half_screen_width, 545), font=myFont, text="Medium MB",
                        text_color=blackColor,
                        hover_color_degree=25)
    hard_btn = Button(pygame, win, hardColor, (half_screen_width + (half_screen_width / 2) + 50, 545), font=myFont,
                      text="Hard",
                      text_color=blackColor,
                      hover_color_degree=25)
    slow_btn = Button(pygame, win, blueColor, (half_screen_width + (half_screen_width / 2), 610), font=myFont,
                      text="Slow Motion",
                      text_color=whiteColor,
                      hover_color_degree=25)
    back_btn = Button(pygame, win, redColor, (half_screen_width - (half_screen_width / 2), 610), font=myFont,
                      text="Main Menu",
                      text_color=whiteColor,
                      hover_color_degree=25)

    while True:
        if not isPrintedFinalSolution and finalSolution is not None:
            isPrintedFinalSolution = True
            PrintNumbersOnBoard(win, myFont, finalSolution, answerGridElement_color)
            easy_btn.draw_button(True)
            medium_btn.draw_button(True)
            hard_btn.draw_button(True)
            slow_btn.draw_button(True)
            back_btn.draw_button(True)

        easy_btn.update()
        medium_btn.update()
        hard_btn.update()
        slow_btn.update()
        back_btn.update()

        buttonState = ''
        if easy_btn.is_mouse_in():
            buttonState = 'easy'
        elif medium_btn.is_mouse_in():
            buttonState = 'medium'
        elif hard_btn.is_mouse_in():
            buttonState = 'hard'
        elif slow_btn.is_mouse_in():
            buttonState = 'slow'
        elif back_btn.is_mouse_in():
            buttonState = 'main menu'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonState == 'slow':
                    main(currentState, not isSlowMotion)
                    return
                if buttonState == 'main menu':
                    print("Main Menu")
                    return
                if buttonState != '':
                    main(buttonState, isSlowMotion)
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main(__level)
                    return

        if not isStartedBackTrack:
            isStartedBackTrack = True
            finalSolution = BacktrackingSolution(copyGrid, myFont, win, answerGridElement_color, originCells)
            print("Is Finished")

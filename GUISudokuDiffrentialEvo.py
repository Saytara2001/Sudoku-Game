import pygame
import requests
import math
import random
import Boards
import matplotlib.pyplot as plt
from Button import Button


def CheckValidCellRowAndColumn(board, number, rowIndex, columnIndex):
    return CheckValidCellRow(board, number, columnIndex, rowIndex) and CheckValidCellColumn(board, number, rowIndex,
                                                                                            columnIndex)


def CheckValidCellRow(board, number, columnIndex, rowIndex):
    row = 0
    while row < 9:
        if rowIndex == row:
            row += 1
            continue
        if board[row][columnIndex] == number:
            return False
        row += 1
    return True


def CheckValidCellColumn(board, number, rowIndex, columnIndex):
    column = 0
    while column < 9:
        if columnIndex == column:
            column += 1
            continue
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
            if i == rowIndex and j == columnIndex:
                continue
            if board[i][j] == number:
                return False
    return True


class Cell:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y


WIDTH = 1250
HEIGHT = 800

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

intervalMotion = 10

finalSolution = None


def printBoardConsole(board):
    print('=============================')
    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            print(board[row][column], end=' ')
        print('')
    print('=============================')


def copyBoard(copyFrom):
    copyTo = []
    for row in range(0, len(copyFrom)):
        copyTo.append(copyFrom[row].copy())
    return copyTo


# function --> Genetic Algorithm
def population(startedBoard, length):
    pop = []
    for i in range(0, length):
        person = copyBoard(startedBoard)
        for row in range(0, 9):
            for column in range(0, 9):
                if person[row][column] == 0:
                    person[row][column] = int(random.uniform(1, 9))
        pop.append(person)
    return pop


def fitnessRow(board):
    fit = 0
    for row in range(9):
        setRow = set()
        for column in range(9):
            setRow.add(board[row][column])
        fit += 9 - len(setRow)
    return fit


def fitnessColumn(board):
    fit = 0
    for column in range(9):
        setColumn = set()
        for row in range(9):
            setColumn.add(board[row][column])
        fit += 9 - len(setColumn)
    return fit


def fitness9x9(board):
    fit = 0
    for row in range(0, 9, 3):
        for column in range(0, 9, 3):
            fit += fitness3X3Cells(board, row, column)
    return fit


def fitness3X3Cells(board, rowIndex, columnIndex):
    startRow = 3 * math.floor(rowIndex / 3) # 0
    startColumn = 3 * math.floor(columnIndex / 3) # 3
    setNumbers = set()
    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            setNumbers.add(board[i][j])
    return 9 - len(setNumbers)


def fitness(board):
    return fitnessRow(board) + fitnessColumn(board) + fitness9x9(board)


def grade(pop):
    total = [fitness(member) for member in pop]
    return sum(total) / len(pop) * 1.0


def clamp(value):
    value = int(value)
    return 1 if value < 1 else 9 if value > 9 else value


'''
    R = Board1 - Board2
    R = Mutant Rate * R
    R = Board3 + R
    R = Clamp(R) #int([1-9])
'''
def makeMutantVector(board1, board2, board3, orgBoard, mutateRate):
    mutantVector = copyBoard(orgBoard)
    for row in range(9):
        for column in range(9):
            if mutantVector[row][column] == 0:
                mutantVector[row][column] = clamp(
                    board3[row][column] + (mutateRate * (board1[row][column] - board2[row][column]))
                )
    return mutantVector

'''
    Loop On All Members As Member
        1. Select 3 Unique Members
        2. Make Mutant Vector From 3 Unique Members
            Equation: Result = B3 + (M * (B1 - B2))
            Clamp: Result
        3. CrossOver
            Make New Target Board => (Copy Target Board)
            Take CrossOver_Rate% From Mutant Vector To New Target Board
        4. Selection
            Select Between New Target Board And The Main Target Board
            By Fitness
        5. Check If Found Solution => Fitness = 0
            Set FinalSolution = Parents[0] As Best Member
            Return Sorted(Parents) By Fitness
'''
def evolve(parents, orgBoard, mutateRate=.3, crossOverRate=.3):
    global finalSolution

    for targetMemberIndex in range(len(parents)): # [0 -> N] 0 -> Target Board
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        # Select 3 Random Members
        parentsLength = len(parents)
        x1 = x2 = x3 = None
        while x1 == x2 or x1 == x3 or x2 == x3:
            x1 = parents[random.randint(0, parentsLength - 1)]  # 0
            x2 = parents[random.randint(0, parentsLength - 1)]  # 1
            x3 = parents[random.randint(0, parentsLength - 1)]  # 2

        # Mutate Board
        mutantVector = makeMutantVector(x1, x2, x3, orgBoard, mutateRate)

        # Crossover
        targetBoard = copyBoard(orgBoard)
        for row in range(9):
            for column in range(9):
                if orgBoard[row][column] == 0:
                    if crossOverRate >= random.random():
                        targetBoard[row][column] = mutantVector[row][column]
                    else:
                        targetBoard[row][column] = parents[targetMemberIndex][row][column]

        # Selection
        mutantVectorFitness = fitness(targetBoard)
        targetMemberFitness = fitness(parents[targetMemberIndex])
        if targetMemberFitness > mutantVectorFitness:
            parents[targetMemberIndex] = targetBoard

        if fitness(parents[targetMemberIndex]) == 0:
            graded = [(fitness(member), member) for member in parents]
            parents = [x[1] for x in sorted(graded)]
            finalSolution = parents[targetMemberIndex]
            return parents

    return parents


def PrintBoard(screen):
    screen.fill(background_color)
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 5)
            pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 5)

        pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 1)
        pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 1)


def PrintNumbersOnBoard(screen, myFont, listOfNumbers, color):
    for cell in listOfNumbers:
        value = myFont.render(str(cell.value), True, color)
        screen.blit(value, ((cell.y + 1) * 50 + 15, (cell.x + 1) * 50))
        pygame.display.update()


def PrintScores(screen, myFont, generations, gradedValue, currentFitness, fitnessHistory):
    value = myFont.render("Best In Generation: #" + str(generations), True, blackColor)
    screen.blit(value, (525, 50))
    value = myFont.render("Final grade value: " + str(gradedValue), True, blackColor)
    screen.blit(value, (525, 100))
    value = myFont.render("Current fitness: " + str(currentFitness), True, blackColor)
    screen.blit(value, (525, 150))

    if fitnessHistory is not None:
        listX = [x[0] for x in fitnessHistory]
        listY = [x[1] for x in fitnessHistory]
        plt.plot(listY, listX, 'r')
        plt.title("Differential Evolution For Sudoku")
        plt.ylabel("Number of generations")
        plt.xlabel("Fitness")
        plt.savefig("Graphs/image.jpg")
        image = pygame.image.load("Graphs/image.jpg")
        screen.blit(image, (525, 200))
    pygame.display.update()


def DrawRedBlocks(screen, board, orgBoard):
    for row in range(9):
        for column in range(9):
            if orgBoard[row][column] == 0:
                isValidSides = CheckValidCellRowAndColumn(board, board[row][column], row, column)
                isValid3X3 = CheckValid3X3Cells(board, board[row][column], row, column)
                if not isValidSides or not isValid3X3:
                    if not isValidSides:
                        print("Not Valid Sides")
                    if not isValid3X3:
                        print("Not Valid 3X3")
                    print(row, column, ":", board[row][column])
                    pygame.draw.rect(screen, (255, 0, 0), ((column + 1) * 50 + 5, (row + 1) * 50 + 5, 40, 40))


def main(__level="easy", force_start=False):
    global finalSolution
    finalSolution = None
    plt.cla()
    plt.gca().invert_xaxis()

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
    PrintBoard(win)

    originCells = []
    for i in range(0, len(originGrid[0])):
        for j in range(0, len(originGrid[0])):
            if originGrid[i][j] > 0:
                originCells.append(Cell(originGrid[i][j], i, j))

    PrintNumbersOnBoard(win, myFont, originCells, originGridElement_color)

    copyGrid = [[originGrid[i][j] for j in range(len(originGrid[0]))] for i in range(len(originGrid))]

    isStarted = False
    isStartedBefore = False
    isPrintedFinalSolution = False
    evo = 1
    gradedValue = 100
    members = None
    fitnessHistory = None
    buttonState = ""

    printEveryWave = 100
    populationCount = 400
    evolveMaxCount = 100000
    mutateFactor = .3     # [0-2]
    crossOverRate = .3    # [0-1]

    easy_btn = Button(pygame, win, easyColor, (150, 550), font=myFont, text="Easy",
                      text_color=blackColor,
                      hover_color_degree=25)
    medium_btn = Button(pygame, win, mediumColor, (150, 615), font=myFont, text="Medium MB",
                        text_color=blackColor,
                        hover_color_degree=25)
    hard_btn = Button(pygame, win, hardColor, (150, 685), font=myFont, text="Hard",
                      text_color=blackColor,
                      hover_color_degree=25)
    start_btn = Button(pygame, win, redColor, (255, 760), font=myFont, text="Start",
                       text_color=whiteColor,
                       hover_color_degree=25)
    back_btn = Button(pygame, win, redColor, (100, 760), font=myFont, text="Main Menu",
                      text_color=whiteColor,
                      hover_color_degree=25)

    while True:
        if not isPrintedFinalSolution and finalSolution is not None:
            isPrintedFinalSolution = True
            PrintBoard(win)
            PrintNumbersOnBoard(win, myFont, originCells, originGridElement_color)
            PrintNumbersOnBoard(win, myFont, finalSolution, answerGridElement_color)
            PrintScores(win, myFont, evo, gradedValue, fitness(members[0]), fitnessHistory)
            easy_btn.draw_button(True)
            medium_btn.draw_button(True)
            hard_btn.draw_button(True)
            back_btn.draw_button(True)
            start_btn.draw_button(True)

        easy_btn.update()
        medium_btn.update()
        hard_btn.update()
        back_btn.update()
        start_btn.update()

        buttonState = ''
        if easy_btn.is_mouse_in():
            buttonState = 'easy'
        elif medium_btn.is_mouse_in():
            buttonState = 'medium'
        elif hard_btn.is_mouse_in():
            buttonState = 'hard'
        elif back_btn.is_mouse_in():
            buttonState = 'main menu'
        elif start_btn.is_mouse_in():
            buttonState = 'start'

        if force_start:
            force_start = False
            isStarted = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonState == 'main menu':
                    print("Main Menu")
                    return
                elif buttonState == 'start':
                    if not isStartedBefore:
                        isStarted = True
                    else:
                        main(__level, force_start=True)
                elif buttonState != '':
                    main(buttonState)
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main(__level)
                    return

        if isStarted:
            PrintScores(win, myFont, 0, 100.0, 100, fitnessHistory)
            pygame.display.update()
            isStartedBefore = True
            isStarted = False

            members = population(copyGrid, populationCount)
            fitnessHistory = [(evo, grade(members))]

            for x in range(evolveMaxCount):
                members = evolve(members, copyGrid, mutateFactor, crossOverRate)
                gradedValue = grade(members)
                fitnessHistory.append((evo, gradedValue))
                evo += 1
                if evo % printEveryWave == 0:
                    graded = [(fitness(member), member) for member in members]
                    graded = [x[1] for x in sorted(graded)]
                    cells = []
                    for row in range(9):
                        for column in range(9):
                            if copyGrid[row][column] == 0:
                                cells.append(Cell(graded[0][row][column], row, column))
                    PrintBoard(win)
                    PrintNumbersOnBoard(win, myFont, originCells, originGridElement_color)
                    DrawRedBlocks(win, graded[0], originGrid)
                    PrintNumbersOnBoard(win, myFont, cells, answerGridElement_color)
                    PrintScores(win, myFont, evo, gradedValue, fitness(graded[0]), fitnessHistory)
                    easy_btn.draw_button(True)
                    medium_btn.draw_button(True)
                    hard_btn.draw_button(True)
                    back_btn.draw_button(True)
                    print(evo, ": ", gradedValue)

                if finalSolution is not None:
                    newCells = []
                    for i in range(9):
                        for j in range(9):
                            if originGrid[i][j] == 0:
                                newCells.append(Cell(finalSolution[i][j], i, j))
                    finalSolution = newCells
                    break

            print(evo, ": ", gradedValue)
            print("Is Finished")

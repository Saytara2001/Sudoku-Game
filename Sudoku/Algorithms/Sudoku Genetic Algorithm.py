import math
import random
import matplotlib.pyplot as plt

# Very evil hard board
'''
mainBoard = [[0, 0, 0, 0, 1, 0, 0, 4, 0],
             [2, 0, 0, 0, 0, 0, 0, 3, 0],
             [0, 6, 0, 0, 0, 9, 1, 0, 2],
             [7, 0, 0, 0, 5, 0, 6, 0, 1],
             [0, 0, 5, 0, 0, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 4, 0, 0],
             [0, 9, 0, 8, 0, 0, 0, 0, 0],
             [6, 0, 0, 0, 3, 0, 5, 0, 7],
             [0, 0, 0, 0, 0, 0, 0, 2, 0]]
'''
# Main board in project PDF
mainBoard = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 9, 5, 0, 0, 0],
             [0, 9, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]]
'''
mainBoard = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 7, 2, 1, 9, 5, 3, 4, 8],
             [1, 9, 8, 3, 4, 2, 5, 6, 7],
             [8, 5, 9, 7, 6, 1, 4, 2, 3],
             [4, 2, 6, 8, 5, 3, 7, 9, 1],
             [7, 1, 3, 9, 2, 4, 8, 5, 6],
             [9, 6, 1, 5, 3, 7, 2, 8, 4],
             [2, 8, 7, 4, 1, 9, 6, 3, 5],
             [3, 4, 5, 2, 8, 6, 1, 7, 9]]
'''


# function --> Check If Valid Cell
def CheckValidCellRowAndColumn(board, number, rowIndex, columnIndex):
    return CheckValidCellRow(board, number, rowIndex, columnIndex) and CheckValidCellColumn(board, number, rowIndex,
                                                                                            columnIndex)


def CheckValidCellRow(board, number, rowIndex, columnIndex):
    row = 0
    while row < 9:
        if row == rowIndex:
            row += 1
            continue
        if board[row][columnIndex] == number:
            return False
        row += 1
    return True


def CheckValidCellColumn(board, number, rowIndex, columnIndex):
    column = 0
    while column < 9:
        if column == columnIndex:
            column += 1
            continue
        if board[rowIndex][column] == number:
            return False
        column += 1
    return True


def CheckValid3X3Cells(board, number, rowIndex, columnIndex):
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)

    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            if columnIndex == rowIndex:
                continue
            if board[i][j] == number:
                return False
    return True


def printBoard(board):
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


def getNumberOfEmptyCells(board):
    emptyCells = 0
    for row in range(0, 9):
        for column in range(0, 9):
            if board[row][column] == 0:
                emptyCells += 1
    return emptyCells


# function --> Genetic Algorithm
def population(startedBoard, length):
    pop = []
    for i in range(0, length):
        person = copyBoard(startedBoard)
        for row in range(0, 9):
            for column in range(0, 9):
                if person[row][column] == 0:
                    person[row][column] = random.randint(1, 9)
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
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)
    setNumbers = set()
    for i in range(startRow, startRow + 3):
        for j in range(startColumn, startColumn + 3):
            setNumbers.add(board[i][j])

    return 9 - len(setNumbers)


def fitness(board):
    return fitnessRow(board) + fitnessColumn(board) + fitness9x9(board)

'''
def fitness(board):
    fit = 0
    for row in range(0, 9):
        for column in range(0, 9):
            if mainBoard[row][column] == 0:
                if not CheckValidCellRowAndColumn(board, board[row][column], row, column) or \
                        not CheckValid3X3Cells(board, board[row][column], row, column):
                    fit += 1
    return fit
'''

def grade(pop):
    total = [fitness(member) for member in pop]
    return sum(total) / len(pop) * 1.0


def evolve(pop, retain=.2, randomSelect=.05, mutate=.01, numberOfEmptyCells=0):
    graded = [(fitness(member), member) for member in pop]
    graded = [x[1] for x in sorted(graded)]

    # Select
    retainLength = int(len(graded) * retain)  # 10 * .2 = 2  --> 20% Population
    parents = graded[:retainLength]  # 20% Parents of the population

    # Select Randomly
    for member in graded[retainLength:]:  # 80% of population
        if randomSelect > random.random():
            parents.append(member)

    # Mutate
    for member in parents:
        if mutate > random.random():
            posX = random.randint(0, 8)
            posY = random.randint(0, 8)
            while mainBoard[posX][posY] != 0:
                posX = random.randint(0, 8)
                posY = random.randint(0, 8)

            member[posX][posY] = random.randint(1, 9)

    '''
        [2, 3, 4, 6, 8, 9, 2]
        [1, 3, 5, 5, 6, 7, 8]
    '''
    # Crossover
    parentsLength = len(parents)
    desiredLength = len(pop) - parentsLength
    children = []
    while len(children) < desiredLength:
        male = random.randint(0, parentsLength - 1)
        female = random.randint(0, parentsLength - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = round(numberOfEmptyCells / 2)
            changedValues = 0
            child = copyBoard(mainBoard)
            for row in range(0, 9):
                for column in range(0, 9):
                    if mainBoard[row][column] == 0:
                        if changedValues < half:
                            if CheckValidCellRowAndColumn(male, child[row][column], row, column) and \
                                    CheckValid3X3Cells(male, child[row][column], row, column):
                                child[row][column] = male[row][column]
                        else:
                            if CheckValidCellRowAndColumn(female, child[row][column], row, column) and \
                                    CheckValid3X3Cells(female, child[row][column], row, column):
                                child[row][column] = female[row][column]
                        changedValues += 1
                    if changedValues > numberOfEmptyCells:
                        break
                if changedValues > numberOfEmptyCells:
                    break
            children.append(child)

    parents.extend(children)
    return parents


printEveryWave = 1
populationCount = 200
# evolveCount = 100
retain = .2
randomSelect = .1
mutate = .01

evo = 1
members = population(mainBoard.copy(), populationCount)
fitnessHistory = [(evo, grade(members))]
gradedValue = 100
while gradedValue > 5:
    members = evolve(members, retain, randomSelect, mutate, getNumberOfEmptyCells(mainBoard))
    gradedValue = grade(members)
    fitnessHistory.append((evo, gradedValue))
    evo += 1
    if evo % printEveryWave == 0:
        print(evo, ": ", gradedValue)

    if gradedValue == 0:
        print("Found Best Solution At Iteration:", evo)
        break

print(evo, ": ", gradedValue)
'''
for data in fitnessHistory:
    print(data)
'''

printBoard(members[0])

listX = [x[0] for x in fitnessHistory]
listY = [x[1] for x in fitnessHistory]
plt.plot(listY, listX)
plt.show()


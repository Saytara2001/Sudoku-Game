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
# Easy board

mainBoard = [[0, 7, 0, 5, 0, 3, 4, 8, 0],
             [0, 3, 0, 6, 0, 0, 7, 0, 2],
             [0, 0, 0, 8, 7, 0, 0, 1, 6],
             [0, 5, 0, 0, 6, 9, 2, 0, 8],
             [0, 9, 0, 2, 0, 0, 5, 0, 7],
             [4, 0, 0, 0, 0, 0, 0, 0, 1],
             [8, 0, 0, 0, 4, 7, 1, 0, 5],
             [3, 6, 7, 0, 0, 8, 9, 0, 4],
             [0, 0, 4, 0, 2, 0, 0, 0, 3]]

# Main board in project PDF
'''
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

finalSolution = None


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
    startRow = 3 * math.floor(rowIndex / 3)
    startColumn = 3 * math.floor(columnIndex / 3)
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


def makeMutantVector(board1, board2, board3, orgBoard, mutateRate):
    mutantVector = copyBoard(orgBoard)
    for row in range(9):
        for column in range(9):
            if mutantVector[row][column] == 0:
                mutantVector[row][column] = clamp(
                    board3[row][column] + (mutateRate * (board1[row][column] - board2[row][column]))
                )
    return mutantVector


def evolve(parents, orgBoard, mutateRate=.3, crossOverRate=.3):
    global finalSolution

    for targetMemberIndex in range(len(parents)):  # [0 -> N]    0 -> Target Board
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


printEveryWave = 100
populationCount = 200
evolveCount = 200000
mutate = .3
crossOver = .4

evo = 1
members = population(mainBoard.copy(), populationCount)
fitnessHistory = [(evo, grade(members))]

gradedValue = 100
for x in range(evolveCount):
    members = evolve(members, mainBoard, mutate, crossOver)
    gradedValue = grade(members)
    fitnessHistory.append((evo, gradedValue))
    evo += 1
    if evo % printEveryWave == 0:
        print(evo, ": ", gradedValue)

    if finalSolution is not None:
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
plt.title("Differential Evolution For Sudoku")
plt.ylabel("Number of generations")
plt.xlabel("Fitness")
plt.show()

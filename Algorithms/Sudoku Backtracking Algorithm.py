import math

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


# function --> Check If Valid Number In Row And Column
def CheckValidCellRowAndColumn(board, number, rowIndex, columnIndex):
    return CheckValidCellRow(board, number, columnIndex) and CheckValidCellColumn(board, number, rowIndex)


def CheckValidCellRow(board, number, columnIndex):
    row = 0
    while row < 9:
        if board[row][columnIndex] == number:
            return False
        row += 1
    return True


def CheckValidCellColumn(board, number, rowIndex):
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
def BacktrackingSolution(board, row=0, column=0):
    if row == 8 and column == 9:
        return True
    elif column == 9:
        row += 1
        column = 0

    if board[row][column] == 0:
        for generatedNumber in range(1, 10):
            if CheckValid3X3Cells(board, generatedNumber, row, column) and \
                    CheckValidCellRowAndColumn(board, generatedNumber, row, column):
                # print(generatedNumber, '->', row, ',', column)
                board[row][column] = generatedNumber
                if BacktrackingSolution(board, row, column + 1) is None:
                    # print(0, '->', row, ',', column)
                    board[row][column] = 0
                else:
                    return True
        if board[row][column] == 0:
            return None
    else:
        return BacktrackingSolution(board, row, column + 1)


'''BacktrackingSolution(mainBoard)
for x in mainBoard:
    print(x)'''

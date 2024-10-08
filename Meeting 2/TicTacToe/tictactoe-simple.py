import random
import copy as cp

class Cell:
    def __init__(self, position, location, max_val, min_val):
        self.position = position
        self.location = location
        self.min_val = min_val
        self.max_val = max_val

def generate_cells(board):
    uboard = cp.deepcopy(board)
    for i in range(len(uboard)):
        for j in range(len(uboard[i])):
            if uboard[i][j] != 'X' and uboard[i][j] != 'O':
                uboard[i][j] = Cell(uboard[i][j], [i,j], 0, 0)
                uboard[i][j].max_val = max_val(board, [i, j])
                uboard[i][j].min_val = min_val(board, [i, j])
                uboard[i][j] = [uboard[i][j].position, uboard[i][j].max_val, uboard[i][j].min_val]
    return uboard

def max_val(board, location):
    maxval = 0
    if board[location[0]][location[1]] != 'O' and board[location[0]][location[1]] != 'X':
        maxval += check_horizontal(board, location[0], 'max')
        maxval += check_vertical(board, location[1], 'max')
        maxval += left_diagonal(board, location[0], location[1], 'max')
        maxval += right_diagonal(board, location[0], location[1], 'max')
    return maxval

def min_val(board, location):
    minval = 0
    if board[location[0]][location[1]] != 'O' and board[location[0]][location[1]] != 'X':
        minval -= check_horizontal(board, location[0], 'min')
        minval -= check_vertical(board, location[1], 'min')
        minval -= left_diagonal(board, location[0], location[1], 'min')
        minval -= right_diagonal(board, location[0], location[1], 'min')
    return minval

def check_horizontal(board, row, u_type):
    opposed = 'X' if u_type == 'max' else 'O'
    sign = 'O' if u_type == 'max' else 'X'
    v = 0
    unfilled = 0
    for i in range(3):
        if board[row][i] != opposed:
            unfilled += 1
            if board[row][i] == sign:
                v += 1
    if unfilled == 3:
        v = 10 if v == 2 else v + 1
    else:
        v = 0
    return v

def check_vertical(board, col, u_type):
    opposed = 'X' if u_type == 'max' else 'O'
    sign = 'O' if u_type == 'max' else 'X'
    v = 0
    unfilled = 0
    for i in range(3):
        if board[i][col] != opposed:
            unfilled += 1
            if board[i][col] == sign:
                v += 1
    if unfilled == 3:
        v = 10 if v == 2 else v + 1
    else:
        v = 0
    return v

def left_diagonal(board, row, col, u_type):
    opposed = 'X' if u_type == 'max' else 'O'
    sign = 'O' if u_type == 'max' else 'X'
    v = 0
    unfilled = 0
    if row == col:
        for i in range(3):
            if board[i][i] != opposed:
                unfilled += 1
                if board[i][i] == sign:
                    v += 1
    if unfilled == 3:
        v = 10 if v == 2 else v + 1
    else:
        v = 0
    return v

def right_diagonal(board, row, col, u_type):
    opposed = 'X' if u_type == 'max' else 'O'
    sign = 'O' if u_type == 'max' else 'X'
    v = 0
    unfilled = 0
    state = False
    for i in range(len(board)):
        if board[i][abs(i-2)] == board[row][col]:
            state = True
        if board[i][abs(i-2)] != opposed:
            unfilled += 1
            if board[i][abs(i-2)] == sign:
                v += 1
    if unfilled == 3 and state:
        v = 10 if v == 2 else v + 1
    else:
        v = 0
    return v

def dispUboard(uboard):
    print('\nUtility Board:\n')
    count = 0
    for i in range(len(uboard)):
        for j in range(len(uboard[i])):
            count += 1
            print(uboard[i][j], end='     ' if count % 3 == 0 else '  ')
        print()

def checkWin(board, sign):
    return checkHorizontal(board, sign) or checkVertical(board, sign) or checkDiagonal(board, sign)

def checkTie(board):
    return all(board[i][j] == 'O' or board[i][j] == 'X' for i in range(3) for j in range(3))

def checkDiagonal(board, sign):
    return all(board[i][i] == sign for i in range(3)) or all(board[i][2-i] == sign for i in range(3))

def checkHorizontal(board, sign):
    return any(all(board[i][j] == sign for j in range(3)) for i in range(3))

def checkVertical(board, sign):
    return any(all(board[j][i] == sign for j in range(3)) for i in range(3))

def dispboard(board):
    print('\nTictactoe Board:\n')
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            count += 1
            print(board[i][j], end='  ')
            if count % 3 == 0:
                print()

def checkCompatible(board, move, sign):
    i = 2 if move > 5 else 1 if move > 2 else 0
    loc = [i, move - (i * 3)]
    if board[loc[0]][loc[1]] == move:
        board[loc[0]][loc[1]] = sign
        return True
    print("Please select an empty spot and try again.")
    return False

def minimax_algorithm(board, depth, is_maximizing, alpha, beta):
    if checkWin(board, 'O'):
        return 10 - depth
    if checkWin(board, 'X'):
        return depth - 10
    if checkTie(board):
        return 0
    
    if is_maximizing:
        best_value = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    temp = board[i][j]
                    board[i][j] = 'O'
                    value = minimax_algorithm(board, depth + 1, False, alpha, beta)
                    board[i][j] = temp
                    best_value = max(best_value, value)
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
        return best_value
    else:
        best_value = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    temp = board[i][j]
                    board[i][j] = 'X'
                    value = minimax_algorithm(board, depth + 1, True, alpha, beta)
                    board[i][j] = temp
                    best_value = min(best_value, value)
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
        return best_value

def computerDecision(board):
    while not checkTie(board) and not checkWin(board, 'X'):
        dispboard(board)

        best_value = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    temp = board[i][j]
                    board[i][j] = 'O'
                    move_value = minimax_algorithm(board, 0, False, -float('inf'), float('inf'))
                    board[i][j] = temp
                    if move_value > best_value:
                        best_value = move_value
                        best_move = [i, j]

        if best_move:
            checkCompatible(board, best_move[0] * 3 + best_move[1], 'O')

        if checkTie(board):
            dispboard(board)
            play_again = input("\nThis is a tie game, to play again enter any key, otherwise enter 'q' to quit.\nYour decision: ")
            if play_again == 'q':
                return
            else:
                board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
                GameInitializer(board)

        elif checkWin(board, 'O'):
            dispboard(board)
            print("The computer won!")
            return
        else:
            playerDecision(board)

def playerDecision(board):
    while not checkTie(board) and not checkWin(board, 'O'):
        dispboard(board)
        player_decision = int(input("\n(The player's turn) Enter the empty position you want to place your 'X': "))

        if checkCompatible(board, player_decision, 'X'):
            if checkTie(board):
                dispboard(board)
                play_again = input("\nThis is a tie game, if you want to play again enter 'p', to quit enter any key.\nYour decision: ")
                if play_again == 'q':
                    return
                else:
                    board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
                    GameInitializer(board)

            elif checkWin(board, 'X'):
                dispboard(board)
                print("The player won!")
                return
            else:
                computerDecision(board)

def GameInitializer(board):
    choice = input("\nDo you want to go first or the computer goes first?\nEnter 'c' for computer first, or 'p' if you would like to go first\nYour Choice: ")
    if choice == 'c':
        computerDecision(board)
    elif choice == 'p':
        playerDecision(board)
    else:
        print("\nPlease enter 'c' or 'p' and try again.")
        GameInitializer(board)

# Start the game
init_board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
GameInitializer(init_board)

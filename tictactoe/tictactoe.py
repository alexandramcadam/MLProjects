"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    turn = 0

    for row in board:
        for space in row:
            if not space == None:
                turn+=1

    c = turn % 2 #gives remainder

    if c == 0:
        return X #even
    else:
        return O #odd




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # i row
    # j col

    actions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                action = (i,j)
                actions.append(action)

    return actions





def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    newBoard = copy.deepcopy(board)
    i = action[0]
    j = action [1]

    if not newBoard[i][j] == None:
        raise ValueError
    else:
        newBoard[i][j] = player(board)

    return newBoard






def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #check for 3 in a row
    #two diagonals, 3 rows, 3 cols

    #rows
    for x in range(3):
        if board[x][0] == board[x][1] == board[x][2] is not None:
            return board[x][0]

    #cols
    for x in range(3):
        if board[0][x] == board[1][x] == board[2][x] is not None:
            return board[0][x]

    #diags
    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]

    #no winners
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    win = winner(board)

    if win == O or win == X:
        return True
    else:
        finish = True
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    finish = False
        return finish




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0




#function for minimax
def MaxValue(s):
    if terminal(s) == True:
        return utility(s)
    else:
        v = -(math.inf)
        for a in actions(s):
            v = max(v, MinValue(result(s, a)))
        return v

#function for minimax
def MinValue(s):
    if terminal(s) == True:
        return utility(s)
    else:
        v = math.inf
        for a in actions(s):
            v = min(v, MaxValue(result(s, a)))
        return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    done = terminal(board)
    turn = player(board)
    optimalA = (None,None)

    if done == True:
        return None

    elif turn == X:
        maxV = -(math.inf)
        for a in actions(board):
            v = MinValue(result(board, a))
            if v > maxV:
                optimalA = a
                maxV = v
        return optimalA

    elif turn == O:
        minV = math.inf
        for a in actions(board):
            v = MaxValue(result(board, a))
            if v < minV:
                optimalA = a
                minV = v
        return optimalA

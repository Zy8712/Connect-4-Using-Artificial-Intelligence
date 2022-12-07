# use math library if needed
import math # import math library
import random # import random library for random value selection
from datetime import datetime # allow program to access system time

##################################
# Course: EECS3401
# Assessment: Project 2
# Student Name: Bryan Li
# Student ID: [Hidden for Privacy Reasons]
# Professor: Archit Garg
# Due Date: 11/28/2021 11:59pm
##################################

# ******* IMPORTANT NOTES ******* #
# From Prof on Course Discord #
# Implementing the 3 algorithms in working condition is enough to get  #
# almost full marks. You are not allowed to add more parameters to the #
# definitions of minimax, alphabeta, and expectimax. But you can make  #
# such additions to the subfunctions: value, max_value, and min_value. #


def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    # Initialize the value of scores
    # [s0, s1, s2, s3, --s4--]
    # s0 for the case where all slots are empty in a 4-slot segment
    # s1 for the case where the player occupies one slot in a 4-slot line, the rest are empty
    # s2 for two slots occupied
    # s3 for three
    # s4 for four
    score = [0]*5
    adv_score = [0]*5

    # Initialize the weights
    # [w0, w1, w2, w3, --w4--]
    # w0 for s0, w1 for s1, w2 for s2, w3 for s3
    # w4 for s4
    weights = [0, 1, 4, 16, 1000]

    # Obtain all 4-slot segments on the board
    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        # col
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved): 
        # backslash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################

    # Inner functions value, max_value, min_value written by following the
    # pseudocode provided in Lecture 6 Slide 17.

    # Main inner function. Checks conditions to see whether to call max_value, min_value, or neither.
    def value(player, board, depth_limit):
        # Checks to see if state is a terminal state
        if depth_limit == 0 or board.terminal(): 
            return [0, evaluate(player, board)] # Return the state's utility
        # Checks to see if player is max player
        if player == max_player:
            return max_value(player, board, depth_limit) # Return max-value(state)
        # If player is not max player, they are the min player
        else:
            return min_value(player, board, depth_limit) # Return min-value(state)
    
    def max_value(player, board, depth_limit):
        # Base Case
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        v = -math.inf # initialize variable v and set equal to negative infinity
        num_column_move = 0 # intialize column move value to zero
        # Iterative Case. Iterates through list of all possible successor boards.
        for col,bor in get_child_boards(player, board): # Iterate.
            v = max(v, value(next_player, bor, depth_limit-1)[1]) # v = max(v, value(successor))
            if v == value(next_player, bor, depth_limit-1)[1]: # checks for equality
                num_column_move = col # set column move value to current value of col
        return v, num_column_move # return values v and num_column_move

    def min_value(player, board, depth_limit):
        # Base Case
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        v = math.inf # initialize variable v and set equal to positive infinity
        num_column_move = 0 # intialize column move value to zero
        # Iterative Case. Iterates through list of all possible successor boards.
        for col,bor in get_child_boards(player, board): # Iterate.
            v = min(v, value(next_player, bor, depth_limit-1)[1]) # v = min(v, value(successor))
            if v == value(next_player, bor, depth_limit-1)[1]: # checks for equality
                num_column_move = col # set column move value to current value of col
        return v, num_column_move # return values v and num_column_move

    # determine which player is next
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = value(player, board, depth_limit)[1] # get column placement move for player
    score = -math.inf # sets score equal to negative infinity
###############################################################################
    return placement # return column placement


def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.

     Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    alpha: float
    beta: float
    max_player: boolean


    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################

    # Inner functions value, max_value, min_value written by following the
    # pseudocode provided in Lecture 6 Slide 26.

    # Main inner function. Checks conditions to see whether to call max_value, min_value, or neither.
    def value(player, board, depth_limit, alpha, beta):
        # Checks to see if state is a terminal state
        if depth_limit == 0 or board.terminal():
            return [0, evaluate(player, board)] # Return the state's utility
        # Checks to see if player is max player
        if player == max_player:
            return max_value(player, board, depth_limit, alpha, beta) # Return max-value(state)
        # If player is not max player, they are the min player
        else:
            return min_value(player, board, depth_limit, alpha, beta) # Return min-value(state)

    def max_value(player, board, depth_limit, alpha, beta):
        # Base Case.
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        v = -math.inf # initialize variable v and set equal to negative infinity
        num_column_move = 0 # intialize column move value to zero
        # Iterative Case. Iterates through list of all possible successor boards.
        for col,bor in get_child_boards(player, board): # Iterate.
            v = max(v, value(next_player, bor, depth_limit-1, alpha, beta)[1]) # v = max(v, value(successor,a,b))
            if v == value(next_player, bor, depth_limit-1, alpha, beta)[1]: # checks for equality
                num_column_move = col # set column move value to current value of col
            if v >= beta: # check if v >= b
                return v, num_column_move # return values v and num_column_move
            alpha = max(alpha, v) # set a = max(a,v)
        return v, num_column_move # return values v and num_column_move
    
    def min_value(player, board, depth_limit, alpha, beta):
        # Base Case.
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        v = math.inf # initialize variable v and set equal to positive infinity
        num_column_move = 0 # intialize column move value to zero
        # Iterative Case. Iterates through list of all possible successor boards.
        for col,bor in get_child_boards(player, board): # Iterate.
            v = min(v, value(next_player, bor, depth_limit-1, alpha, beta)[1]) # v = min(v, value(successor,a,b))
            if v == value(next_player, bor, depth_limit-1, alpha, beta)[1]: # checks for equality
                num_column_move = col # set column move value to current value of col
            if v <= alpha: # check if v <= a
                return v, num_column_move # return values v and num_column_move
            beta = min(beta, v) # set B = min(B,v)
        return v, num_column_move # return values v and num_column_move

    # intialize varaibles
    alpha = float('-inf') # declare/intialize alpha value, set to negative infinity
    beta = float('inf') # declare/intialize beta value, set to positive infinity
    # determine which player is next
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = value(player, board, depth_limit, alpha, beta)[1] # get column placement move for player
    score = -math.inf # sets score equal to negative infinity
###############################################################################
    return placement # return column placement


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm.
    We assume that the adversary of the initial player chooses actions
    uniformly at random.
    Say that it is the turn for Player 1 when the function is called initially,
    then, during search, Player 2 is assumed to pick actions uniformly at
    random.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################

    # Inner functions value, max_value, min_value written by following the
    # pseudocode provided in Lecture 7 Slide 5.

    # Main inner function. Checks conditions to see whether to call max_value, min_value, or neither.
    def value(player, board, depth_limit):
        # Checks to see if state is a terminal state
        if depth_limit == 0 or board.terminal():
            return [0, evaluate(player, board)] # Return the state's utility
        # Checks to see if player is max player
        if player == max_player:
            return max_value(player, board, depth_limit) # Return max-value(state)
        # If player is not max player, they are the chance player
        else:
            return exp_value(player, board, depth_limit) # Return exp-value(state)

    def max_value(player, board, depth_limit):
        # Base Case.
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        v = -math.inf # initialize variable v and set equal to negative infinity
        num_column_move = 0 # intialize column move value to zero
        # Iterative Case. Iterates through list of all possible successor boards.
        for col,bor in get_child_boards(player, board): # Iterate.
            v = max(v, value(next_player, bor, depth_limit-1)[1]) # v = max(v, value(successor))
            if v == value(next_player, bor, depth_limit-1)[1]: # checks for equality
                num_column_move = col # set column move value to current value of col
        return v, num_column_move # return values v and num_column_move

    def exp_value(player, board, depth_limit): # (EXTRA COMMENTED CONTENTS IS VARIOUS OTHER RANDOMIZING TECHNIQUES I TRIED)
        v = 0 # intialize v and seo value equal to zero
        num_column_move = 0 # intialize column move value to zero
        poss_list = [] # declare list for possible columns to randomize into
        #sumValue = 0
        #sys_random = random.SystemRandom()
        #Base Case.
        if depth_limit == 0: # If we've reach the bottom of depth-limited search.
            return evaluate(player, board) # Return value from evaluate function.
        # Iterative Case. Iterates through all columns of the board.
        for col in range(board.cols): # Iterate.
            if board.placeable(col): # Check if there is still space in the column.
                poss_list.append(col) # Add column number to the list.
                #sumValue += col
        #random.shuffle(poss_list)
        random.seed(datetime.now()) # set up seed for random num generator
        if (len(poss_list) > 0): # ensure that there some possible moves left
            #num_column = sys_random.choice(poss_list)
            #num_column = poss_list[0]
            num_column_move = random.choice(poss_list) # set column move value to random possible move
        #num_column = sumValue / len(poss_list)
        return v, num_column_move # return values v and num_column_move        
        
    # determine which player is next
    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    placement = value(player, board, depth_limit)[1] # get column placement move for player
    score = -math.inf # sets score equal to negative infinity
###############################################################################
    return placement # return column placement

# MAIN METHOD/FUNCTION.
if __name__ == "__main__":
    from game_gui import GUI
    import tkinter

    algs = { # array of algorithm options and functios connected to them
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    GUI(algs, root)
    root.mainloop()

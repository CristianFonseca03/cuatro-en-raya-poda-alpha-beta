import random

def create_board():
    """Create a 7x6 Connect Four board."""
    return [['.' for _ in range(7)] for _ in range(6)]

def print_board(board):
    """Print the Connect Four board."""
    for row in board:
        print(' '.join(row))
    print('0 1 2 3 4 5 6')  # Column indices

def drop_piece(board, column, piece):
    """Drop a piece in the specified column."""
    for row in reversed(board):
        if row[column] == '.':
            row[column] = piece
            return True
    return False

def is_valid_location(board, column):
    """Check if the column is a valid location to drop a piece."""
    return board[0][column] == '.'

def check_win(board, piece):
    """Check if the current piece has won the game."""
    # Check horizontal locations
    for c in range(4):
        for r in range(6):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check vertical locations
    for c in range(7):
        for r in range(3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(4):
        for r in range(3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(4):
        for r in range(3, 6):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def alpha_beta_pruning(board, depth, alpha, beta, maximizingPlayer):
    """Implement the Alpha-Beta pruning algorithm."""
    # Base case: Check for terminal state (win, lose, draw, or max depth)
    if depth == 0 or check_win(board, 'O') or check_win(board, 'X'):
        return None, score_position(board, 'O')

    if maximizingPlayer:
        value = float('-inf')
        column = random.choice([c for c in range(7) if is_valid_location(board, c)])
        for col in range(7):
            if is_valid_location(board, col):
                row = next(r for r in range(6) if board[r][col] == '.')
                b_copy = [row[:] for row in board]
                drop_piece(b_copy, col, 'O')
                new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value
    else:
        value = float('inf')
        column = random.choice([c for c in range(7) if is_valid_location(board, c)])
        for col in range(7):
            if is_valid_location(board, col):
                row = next(r for r in range(6) if board[r][col] == '.')
                b_copy = [row[:] for row in board]
                drop_piece(b_copy, col, 'X')
                new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return column, value

def score_position(board, piece):
    """Score the board position for the AI."""
    score = 0

    # Score center column (AI prefers center moves)
    center_array = [i[3] for i in board]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Check horizontal
    for r in range(6):
        row_array = board[r]
        for c in range(4):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Check vertical
    for c in range(7):
        col_array = [i[c] for i in board]
        for r in range(3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Check positively sloped diagonals
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Check negatively sloped diagonals
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    """Evaluate a window of four cells for scoring."""
    score = 0
    opp_piece = 'X' if piece == 'O' else 'O'

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count('.') == 1:
        score += 5
    elif window.count(piece) == 2 and window.count('.') == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count('.') == 1:
        score -= 4

    return score

def play_game():
    """Play a game of Connect Four."""
    board = create_board()
    game_over = False
    turn = 0  # Player starts first

    while not game_over:
        # Player's turn
        if turn == 0:
            print_board(board)
            col = int(input("Player 1 Make your Selection (0-6):"))
            if is_valid_location(board, col):
                drop_piece(board, col, 'X')

                if check_win(board, 'X'):
                    print_board(board)
                    print("Player 1 wins!")
                    game_over = True
                turn += 1
                turn = turn % 2

        # AI's turn
        else:
            col, _ = alpha_beta_pruning(board, 5, float('-inf'), float('inf'), True)
            if is_valid_location(board, col):
                drop_piece(board, col, 'O')

                if check_win(board, 'O'):
                    print_board(board)
                    print("AI wins!")
                    game_over = True
                turn += 1
                turn = turn % 2

play_game()


# For testing, let's make the AI make a move on an empty board
# board = create_board()
# ai_column, _ = alpha_beta_pruning(board, 5, float('-inf'), float('inf'), True)
# drop_piece(board, ai_column, 'O')
# print_board(board)


# # Let's test the basic board functions
# board = create_board()
# print_board(board)
# drop_piece(board, 3, 'X')
# print_board(board)
# print("Check win for 'X':", check_win(board, 'X'))

import random

def create_board():
    return [['.' for _ in range(7)] for _ in range(6)]

def print_board(board):
    for row in board:
        print(' '.join(row))
    print('0 1 2 3 4 5 6') 

def drop_piece(board, column, piece):
    for row in reversed(board):
        if row[column] == '.':
            row[column] = piece
            return True
    return False

def is_valid_location(board, column):
    return board[0][column] == '.'

def check_win(board, piece):
    for c in range(4):
        for r in range(6):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(7):
        for r in range(3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(4):
        for r in range(3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(4):
        for r in range(3, 6):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def alpha_beta_pruning(board, depth, alpha, beta, maximizingPlayer):
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
    score = 0
    center_array = [i[3] for i in board]
    center_count = center_array.count(piece)
    score += center_count * 3
    for r in range(6):
        row_array = board[r]
        for c in range(4):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)
    for c in range(7):
        col_array = [i[c] for i in board]
        for r in range(3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
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
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        if turn == 0:
            print_board(board)
            try:
                col = int(input("Ingrese columna: "))
            except ValueError:
                print("Columna no valida")
                continue
            if(col < 0 or col > 6):
                print("Columna no valida")
                continue
            if is_valid_location(board, col):
                drop_piece(board, col, 'X')

                if check_win(board, 'X'):
                    print_board(board)
                    print("jugador gana!") 
                    game_over = True
                turn += 1
                turn = turn % 2
            else:
                print("Columna no valida")
        else:
            col, _ = alpha_beta_pruning(board, 5, float('-inf'), float('inf'), True)
            if is_valid_location(board, col):
                drop_piece(board, col, 'O')

                if check_win(board, 'O'):
                    print_board(board)
                    print("IA gana!")
                    game_over = True
                turn += 1
                turn = turn % 2

play_game()

import math
import random
import time

EMPTY = "."
PLAYER_X = "X"
PLAYER_O = "O"
# get dynamic size
#def get_board_size():
    #while True:
        #try:
           # size = int(input("Enter board size (e.g., 15 for 15x15 board): "))
           # if 5 <= size <= 19:
                #return size
            #else:
               # print("Please enter a size between 5 and 30.")
        #except ValueError:
           # print("Invalid input. Please enter an integer.")

BOARD_SIZE = 15
WIN_LENGTH = 5

class GomokuBoard:
    def __init__(self, size):
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.size = size

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def is_within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_winner(self, player):
        for x in range(self.size):
            for y in range(self.size):
                if (self.check_direction(x, y, 1, 0, player) or
                        self.check_direction(x, y, 0, 1, player) or
                        self.check_direction(x, y, 1, 1, player) or
                        self.check_direction(x, y, 1, -1, player)):
                    return True

        return False

    def check_direction(self, x, y, dx, dy, player):
        count = 0
        for _ in range(WIN_LENGTH):
            if self.is_within_bounds(x, y) and self.board[x][y] == player:
                count += 1
                x += dx
                y += dy
            else:
                break
        return count == WIN_LENGTH

    # Returns a list of valid adjacent moves or the center if no moves are available.
    def get_valid_moves(self):
        moves = set()
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != EMPTY:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if self.is_within_bounds(nx, ny) and self.board[nx][ny] == EMPTY:
                                moves.add((nx, ny))
        if not moves:
            return [(self.size // 2, self.size // 2)]
        return list(moves)


    # Evaluates the board state for the given player by counting lines of consecutive stones
    # It adds score for helpful lines and subtracts for opponent's lines.
    # The score helps the AI algoritm determine the best move. acts as (utility)

    def evaluate(self, player):
        score = 0
        opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
        weight = [0, 1, 10, 100, 1000, 100000]

        for x in range(self.size):
            for y in range(self.size):
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    my_count, opp_count = 0, 0
                    for i in range(WIN_LENGTH):
                        nx, ny = x + dx * i, y + dy * i
                        if not self.is_within_bounds(nx, ny):
                            break
                        if self.board[nx][ny] == player:
                            my_count += 1
                        elif self.board[nx][ny] == opponent:
                            opp_count += 1
                    if my_count > 0 and opp_count == 0:
                        score += weight[my_count]
                    elif opp_count > 0 and my_count == 0:
                        score -= weight[opp_count] * 1.5
        return score

#implementation of alpha-beta

def alpha_beta(board, depth, maximizing_player, player, alpha, beta):
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X

    if depth == 0 or board.is_winner(player) or board.is_winner(opponent):
        return board.evaluate(player), None

    best_move = None
    if maximizing_player:
        max_eval = -math.inf
        for move in board.get_valid_moves():
            x, y = move
            board.board[x][y] = player
            eval_score, _ = alpha_beta(board, depth - 1, False, player, alpha, beta)
            board.board[x][y] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in board.get_valid_moves():
            x, y = move
            board.board[x][y] = opponent
            eval_score, _ = alpha_beta(board, depth - 1, True, player, alpha, beta)
            board.board[x][y] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move




#implementation of  mimimax

def minimax(board, depth, maximizing_player, player):
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X

    if depth == 0 or board.is_winner(player) or board.is_winner(opponent):
        return board.evaluate(player), None

    best_move = None
    if maximizing_player:
        max_eval = -math.inf
        for move in board.get_valid_moves():
            x, y = move
            board.board[x][y] = player
            eval_score, _ = minimax(board, depth - 1, False, player)
            board.board[x][y] = EMPTY
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in board.get_valid_moves():
            x, y = move
            board.board[x][y] = opponent
            eval_score, _ = minimax(board, depth - 1, True, player)
            board.board[x][y] = EMPTY
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


# function to initate ai vs ai game (minimax vs alpha)
def play_ai_vs_ai_minimax_vs_alphabeta():
    board = GomokuBoard(BOARD_SIZE)
    move_count = 0
    current_player = PLAYER_X
    max_moves = BOARD_SIZE * BOARD_SIZE

    while move_count < max_moves:
        print(f"Turn: {current_player}")
        if current_player == PLAYER_X:
             _, move = minimax(board, depth=3, maximizing_player=True, player=current_player)
        else:
             _, move = alpha_beta(board, depth=3, alpha=-math.inf, beta=math.inf, maximizing_player=True, player=current_player)

        if move is None:
            break
        x, y = move
        print(f"{current_player} chooses: ({x}, {y})")
        board.board[x][y] = current_player
        board.print_board()

        if board.is_winner(current_player):
            print(f"{current_player} wins!")
            return

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
        move_count += 1
        time.sleep(0.3)

    print("Game over! It's a draw.")
# function to initate human vs ai game (minimax vs human )
def play_human_vs_ai(human_player=PLAYER_X):
    board = GomokuBoard(BOARD_SIZE)
    ai_player = PLAYER_O if human_player == PLAYER_X else PLAYER_X
    current_player = PLAYER_X
    move_count = 0
    max_moves = BOARD_SIZE * BOARD_SIZE

    while move_count < max_moves:
        print(f"Turn: {current_player}")
        board.print_board()

        if current_player == human_player:
            x, y = get_human_move(board)
        else:
            _, move = minimax(board, depth=3, maximizing_player=True, player=ai_player)
            if move is None:
                break
            x, y = move
            print(f"AI chooses: {x}, {y}")
            time.sleep(0.5)

        board.board[x][y] = current_player

        if board.is_winner(current_player):
            board.print_board()
            print(f"{current_player} wins!")
            return

        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
        move_count += 1

    print("Game over! It's a draw by evaluation.")






# function to control human inputs during play
def get_human_move(board):
    while True:
        try:
            move = input("Enter your move (row, col): ")
            x, y = map(int, move.split(","))
            if board.is_within_bounds(x, y) and board.board[x][y] == EMPTY:
                return x, y
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and column as two integers separated by a comma.")

def main():
    game_type = input("Choose game type (1 for Human vs AI, 2 for AI vs AI): ")

    if game_type == "1":
        human_player = input("Choose your player (X or O): ").upper()
        if human_player not in [PLAYER_X, PLAYER_O]:
            print("Invalid choice. Defaulting to X.")
            human_player = PLAYER_X
        play_human_vs_ai(human_player)
    elif game_type == "2":
        play_ai_vs_ai_minimax_vs_alphabeta()

    else:
        print("Invalid choice. Please select either 1 or 2.")


if __name__ == "__main__":
    main()


#class GomokuBoard:
#   def __init__(self, size=15):
#      self.size = size
#     self.board = [["." for _ in range(size)] for _ in range(size)]

# def print_board(self):
#    for row in self.board:
#       print(" ".join(row))

# def is_valid_move(self, row, col):
#    return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == "."

#def make_move(self, row, col, symbol):
#   if self.is_valid_move(row, col):
#      self.board[row][col] = symbol
#     return True
#return False


#this for testing
#board = GomokuBoard()

#board.print_board()# initail empty board


#board.make_move(0, 0, "X")
#board.make_move(1, 1, "O")
#board.make_move(14, 14, "X")


#x = board.make_move(0, 0, "O")
#print("Move success:", x) #should return flase as 0,0 already has x
#y=board.make_move(0,1,'x')
#print(y)

#print("\nUpdated board:")
#board.print_board()

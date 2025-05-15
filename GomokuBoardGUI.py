import tkinter as tk
from tkinter import messagebox
import math
import time
import threading

EMPTY = ""
PLAYER_BLUE = "BLUE"
PLAYER_PINK = "PINK"
BOARD_SIZE = 15
WIN_LENGTH = 5
CELL_SIZE = 30


class GomokuBoard:
    def __init__(self, size):
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.size = size

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

    def evaluate(self, player):
        score = 0
        opponent = PLAYER_PINK if player == PLAYER_BLUE else PLAYER_BLUE
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


def minimax(board, depth, maximizing_player, player):
    opponent = PLAYER_PINK if player == PLAYER_BLUE else PLAYER_BLUE

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


def alpha_beta(board, depth, maximizing_player, player, alpha, beta):
    opponent = PLAYER_PINK if player == PLAYER_BLUE else PLAYER_BLUE

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
                break
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
                break
        return min_eval, best_move


class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku Game")
        self.board = GomokuBoard(BOARD_SIZE)
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_BLUE
        self.human_player = PLAYER_BLUE
        self.ai_player = PLAYER_PINK
        self.game_mode = "human_vs_ai"

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        mode_label = tk.Label(top_frame, text="Select Mode:")
        mode_label.pack(side=tk.LEFT, padx=5)

        self.mode_var = tk.StringVar(value="human_vs_ai")
        mode_menu = tk.OptionMenu(top_frame, self.mode_var, "human_vs_ai", "ai_vs_ai")
        mode_menu.pack(side=tk.LEFT)

        color_label = tk.Label(top_frame, text="Play as:")
        color_label.pack(side=tk.LEFT, padx=5)

        self.color_var = tk.StringVar(value="BLUE")
        color_menu = tk.OptionMenu(top_frame, self.color_var, "BLUE", "PINK")
        color_menu.pack(side=tk.LEFT)

        start_button = tk.Button(top_frame, text="Start Game", command=self.start_game)
        start_button.pack(side=tk.LEFT, padx=10)

        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                canvas = tk.Canvas(board_frame, width=CELL_SIZE, height=CELL_SIZE, bg="#E6E6FA")
                canvas.grid(row=x, column=y, padx=1, pady=1)
                self.buttons[x][y] = canvas
                canvas.bind("<Button-1>", lambda event, x=x, y=y: self.on_cell_click(x, y))

    def start_game(self):
        self.board = GomokuBoard(BOARD_SIZE)
        self.current_player = PLAYER_BLUE
        self.game_mode = self.mode_var.get()
        self.human_player = self.color_var.get()
        self.ai_player = PLAYER_PINK if self.human_player == PLAYER_BLUE else PLAYER_BLUE

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.buttons[x][y].delete("all")
                self.buttons[x][y].config(bg="#E6E6FA")

        if self.game_mode == "ai_vs_ai":
            threading.Thread(target=self.play_ai_vs_ai).start()
        elif self.current_player == self.ai_player:
            self.root.after(100, self.ai_turn)

    def on_cell_click(self, x, y):
        if self.game_mode != "human_vs_ai":
            return
        if self.board.board[x][y] != EMPTY or self.current_player != self.human_player:
            return
        self.make_move(x, y)
        self.root.after(100, self.ai_turn)

    def make_move(self, x, y):
        self.board.board[x][y] = self.current_player
        self.draw_circle(x, y)

        if self.board.is_winner(self.current_player):
            messagebox.showinfo("Game Over", f"{self.current_player} wins!")
            return

        self.current_player = PLAYER_PINK if self.current_player == PLAYER_BLUE else PLAYER_BLUE

    def draw_circle(self, x, y):
        canvas = self.buttons[x][y]
        color = "blue" if self.current_player == PLAYER_BLUE else "pink"
        canvas.create_oval(5, 5, CELL_SIZE - 5, CELL_SIZE - 5, fill=color)

    def ai_turn(self):
        if self.current_player != self.ai_player:
            return
        _, move = minimax(self.board, depth=2, maximizing_player=True, player=self.ai_player)
        if move:
            x, y = move
            self.make_move(x, y)

    def play_ai_vs_ai(self):
        while True:
            if self.board.is_winner(self.current_player):
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                break

            if self.current_player == PLAYER_BLUE:
                _, move = minimax(self.board, depth=2, maximizing_player=True, player=self.current_player)
            else:
                _, move = alpha_beta(self.board, depth=2, maximizing_player=True,
                                    player=self.current_player, alpha=-math.inf, beta=math.inf)

            if move is None:
                break

            x, y = move
            self.root.after(0, lambda x=x, y=y: self.make_move(x, y))
            time.sleep(0.3)


if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()
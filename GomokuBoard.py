class GomokuBoard:
    def __init__(self, size=15):
        self.size = size
        self.board = [["." for _ in range(size)] for _ in range(size)]

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
    
    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == "."

    def make_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.board[row][col] = symbol
            return True
        return False


#this for testing
board = GomokuBoard()

board.print_board()# initail empty board


board.make_move(0, 0, "X")
board.make_move(1, 1, "O")
board.make_move(14, 14, "X")


x = board.make_move(0, 0, "O")
print("Move success:", x) #should return flase as 0,0 already has x
y=board.make_move(0,1,'x')
print(y)

print("\nUpdated board:")
board.print_board()

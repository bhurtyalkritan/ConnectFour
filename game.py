import tkinter as tk
from tkinter import messagebox

def create_board():
    return [[" " for _ in range(7)] for _ in range(6)]

def drop_disc(board, column, disc):
    for row in reversed(range(6)):
        if board[row][column] == " ":
            board[row][column] = disc
            return row
    return None

def check_win(board, disc):
    # Horizontal, vertical, and diagonal checks
    for c in range(4):
        for r in range(6):
            if board[r][c] == disc and board[r][c+1] == disc and board[r][c+2] == disc and board[r][c+3] == disc:
                return True
    for c in range(7):
        for r in range(3):
            if board[r][c] == disc and board[r+1][c] == disc and board[r+2][c] == disc and board[r+3][c] == disc:
                return True
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == disc and board[r-1][c+1] == disc and board[r-2][c+2] == disc and board[r-3][c+3] == disc:
                return True
    for c in range(4):
        for r in range(3):
            if board[r][c] == disc and board[r+1][c+1] == disc and board[r+2][c+2] == disc and board[r+3][c+3] == disc:
                return True
    return False

def is_full(board):
    return all(board[0][col] != " " for col in range(7))

# Ensure to include the previously defined functions: create_board, drop_disc, check_win, is_full

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.board = create_board()
        self.current_player = "R"  # "R" for Red, "Y" for Yellow
        self.slots = [[None for _ in range(7)] for _ in range(6)]  # Track canvas items for each slot
        self.init_board()
        self.create_buttons()

    def init_board(self):
        self.canvas = tk.Canvas(self.master, width=700, height=600, bg='blue')
        self.canvas.grid(row=1, columnspan=7)
        self.draw_empty_slots()

    def create_buttons(self):
        for col in range(7):
            button = tk.Button(self.master, text=str(col), command=lambda col=col: self.prepare_disc_drop(col))
            button.grid(row=0, column=col)

    def draw_empty_slots(self):
        for row in range(6):
            for col in range(7):
                x0 = col * 100 + 10
                y0 = row * 100 + 10
                x1 = x0 + 80
                y1 = y0 + 80
                self.slots[row][col] = self.canvas.create_oval(x0, y0, x1, y1, fill="white", outline="black")

    def prepare_disc_drop(self, column):
        row = drop_disc(self.board, column, self.current_player)  # Get the target row for the disc
        if row is not None:
            self.animate_disc(column, row)
        else:
            messagebox.showwarning("Column full", "This column is full. Please try a different one.")

    def animate_disc(self, column, target_row):
        color = "red" if self.current_player == "R" else "yellow"
        # Start the animation from the top
        self.animate_step(column, 0, target_row, color)

    def animate_step(self, column, current_row, target_row, color):
        if current_row > 0:
            # Clear the disc at the previous temporary position
            self.canvas.itemconfig(self.slots[current_row-1][column], fill="white")
        # Update the disc to the next position
        self.canvas.itemconfig(self.slots[current_row][column], fill=color)

        if current_row < target_row:
            # Continue the animation if the target row has not been reached
            self.master.after(100, lambda: self.animate_step(column, current_row + 1, target_row, color))
        else:
            # Finalize the disc placement and check game state
            self.finalize_move()

    def finalize_move(self):
        if check_win(self.board, self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_board()
        elif is_full(self.board):
            messagebox.showinfo("Game Over", "The game is a tie!")
            self.reset_board()
        else:
            self.current_player = "R" if self.current_player == "Y" else "Y"

    def reset_board(self):
        self.canvas.delete("all")  # Clear the canvas
        self.board = create_board()
        self.current_player = "R"
        self.draw_empty_slots()  # Re-draw the empty slots for the new game

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    app = ConnectFourGUI(root)
    root.mainloop()

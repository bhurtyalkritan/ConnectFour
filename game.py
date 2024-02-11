import tkinter as tk
from tkinter import messagebox
from random import choice  # Import choice for the AI move

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

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="lightgray")
        self.game_frame = tk.Frame(self.master)
        self.menu_frame = tk.Frame(self.master)
        self.action_in_progress = False
        self.board = create_board()
        self.current_player = "R"  # "R" for Red, "Y" for Yellow
        self.slots = [[None for _ in range(7)] for _ in range(6)]
        self.is_ai_game = False  # Track if the game is against AI
        self.create_menu()

    def create_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(padx=10, pady=10)
        tk.Label(self.menu_frame, text="Connect Four", font=("Arial", 24, "bold")).pack(pady=(0, 20))
        tk.Button(self.menu_frame, text="Player vs Player", command=self.start_pvp).pack(fill="x")
        tk.Button(self.menu_frame, text="Player vs AI", command=self.start_ai).pack(fill="x", pady=5)
        tk.Button(self.menu_frame, text="Exit", command=self.exit_game).pack(fill="x")

    def start_game(self, ai_game=False):
        self.is_ai_game = ai_game
        self.clear_frame(self.game_frame)  # Clear the game frame before creating a new game
        self.game_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.init_board()  # Initialize the board and its GUI representation first
        self.reset_board()  # Now safe to reset the board, since self.canvas is defined
        self.create_buttons()
        tk.Button(self.game_frame, text="Exit Game", command=self.exit_to_menu).grid(row=7, columnspan=7)
        if ai_game and self.current_player == "Y":
            self.master.after(500, self.ai_move)

    def start_pvp(self):
        self.start_game(ai_game=False)

    def start_ai(self):
        self.start_game(ai_game=True)

    def exit_to_menu(self):
        self.clear_frame(self.game_frame)
        self.create_menu()

    def exit_game(self):
        self.master.quit()
    
    def ai_move(self):
        # AI logic for choosing a column
        def can_win_next(board, disc):
            for c in range(7):
                temp_board = [row[:] for row in board]  # Copy the board
                for r in reversed(range(6)):
                    if temp_board[r][c] == " ":
                        temp_board[r][c] = disc
                        if check_win(temp_board, disc):
                            return c
                        break
            return None

        opponent_disc = "R" if self.current_player == "Y" else "Y"
        
        # 1. Check if AI can win in the next move
        win_move = can_win_next(self.board, self.current_player)
        if win_move is not None:
            self.prepare_disc_drop(win_move)
            return

        # 2. Block the opponent if they are about to win in the next move
        block_move = can_win_next(self.board, opponent_disc)
        if block_move is not None:
            self.prepare_disc_drop(block_move)
            return

        center_columns = [3, 2, 4, 1, 5, 0, 6]
        for col in center_columns:
            if self.board[0][col] == " ":
                self.prepare_disc_drop(col)
                return

    def init_board(self):
        self.canvas = tk.Canvas(self.game_frame, width=700, height=600, bg='blue')
        self.canvas.grid(row=1, columnspan=7)
        self.draw_empty_slots()

    def create_buttons(self):
        self.column_buttons = []  
        for col in range(7):
            button = tk.Button(self.game_frame, text=str(col), command=lambda col=col: self.prepare_disc_drop(col))
            button.grid(row=0, column=col)
            self.column_buttons.append(button)

    def enable_buttons(self, enable=True):
        for button in self.column_buttons:
            button['state'] = tk.NORMAL if enable else tk.DISABLED

    def draw_empty_slots(self):
        for row in range(6):
            for col in range(7):
                x0 = col * 100 + 10
                y0 = row * 100 + 10
                x1 = x0 + 80
                y1 = y0 + 80
                self.slots[row][col] = self.canvas.create_oval(x0, y0, x1, y1, fill="white", outline="black")

    def prepare_disc_drop(self, column):
        if self.action_in_progress:  
            return  
        self.action_in_progress = True
        self.enable_buttons(False)  
        row = drop_disc(self.board, column, self.current_player)
        if row is not None:
            self.animate_disc(column, row)
        else:
            messagebox.showwarning("Column full", "This column is full. Please try a different one.")

    def animate_disc(self, column, target_row):
        color = "red" if self.current_player == "R" else "yellow"
        self.animate_step(column, 0, target_row, color)

    def animate_step(self, column, current_row, target_row, color):
        if current_row > 0:
            self.canvas.itemconfig(self.slots[current_row-1][column], fill="white")
        self.canvas.itemconfig(self.slots[current_row][column], fill=color)

        if current_row < target_row:
            self.master.after(100, lambda: self.animate_step(column, current_row + 1, target_row, color))
        else:
            self.finalize_move()

    def finalize_move(self):
        self.action_in_progress = False  
        self.enable_buttons(True)  
        if check_win(self.board, self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_board()
        elif is_full(self.board):
            messagebox.showinfo("Game Over", "The game is a tie!")
            self.reset_board()
        else:
            self.current_player = "R" if self.current_player == "Y" else "Y"
            if self.is_ai_game and self.current_player == "Y":  
                self.ai_move()


    def clear_frame(self, frame):
        
        for widget in frame.winfo_children():
            widget.destroy()

    def create_menu(self):
        self.clear_frame(self.menu_frame)  
        self.menu_frame.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Label(self.menu_frame, text="Connect Four", font=("Arial", 24, "bold"), bg="lightgray").pack(pady=(0, 20))
        tk.Button(self.menu_frame, text="Player vs Player", command=self.start_pvp).pack(fill="x")
        tk.Button(self.menu_frame, text="Player vs AI", command=self.start_ai).pack(fill="x", pady=5)
        tk.Button(self.menu_frame, text="Exit", command=self.exit_game).pack(fill="x")


    def reset_board(self):
        if hasattr(self, 'canvas'):
            self.canvas.delete("all")  
        self.board = create_board()
        self.current_player = "R"
        if hasattr(self, 'canvas'):  
            self.draw_empty_slots()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    app = ConnectFourGUI(root)
    root.mainloop()

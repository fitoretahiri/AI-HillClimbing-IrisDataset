import tkinter as tk
from tkinter import messagebox
import numpy as np
import time

class NQueenSolverGUI:
    def __init__(self, root):
        """Initialize the N-Queen Solver GUI."""
        self.root = root
        self.root.title("N-Queen Solver")
        self.create_widgets()
        self.board_size = None
        self.canvas = None

    def create_widgets(self):
        """Create input field and solve button in the GUI."""
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Number of Queens (N):").grid(row=0, column=0, padx=5, pady=5)
        self.n_input = tk.Entry(input_frame, width=5)
        self.n_input.grid(row=0, column=1, padx=5, pady=5)

        self.solve_button = tk.Button(input_frame, text="Solve", command=self.solve_nqueens)
        self.solve_button.grid(row=0, column=2, padx=10, pady=5)

    def initialize_canvas(self, N):
        """Initialize and display the chessboard canvas."""
        if self.canvas:
            self.canvas.destroy()
        self.board_size = N
        self.cell_size = 40
        self.canvas = tk.Canvas(self.root, width=N * self.cell_size, height=N * self.cell_size, bg="white")
        self.canvas.pack(pady=10)
        self.draw_board()

    def draw_board(self):
        """Draw the N x N chessboard."""
        N = self.board_size
        for i in range(N):
            for j in range(N):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def draw_queens(self, board):
        """Draw queens on the board based on the given board configuration."""
        self.canvas.delete("queen")
        N = len(board)
        for row, col in enumerate(board):
            x1, y1 = col * self.cell_size, row * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red", outline="black", tags="queen")
        self.root.update()

    def solve_hill_climbing(self, board):
        """Solve the N-Queens problem using the hill climbing algorithm."""
        N = len(board)
        current = board.copy()
        current_score = self.evaluate_conflicts(current)

        while current_score > 0:
            best_board = None
            min_score = current_score

            for row in range(N):
                for col in range(N):
                    if col != current[row]:
                        new_board = current.copy()
                        new_board[row] = col
                        new_score = self.evaluate_conflicts(new_board)
                        if new_score < min_score:
                            min_score = new_score
                            best_board = new_board

            if min_score < current_score:
                current = best_board
                current_score = min_score
                self.draw_queens(current)
                time.sleep(0.5)  # Slow down for visualization
            else:
                break

        return current

    @staticmethod
    def evaluate_conflicts(board):
        """Count the number of queen conflicts in the given board configuration."""
        conflicts = 0
        N = len(board)
        for i in range(N):
            for j in range(i + 1, N):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def solve_nqueens(self):
        """Handle user input, generate initial board, and solve the N-Queens problem."""
        try:
            N = int(self.n_input.get())
            if N < 4:
                raise ValueError("N must be 4 or greater.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.initialize_canvas(N)
        solution_found = False
        attempts = 0
        total_start_time = time.time()

        while not solution_found:
            attempts += 1
            initial_board = np.random.randint(0, N, size=N)  # Randomly initialize board
            self.draw_queens(initial_board)
            final_board = self.solve_hill_climbing(initial_board)

            final_score = self.evaluate_conflicts(final_board)
            if final_score == 0:
                solution_found = True
                total_end_time = time.time()
                total_time_taken = total_end_time - total_start_time
                messagebox.showinfo(
                    "Solved!",
                    f"Solved in {total_time_taken:.2f} seconds after {attempts} attempts!"
                )
                self.draw_queens(final_board)
            else:
                print(f"Attempt {attempts} failed. Retrying...")

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueenSolverGUI(root)
    root.mainloop()

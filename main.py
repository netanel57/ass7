import tkinter as tk
from tkinter import messagebox
import random


class Game:
    def __init__(self, size: int) -> None:
        self.n = size
        self.board = self.create_board()
        self.revealed = self.create_2d_array(False)
        self.flagged = self.create_2d_array(False)
        self.buttons = self.create_2d_array(None)
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.place_mines()
        self.create_gui()

    def create_board(self):
        return [[0 for _ in range(self.n)] for _ in range(self.n)]

    def create_2d_array(self, default):
        return [[default for _ in range(self.n)] for _ in range(self.n)]

    def place_mines(self):
        total_cell = self.n * self.n
        num_mines = int(input("Enter the number of bombs:"))
        if num_mines > total_cell:
            print("You can't mine, try again")
            return self.place_mines()

        bomb_positions = set()
        while len(bomb_positions) < num_mines:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            if (row, col) not in bomb_positions:
                bomb_positions.add((row, col))
                self.board[row][col] = -1

    def count_adjacent_bombs(self, row, col):
        count = 0
        for i in range(max(0, row - 1), min(self.n, row + 2)):
            for j in range(max(0, col - 1), min(self.n, col + 2)):
                if i == row and j == col:
                    continue
                if self.board[i][j] == -1:
                    count += 1
        return count

    def create_gui(self):
        for row in range(self.n):
            for col in range(self.n):
                btn = tk.Button(self.window, width=2, height=1)
                btn.bind("<Button-1>", lambda e, r=row, c=col: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=row, c=col: self.right_click(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def left_click(self, row, col):
        if row < 0 or row >= self.n or col < 0 or col >= self.n:
            return
        if self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        if self.board[row][col] == -1:
            messagebox.showinfo("Game Over", "You clicked on a mine!")
        else:
            adjacent = self.count_adjacent_bombs(row, col)
            self.board[row][col] = adjacent
            if adjacent == 0:
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        if i == row and j == col:
                            continue
                        self.left_click(i, j)
        self.update_gui()
        if self.check_win():
            messagebox.showinfo("You Win!", "You cleared the board!")

    def right_click(self, row, col):
        if row < 0 or row >= self.n or col < 0 or col >= self.n:
            return
        if self.revealed[row][col]:
            return
        self.flagged[row][col] = not self.flagged[row][col]
        self.update_gui()

    def update_gui(self):
        for i in range(self.n):
            for j in range(self.n):
                btn = self.buttons[i][j]
                if self.revealed[i][j]:
                    val = self.board[i][j]
                    btn.config(state=tk.DISABLED, relief=tk.SUNKEN)
                    if val > 0:
                        btn.config(text=str(val))
                    elif val == 0:
                        btn.config(text="")
                    elif val == -1:
                        btn.config(text="B", bg="red")
                elif self.flagged[i][j]:
                    btn.config(text="flag")
                else:
                    btn.config(text="")

    def check_win(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return False
        return True

    def run(self):
        self.window.mainloop()


def main():
    size = int(input("Enter the size of the board: "))
    game = Game(size)
    game.run()


if __name__ == "__main__":
    main()

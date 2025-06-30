import tkinter as tk
from tkinter import messagebox
import random
import sys

# create the gui
window = tk.Tk()
window.title("Minesweeper")
window.geometry("300x300")



def create_board(n):
    board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
        board.append(row)
    return board


def place_mines(board):
    n = len(board)
    total_cell = n * n
    num_mines = int(input("Enter the number of bombs:"))
    if num_mines > total_cell:
        print("You can't mine, try again")
        return place_mines(board)

    bomb_positions = set()
    while len(bomb_positions) < num_mines:
        row = random.randint(0, n - 1)
        col = random.randint(0, n - 1)
        if (row, col) not in bomb_positions:
            bomb_positions.add((row, col))
            board[row][col] = -1  # we place a bomb here
#for debug. show the answers to the console here if needed
    for row in board:
        pass
    return board


# helper function to count adjacent mines
def count_adjacent_bombs(board, row, col):
    n = len(board)
    count = 0
    for i in range(max(0, row - 1), min(n, row + 2)):
        for j in range(max(0, col - 1), min(n, col + 2)):
            if i == row and j == col:
                continue
            if board[i][j] == -1:
                count += 1
    return count


def left_click(board, revealed, row, col):
    """
    So I built this function to handle the cased of left click
    -if it's a bomb, game over
    -if it's a number, reveal it
    -if it's 0, reveal adjacent cells
    :param board:
    :param revealed:
    :param row:
    :param col:
    :return:
    """
    n = len(board)
    if row < 0 or row >= n or col < 0 or col >= n or revealed[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == -1:
        print("Game over")
        return
    adjacent = count_adjacent_bombs(board, row, col)
    board[row][col] = adjacent
    if adjacent == 0:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                left_click(board, revealed, i, j)


def right_click(flagged, revealed, row, col):
    """
    So I built this function to handle the case of right click
    -if the cell already revealed do nothing
    -if it's flagged, ok
    -if it's not flagged, flag it.
    :param flagged:
    :param revealed:
    :param row:
    :param col:
    :return:
    """
    n = len(flagged)
    if row < 0 or row >= n or col < 0 or col >= n:
        return
    if revealed[row][col]:
        return
    flagged[row][col] = not flagged[row][col]


def check_win(board, revealed):
    n = len(board)
    for row in range(n):
        for col in range(n):
            if board[row][col] != -1 and not revealed[row][col]:
                return False
    return True
def create_2d_array(n, default_value):
    return [[default_value for _ in range(n)] for _ in range(n)]

def on_left_click(event):
    button = event.widget
    row = button.row
    col = button.col
    left_click(board, revealed, row, col)
    update_gui()
    if board[row][col] == -1:
        messagebox.showinfo("Game Over", "You clicked on a mine!")
    elif check_win(board, revealed):
        messagebox.showinfo("You Win!", "You cleared the board!")
def on_right_click(event):
    button = event.widget
    row = button.row
    col = button.col
    right_click(flagged, revealed, row, col)


def start_game():
    global board, revealed, flagged, buttons, n

    n = int(input("Enter the size of the board: "))
    board = create_board(n)
    revealed = create_2d_array(n, False)
    flagged = create_2d_array(n, False)
    buttons = create_2d_array(n, None)

    place_mines(board)

    for row in range(n):
        for col in range(n):
            btn = tk.Button(window, width=2, height=1)
            btn.row = row
            btn.col = col
            btn.bind("<Button-1>", on_left_click)
            btn.bind("<Button-3>", on_right_click)
            btn.grid(row=row, column=col)
            buttons[row][col] = btn
def update_gui():
    for i in range(n):
        for j in range(n):
            btn = buttons[i][j]
            if revealed[i][j]:
                val = board[i][j]
                btn.config(state=tk.DISABLED, relief=tk.SUNKEN)
                if val > 0:
                    btn.config(text=str(val))
                elif val == 0:
                    btn.config(text="")
                elif val == -1:
                    btn.config(text="B", bg="red")
            elif flagged[i][j]:
                btn.config(text="flag")
            else:
                btn.config(text="")

start_game()
window.mainloop()
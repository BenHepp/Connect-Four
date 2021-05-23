# Author: Ben Hepp
# Created: May 17th, 2021
# Email: benhepp1414@gmail.com

import sys
from tkinter import *
from nodes import *
from AI import *
import numpy as np
import random
import time
import csv

width_of_board = 1200
height_of_board = 800
example_token_width = 80
motion_token_width = 100
max_moves = 42.0

def col_i(i):
    x_left = (1/3) * width_of_board + (i/8) * (2/3) * width_of_board
    x_right = (1/3) * width_of_board + ((i+1)/8) * (2/3) * width_of_board
    y_bottom = (7/8) * height_of_board
    y_top = (1/8) * height_of_board - 20
    return x_left, x_right, y_bottom, y_top

def row_i(i):
    x_left = (1/3) * width_of_board
    x_right = width_of_board - (1/8) * (2/3) * width_of_board
    y_bottom = ((i+1)/8) * height_of_board
    y_top = ((i+1)/8) * height_of_board
    return x_left, x_right, y_bottom, y_top

def token_coordinates(col, row):
    x_left = (1/3) * width_of_board + (col/8) * (2/3) * width_of_board
    x_right = (1/3) * width_of_board + ((col+1)/8) * (2/3) * width_of_board
    y_bottom = ((num_rows-row)/8) * height_of_board
    y_top = ((num_rows-row+1)/8) * height_of_board
    return x_left, x_right, y_bottom, y_top

class Connect_Four():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def mainloop(self):
        self.window.mainloop()

    def __init__(self):
        self.window = Tk()
        self.window.title('Connect-4')
        self.canvas = Canvas(self.window, width=width_of_board, height=height_of_board)
        self.canvas.pack()
        self.train_or_play()

    def initialize_new_session(self):
        self.initialize_member_variables()
        self.generate_gameboard()

    def initialize_member_variables(self):
        self.game_in_progress = False
        self.players_turn = False
        self.move_tracker = None
        self.board_chips = np.zeros(num_cols, dtype=int)
        self.gameboard = {}

    def generate_gameboard(self):
        for i in range(num_cols):
            for j in range(num_rows):
                self.gameboard[(i,j)] = Node(i, j)
        for i in range(num_cols):
            for j in range(num_rows):
                self.gameboard[(i,j)].connect_to_neighbors(self.gameboard)

    def train_or_play(self):
        self.initialize_new_session()
        if len(sys.argv) == 2 and sys.argv[1] == "train":
            self.train_AI()
        else:
            self.play_game()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # ------------------------------------------------------------------
    def draw_game_preview(self):
        self.canvas.create_text(width_of_board*0.25, height_of_board/2, font="cmr 60 bold", fill="blue", text="Player\nBegins", justify='center')
        self.canvas.create_text(width_of_board*0.25, height_of_board/1.2, font="cmr 20 bold", fill="grey", text="Click Here", justify='center')
        self.canvas.create_text(width_of_board*0.75, height_of_board/2, font="cmr 60 bold", fill="red", text="Computer\nBegins", justify='center')
        self.canvas.create_text(width_of_board*0.75, height_of_board/1.2, font="cmr 20 bold", fill="grey", text="Click Here", justify='center')
        self.canvas.create_line(width_of_board*0.5, 0, width_of_board*0.5, height_of_board)

    def draw_board(self):
        for i in range(num_cols+1): # vertical lines
            x1, _, y1, y2 = col_i(i)
            self.canvas.create_line(x1,y1,x1,y2, width=4)

        for i in range(num_rows+1): # horizontal lines
            x1, x2, y1, y2 = row_i(i)
            self.canvas.create_line(x1, y1, x2, y2, width=4)

    def draw_game_begin_text(self):
        self.canvas.create_text(width_of_board*(1/6), height_of_board*0.5, font="cmr 40 bold", fill="light green", \
                                text="Click Anywhere\nto Begin Game", justify='center', tag="begin_text")

    def draw_color_assignments(self):
        self.canvas.create_text(width_of_board*(3/24), height_of_board*(1/3), font="cmr 45 bold", fill="grey", \
                                text="Player:", justify='center', tag="player_color")
        self.canvas.create_text(width_of_board*(3/24), height_of_board*(2/3), font="cmr 45 bold", fill="grey", \
                                text="Computer:", justify='center', tag="computer_color")
        self.canvas.create_oval(width_of_board*(1/12), height_of_board*(5/12), width_of_board*(1/12)+example_token_width, height_of_board*(5/12)+example_token_width, \
                                fill="blue", outline="#DDD", width=4, tag="player_example_token")
        self.canvas.create_oval(width_of_board*(1/12), height_of_board*(9/12), width_of_board*(1/12)+example_token_width, height_of_board*(9/12)+example_token_width, \
                                fill="red", outline="#DDD", width=4, tag="computer_example_token")

    def draw_drop_token(self):
        self.canvas.create_oval(0, 0, 0, 0, fill="blue", outline="#DDD", width=4, \
                                state="hidden", tag="drop_token")
        self.window.bind('<Motion>', self.motion)

    def draw_move(self, color, col, row, token_state):
        self.canvas.itemconfig("drop_token", state=token_state)
        x1, x2, y1, y2 = token_coordinates(col, row)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#DDD", width=4)

    def draw_ending_text(self, outcome):
        text, text_color, text_hight = None, None, None

        if outcome is "player":
            text, text_color, text_hight = "Player Wins :)", "light green", 1/3
        elif outcome is "computer":
            text, text_color, text_hight = "Computer Wins :(", "dark green", 2/3
        else:
            text, text_color, text_hight = "Tie game :P", "light blue", 1/2

        self.canvas.create_text(width_of_board*(4/24), height_of_board*text_hight, font="cmr 45 bold", fill=text_color, \
                                text=text, justify='center')

        self.canvas.create_text(width_of_board*(15/24), height_of_board*(16/17), font="cmr 45 bold", fill="magenta", \
                                text="Click Anywhere to Play Again", justify='center')

    # ------------------------------------------------------------------
    # Game Setup Functions:
    # ------------------------------------------------------------------

    def play_game(self):
        self.window.bind('<Button-1>', self.click)
        self.draw_game_preview()

    def click(self, event):
        self.window.unbind('<Button-1>')
        self.canvas.delete("all")
        self.initialize_first_move_vars(event)
        self.draw_board()
        self.window.bind('<Button-1>', self.game_click)

    def initialize_first_move_vars(self, event):
        clicked_x_coordinate = event.x
        if clicked_x_coordinate < width_of_board / 2:
            print("Player begins")
            self.players_turn = True
            self.move_tracker = "p"
            self.artificial_intelligence = AI("second")
        else:
            print("Computer begins")
            self.players_turn = False
            self.move_tracker = "c"
            self.artificial_intelligence = AI("first")
        self.draw_game_begin_text()


    # ------------------------------------------------------------------
    # Logic Functions:
    # ------------------------------------------------------------------

    def game_click(self, event):
        if self.game_in_progress is False:
            self.canvas.delete("begin_text")
            self.draw_color_assignments()
            self.game_in_progress = True
            self.draw_drop_token()
            self.computer_first_move()
        elif self.column_selected(event) != -1:
            self.driver(event)

    def computer_first_move(self):
        if self.players_turn is False:
            self.driver(None)

    def driver(self, event):
        if self.players_turn is True and self.selected_valid_col(event) is True:

            col, row = self.take_player_turn(event, "blue")
            self.players_turn = False
            self.draw_move("blue", col, row, "hidden")

            player_wins = self.check_for_winner("blue", col, row)
            if player_wins is True:
                print("    Player Wins")
                self.gameover("player")
                return

        if self.check_for_tie() is True:
            print("    Tie Game")
            self.gameover("tie")

        if self.players_turn is False:
            col, row = self.take_computer_turn("red")
            self.players_turn = True
            self.draw_move("red", col, row, "normal")

            computer_wins = self.check_for_winner("red", col, row)
            if computer_wins is True:
                print("    Computer Wins")
                self.gameover("computer")
                return

        if self.check_for_tie() is True:
            print("    Tie Game")
            self.gameover("tie") #consider testing for tie withing "check_for_winner"

    def take_player_turn(self, event, color):
        col = self.column_selected(event)
        row = self.board_chips[col]

        self.log_move(color[0], col, row)
        return col, row

    def take_computer_turn(self, color):
        col = self.artificial_intelligence.next_move(self.board_chips, self.move_tracker, self.gameboard, color)
        row = self.board_chips[col]

        self.log_move(color[0], col, row)
        return col, row

    def take_computer_turn_TRAINING(self, color, ai):
        col = 0
        if ai == 1:
            col = self.artificial_intelligence1.next_move(self.board_chips, self.move_tracker, self.gameboard, color)
        else:
            col = self.artificial_intelligence2.next_move(self.board_chips, self.move_tracker, self.gameboard, color)
        row = self.board_chips[col]

        self.log_move(color[0], col, row)
        return col, row

    def log_move(self, token, col, row):
        self.gameboard[(col, row)].token = token
        self.move_tracker += str(col)
        self.board_chips[col] += 1

    def check_for_winner(self, color, col, row):
        return self.gameboard[(col, row)].is_winning_token()

    def check_for_tie(self):
        if np.sum(self.board_chips) >= 42:
            return True
        return False

    def column_selected(self, event):
        if self.players_turn is True:
            for i in range(num_cols):
                x_left, x_right, y_bottom, _ = col_i(i)
                if x_left <= event.x and event.x <= x_right and event.y <= y_bottom:
                    return i
        return -1

    def selected_valid_col(self, event):
        col = self.column_selected(event)
        if self.board_chips[col] < num_rows:
            return True
        return False

    def motion(self, event):
        if self.players_turn is True:
            for i in range(num_cols):
                x_left, x_right, y_bottom, _ = col_i(i)
                if x_left <= event.x and event.x <= x_right and event.y <= y_bottom:
                    self.canvas.coords("drop_token", x_left, 0, x_right, 100)
                    self.canvas.itemconfig("drop_token", state="normal")
                    return
            self.canvas.itemconfig("drop_token", state="hidden")

    # ------------------------------------------------------------------
    # End Game Functions
    # ------------------------------------------------------------------
    def gameover(self, winner):
        self.window.unbind('<Button-1>')
        self.window.unbind('<Motion>')
        self.remove_drawings()
        self.draw_ending_text(winner)
        outcome = "won" if winner is "computer" else "lost"
        self.artificial_intelligence.end_game(outcome)
        self.artificial_intelligence.write_back_prev_moves()
        self.window.bind('<Button-1>', self.restart)

    def restart(self, event):
        self.canvas.delete("all")
        self.train_or_play()

    def remove_drawings(self):
        self.canvas.delete("player_example_token")
        self.canvas.delete("computer_example_token")
        self.canvas.delete("player_color")
        self.canvas.delete("computer_color")
        self.canvas.delete("drop_token")


    # ------------------------------------------------------------------
    # AI Training Functions
    # ------------------------------------------------------------------
    def train_AI(self):
        print("training...")

        cpu_1 = "player"
        cpu_2 = "computer"

        # read in batch size??
        batch_size = 100000
        self.initialize_training_first_move(cpu_1)
        for game in range(batch_size):

            self.initialize_new_session()
            self.move_tracker = cpu_1[0]
            self.AI_driver(cpu_1, cpu_2)

            if game % (batch_size/100) == 0:
                print(str(game * 100 / batch_size) + "%")

        self.artificial_intelligence1.write_back_prev_moves()
        self.artificial_intelligence2.write_back_prev_moves()

        print("Training completed.")

    def initialize_training_first_move(self, name):
        self.move_tracker = name[0]
        self.artificial_intelligence1 = AI("first")
        self.artificial_intelligence2 = AI("second")

    def AI_driver(self, cpu_1, cpu_2):
        winner = None

        while True:
            col, row = self.take_computer_turn_TRAINING("red", 1)
            cpu_1_wins = self.check_for_winner("red", col, row)
            if cpu_1_wins is True:
                winner = cpu_1
                break

            if self.check_for_tie() is True:
                winner = "tie"
                break

            col, row = self.take_computer_turn_TRAINING("blue", 2)
            cpu_2_wins = self.check_for_winner("blue", col, row)
            if cpu_2_wins is True:
                winner = cpu_2
                break

            if self.check_for_tie() is True:
                winner = "tie"
                break

        outcome_cpu_1 = "won" if winner is "player" else "lost"
        outcome_cpu_2 = "won" if winner is "computer" else "lost"
        self.artificial_intelligence1.end_game(outcome_cpu_1)
        self.artificial_intelligence2.end_game(outcome_cpu_2)
        # print statistics



game_instance = Connect_Four()
game_instance.mainloop()










    # game loop, driver, when comp wins print "lol dad sucks"

# AI Class

from nodes import *
import numpy as np
import random
import math
import csv

headers = None

class AI:
    
    def __init__(self, debut):
        self.prev_moves = {}
        self.game_moves = []
        self.debut = debut
        self.read_in_prev_moves()
    
    def next_move(self, board_chips, moves_so_far, gameboard, color):
        
        col = None
        col_scores = np.zeros(7, dtype=float)
        
        for column in range(7):
            col_scores[column] = self.evaluate_column(board_chips, moves_so_far, column, gameboard, color)
        
        col = self.break_ties_randomly(col_scores)
        self.game_moves.append(moves_so_far + str(col))
        
    return col

def break_ties_randomly(self, col_scores):
    col = np.argmax(col_scores)
    max_val = col_scores[col]
    
    index_arr = []
        index = 0
        for val in col_scores:
            if max_val == val:
                index_arr.append(index)
            index += 1

    random_index = random.randint(0,len(index_arr)-1)
        col = index_arr[random_index]
        print('----')
        
        return col

def read_in_prev_moves(self):
    filename = "prev_moves1.csv" if self.debut == "first" else "prev_moves2.csv"
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                move = row[0]
                score = row[1]
                wins = row[2]
                total = row[3]
                self.prev_moves[move] = {}
                self.prev_moves[move]["score"] = float(score)
                self.prev_moves[move]["wins"] = int(wins)
                self.prev_moves[move]["total"] = int(total)
                    
                    def write_back_prev_moves(self):
                        filename = "prev_moves1.csv" if self.debut == "first" else "prev_moves2.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for move in self.prev_moves:
        score = self.prev_moves[move]["score"]
        wins = self.prev_moves[move]["wins"]
        total = self.prev_moves[move]["total"]
        row = [move,score,wins,total]
        csvwriter.writerow(row)

    def end_game(self, outcome):
        self.update_prev_move_scores(outcome)
    #self.write_back_prev_moves()

def update_prev_move_scores(self, outcome):
    
    update = 1 if outcome == "won" else 0
        
        for move in self.game_moves:
            if move in self.prev_moves:
                self.prev_moves[move]["wins"] += update
                self.prev_moves[move]["total"] += 1
                self.prev_moves[move]["score"] = float(self.prev_moves[move]["wins"]) / self.prev_moves[move]["total"]
            else:
                self.prev_moves[move] = {"score": 1, "wins": 1, "total": 1}
    self.game_moves = []

def evaluate_column(self, board_chips, moves_so_far, column, gameboard, color):
    
    col_score = 1
        col = column
        row = board_chips[col]
        
        print("col " + str(col), end=": ")
        
        if board_chips[column] >= 6:
            print("-1")
            return -1
        
        col_score += gameboard[(col, row)].heuristics(gameboard, color, col, row)
        print(str(col_score))
        potential_move = moves_so_far + str(col)
        if potential_move in self.prev_moves:
            col_score *= self.prev_moves[potential_move]["score"]
        
        return col_score







#


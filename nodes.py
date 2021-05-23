# Node Class

import numpy as np
import math

num_rows = 6
num_cols = 7

def is_valid_coordinates(arr):
    if arr[0] >= 0 and arr[1] >= 0 and arr[0] < num_cols and arr[1] < num_rows:
        return True
    return False

class Node():
    # ------------------------------------------------------------------
    # Each Node is a space on the gameboard, has pointer to every neighbor
    # ------------------------------------------------------------------
    def __init__(self, x, y):
        self.coordinates = np.array((x,y))
        self.token = "S"
        # need neighbor ptr, don't need relative_coordinates and don't need orientation
        self.neighbors = {"left_down": None, "left_": None, "left_up": None, "_down": None, \
                                "_up": None, "right_down": None, "right_": None, "right_up": None }


    def connect_to_neighbors(self, gameboard):
        for neighbor in self.neighbors:
            neighbor_coordinates = self.coordinates + orientation_mapping[neighbor]["relative_coords"]
            if is_valid_coordinates(neighbor_coordinates):
                self.neighbors[neighbor] = gameboard[tuple(neighbor_coordinates)]

    def is_winning_token(self):
        orientations = {"horizontal": 1, "vertical": 1, "leading_diag": 1, "counter_diag": 1}

        for neighbor in self.neighbors:
            current_node = self
            while current_node.neighbors[neighbor] is not None and current_node.neighbors[neighbor].token == self.token:
                current_node = current_node.neighbors[neighbor]
                orientations[orientation_mapping[neighbor]["orientation"]] += 1

        for value in orientations.values():
            if value >= 4:
                return True

        return False



    def heuristics(self, gameboard, color, col, row):
        opposite_color = "blue" if color == "red" else "red"

        if self.can_win(gameboard, color, col, row) == True: # if you can win this move, do it
            print("WIN", end=": ")
            return 100

        if self.can_win(gameboard, opposite_color, col, row) == True: # if opponent can win in this spot, take it
            print("BLOCK", end=": ")
            return 90

        if row+1 < 6 and self.can_win(gameboard, opposite_color, col, row+1) == True: # if opponent can win on top next move, don't do it
            print("LOST COLUMN", end=": ")
            return -1

        if row+2 < 6 and self.can_win(gameboard, color, col, row+1) == True and self.can_win(gameboard, color, col, row+2) == True: #if you can force a win, do it
            print("CATCH 22", end=": ")
            return 80

        if row+1 < 6 and self.can_win(gameboard, color, col, row+1) == True: #if you can win on top, don't go here
            print("WON COLUMN", end=": ")
            return -1

        #if strategies/edge cases don't apply, calculate score based on incidence/three in a rows, emphasis on offense rather than defense

        return 2 * self.num_incident(gameboard, color, col, row) + 2 * self.num_threes(gameboard, color, col, row) \
                    + self.num_incident(gameboard, opposite_color, col, row) + self.num_threes(gameboard, opposite_color, col, row)

            #NUM THREES SHOULD HAVE AT LEAST 1 SPACE (> 0)
    def num_incident(self, gameboard, color, col, row):
        score = 0
        #max score is 7
        token = color[0]
        for nbr in self.neighbors:
            neighbor = self.neighbors[nbr]
            if neighbor is not None and neighbor.token == token:
                score += 1
        return score

    def num_threes(self, gameboard, color, col, row):

        orientations = {"horizontal": 1, "vertical": 1, "leading_diag": 1, "counter_diag": 1}

        score = 0
        #max score is 4
        token = color[0]
        for nbr in self.neighbors:
            neighbor = self.neighbors[nbr]
            space_counter = 0
            while neighbor is not None and (neighbor.token == token or neighbor.token == "S") and space_counter < 2:

                if neighbor.token == "S":
                    space_counter += 1
                else:
                    orientations[orientation_mapping[nbr]["orientation"]] += 1
                neighbor = neighbor.neighbors[nbr]

        for value in orientations.values():
            if value >= 3:
                score += 1

        return score

    def can_win(self, gameboard, color, col, row):

        orientations = {"horizontal": 1, "vertical": 1, "leading_diag": 1, "counter_diag": 1}

        #max score is 20, 0 otherwise
        current_node = gameboard[(col,row)]
        token = color[0]
        for nbr in current_node.neighbors:
            neighbor = current_node.neighbors[nbr]
            space_counter = 0
            while neighbor is not None and neighbor.token == token:
                orientations[orientation_mapping[nbr]["orientation"]] += 1
                neighbor = neighbor.neighbors[nbr]

        for value in orientations.values():
            if value >= 4:
                return True
        return False

orientation_mapping = {"left_down":
                            {"orientation": "leading_diag",
                             "relative_coords": np.array((-1,-1)) },
                       "left_":
                             {"orientation": "horizontal",
                            "relative_coords": np.array((-1,0)) },
                       "left_up":
                            {"orientation": "counter_diag",
                             "relative_coords": np.array((-1,1)) },
                       "_down":
                            {"orientation": "vertical",
                            "relative_coords": np.array((0,-1)) },
                       "_up":
                            {"orientation": "vertical",
                             "relative_coords": np.array((0,1)) },
                       "right_down":
                            {"orientation": "counter_diag",
                             "relative_coords": np.array((1,-1)) },
                       "right_":
                            {"orientation": "horizontal",
                             "relative_coords": np.array((1,0)) },
                       "right_up":
                            {"orientation": "leading_diag",
                             "relative_coords": np.array((1,1)) }
                        }











#

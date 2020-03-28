import numpy as np
from .utils.board_utils import *
#from .optimizations.deadzone_algorithm import convolve


#   Retrieval function for index_mapping 
def get_square_by_id(self, index):
    x = self.index_mapping[index][0]
    y = self.index_mapping[index][1]
    return self.squares[x][y]


#   Sets the respective levels of large and small ziggurats at a given location
#   by calling create_ziggurat_starting_at() in board_utils.py
#       NOTE: Simple example layout: [["E5", LARGE_ZIG]]
#       This method also passes self.zig_tops (the promotion squares) so that
#       create_ziggurat_starting_at() can generate a list of all promotion squares
def create_ziggurats(self, layout):
    for ziggurat_data in layout:
        x = self.index_mapping[ziggurat_data[0]][0]
        y = self.index_mapping[ziggurat_data[0]][1]
        create_ziggurat_starting_at(x, y, ziggurat_data[1], self.squares, self.zig_tops)


#   Setup utility for placing a piece on the board
def place_piece(self, piece, loc, owned_by):
    self.get_square_by_id(loc).piece = pieces[piece]
    if owned_by == "P1":
        self.get_square_by_id(loc).ownership = self.player_one_name
    if owned_by == "P2":
        self.get_square_by_id(loc).ownership = self.player_two_name
    self.get_square_by_id(loc).mark = allocate_mark(pieces[piece], self.player_one_turn)


#   Toggles self.player_one_turn on/ off, changes self.current_player 
def change_turns(self):
    self.player_one_turn = not self.player_one_turn
    if self.player_one_turn == True:
        self.current_player = self.player_one_name
    else:
        self.current_player = self.player_two_name


#   Display for dubugging
def display(self):
    self.template_data = []
    trimmed_image = [[sq.mark for sq in row] for row in self.gameplay_squares][1: -1]
    rotated_board_rows = list(zip(*trimmed_image))[::-1]
    ranks = list(reversed(self.numeric_markers))
    spaced_alpha_markers = [" " + i + " " for i in self.alpha_markers]
    for i in range(len(rotated_board_rows)):
        self.template_data.append(str(rotated_board_rows[i]).replace("'", "").replace(",", "").replace("(", "").replace(")", "") + "\t\t" + str(ranks[i]))
        print(ranks[i], "\t", rotated_board_rows[i])
    print("\t", spaced_alpha_markers)
    #
    #   NOTE: Line below is currently trimming alpha_markers for the debugger [:-4]
    #
    self.template_data.append(str(self.alpha_markers[:-4]).replace("'", "|").replace(",", "").replace("[", "").replace("]", ""))


#   Updates the self.game_state dictionary
#   This method should be called after checking whether self.parse returns True
#   If so, it will update the game state. Otherwise, it will return False and
#   the player will be prompted to take their turn again
def update_game_state(self):
    if self.valid_move and not self.game_over:
        
        prev_player = self.player_one_name if not self.player_one_turn else self.player_two_name
        self.check_hubris_rule()
        self.check_unholy_structs_rule()
        make_promotions(self.zig_tops, prev_player, self.player_one_name, self.player_two_name, phase="turn_end")
        deadzone_algorithm(self.squares, self.player_one_turn, self.player_one_name, self.player_two_name)
        self.valid_move = False
        self.game_state["Current Player"] = self.player_one_name if self.player_one_turn else self.player_two_name
        for row in self.squares:
            for sq in row:
                self.game_state[str(sq.index[0])+":"+str(sq.index[1])] = sq.__dict__
        self.change_turns()
        deadzone_algorithm(self.squares, self.player_one_turn, self.player_one_name, self.player_two_name)
        make_promotions(self.zig_tops, prev_player, self.player_one_name, self.player_two_name, phase="turn_start")
        self.collect_data()

        

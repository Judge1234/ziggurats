import numpy as np
from .utils.board_utils import *
from .optimizations.deadzone_algorithm import convolve


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
        self.template_data.append(str(rotated_board_rows[i]).replace("'", "").replace(",", "").replace("(", "").replace(")", ""))
        print(ranks[i], "\t", rotated_board_rows[i])
    print("\t", spaced_alpha_markers)
    self.template_data.append(str(self.alpha_markers).replace("'", "|").replace(",", "").replace("[", "").replace("]", ""))


#   Board encoder for deadzone algorithm optimizations
def encode(self):
    encoded_board = np.ndarray(self.height * self.width * 3, dtype=np.int).reshape(self.height, self.width, 3)
    encoded_board.fill(0)
    encoded_sq = [0, 0, 0]
    p1_name = self.player_one_name
    p2_name = self.player_two_name
    for i in range(self.height):
        for j in range(self.width):
            current = self.squares[i][j]
            if current.p1_deadzone == False and \
                current.p2_deadzone == False and \
                current.mutual_deadzone == False:
                encoded_sq[0] = 0
            if current.p1_deadzone:
                encoded_sq[0] = 1
            if current.p2_deadzone:
                encoded_sq[0] = 2
            if current.mutual_deadzone:
                encoded_sq[0] = 3
            if current.ownership == None:
                encoded_sq[1] = 0
            if current.ownership == p1_name:
                encoded_sq[1] = 1
            if current.ownership == p2_name:
                encoded_sq[1] = 2
            if current.piece == pieces["no piece"]:
                encoded_sq[2] = 0
            if current.piece != pieces["no piece"]:
                encoded_sq[2] = 1
        
            encoded_board[i][j] = np.array(encoded_sq)
    
    return encoded_board


#   Board decoder for deadzone algorithm optimizations
def decode(self, convolution):
    for i in range(len(convolution)):
        for j in range(len(convolution)):
            sq_data = convolution[i][j]
            if sq_data[0] == 0:
                self.squares[i][j].p1_deadzone = False
                self.squares[i][j].p2_deadzone = False
                self.squares[i][j].mutual_deadzone = False
            if sq_data[0] == 1:
                self.squares[i][j].p1_deadzone = True
                self.squares[i][j].p2_deadzone = False
                self.squares[i][j].mutual_deadzone = False
            if sq_data[0] == 2:
                self.squares[i][j].p1_deadzone = False
                self.squares[i][j].p2_deadzone = True
                self.squares[i][j].mutual_deadzone = False
            if sq_data[0] == 3:
                self.squares[i][j].p1_deadzone = False
                self.squares[i][j].p2_deadzone = False
                self.squares[i][j].mutual_deadzone = True
            if sq_data[1] == 0:
                self.squares[i][j].ownership = None
            if sq_data[1] == 1:
                self.squares[i][j].ownership = self.player_one_name
            if sq_data[1] == 2:
                self.squares[i][j].ownership = self.player_two_name
            self.squares[i][j].piece = sq_data[2]  


#   Updates the self.game_state dictionary
#   This method should be called after checking whether self.parse returns True
#   If so, it will update the game state. Otherwise, it will return False and
#   the player will be prompted to take their turn again
def update_game_state(self):
    if self.valid_move:

        #   CYTHON START
        encoded_board_state = self.encode()
        convolution = convolve(encoded_board_state)
        self.decode(convolution)
        #   CYTHON END

        prev_player = self.player_two_name if not self.player_one_turn else self.player_two_name
        make_promotions(self.zig_tops, self.current_player, self.player_one_name, self.player_two_name, phase="turn_end")

        self.valid_move = False
        self.game_state["Current Player"] = self.player_one_name if self.player_one_turn else self.player_two_name
        for row in self.squares:
            for sq in row:
                self.game_state[str(sq.index[0])+":"+str(sq.index[1])] = sq.__dict__
        self.change_turns()
        make_promotions(self.zig_tops, prev_player, self.player_one_name, self.player_two_name, phase="turn_start")

def old_update_game_state(self):
    if self.valid_move:
        
        #   OLD CODE VERSION START
        deadzone_algorithm(self.squares, self.player_one_turn, self.player_one_name, self.player_two_name)
        #   OLD CODE VERSION END

        prev_player = self.player_two_name if not self.player_one_turn else self.player_two_name
        make_promotions(self.zig_tops, self.current_player, self.player_one_name, self.player_two_name, phase="turn_end")

        self.valid_move = False
        self.game_state["Current Player"] = self.player_one_name if self.player_one_turn else self.player_two_name
        for row in self.squares:
            for sq in row:
                self.game_state[str(sq.index[0])+":"+str(sq.index[1])] = sq.__dict__
        self.change_turns()
        make_promotions(self.zig_tops, prev_player, self.player_one_name, self.player_two_name, phase="turn_start")

        

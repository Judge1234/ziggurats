from .utils.square import Square
from .utils.markers import markers
import string


class Board:
    
    from .primary_methods import get_square_by_id, \
                                 create_ziggurats, \
                                 place_piece, \
                                 change_turns, \
                                 display, \
                                 update_game_state
                                 
    from ._movement import MV, MG, SP
    from ._parser import parse
    from ._legalities import validate, check_range_and_path
    from ._rule_checking import check_hubris_rule, check_unholy_structs_rule
    from ._data_collection import collect_data
    
    def __init__(self, height, width, p1_name, p2_name):

        #   Game logic members
        self.height = height
        self.width = width
        self.squares = []
        self.gameplay_squares = []
        self.index_mapping = {}
        self.player_one_name = p1_name
        self.player_two_name = p2_name
        self.player_one_turn = True
        self.current_player = self.player_one_name
        self.valid_move = False
        self.p1_turn_data = []
        self.p2_turn_data = []
        self.game_over = False

        #   Promotion squares
        self.zig_tops = []

        #   Entire game state member
        self.game_state = {}

        #   Terminal display members
        self.alpha_markers = []
        self.numeric_markers = []

        #   debug.html template display members
        self.template_data = []
        self.display_data = {}
        
        #   Squares are generated here
        for i in range(self.height):
            row = []
            for j in range(self.width):
                entry = Square([i, j])
                row.append(entry)
            self.squares.append(row)

        #   --- Out of bounds squares are set below --- 

        #   First row
        for sq in self.squares[0]:
            sq.out_of_bounds = True
            sq.mark = markers["NO_BOUNDS_MARK"]
        
        #   First column minus first and last element 
        for i in range(self.height - 2):
            sq = self.squares[i+1][0]
            sq.out_of_bounds = True
            sq.mark = markers["NO_BOUNDS_MARK"]
            
        #   Bottom row
        for sq in self.squares[-1]:
            sq.out_of_bounds = True
            sq.mark = markers["NO_BOUNDS_MARK"]

        #   Last column minus first and last element
        for i in range(self.height - 2):
            sq = self.squares[i+1][-1]
            sq.out_of_bounds = True
            sq.mark = markers["NO_BOUNDS_MARK"]
            
        #   --- Alphanumeric mapping to in-bounds squares is set below ---

        #   alpha_markers and numeric_markers are self.width minus two
        #   since out-of-bounds exists on both sides of the board
        self.alpha_markers = [list(string.ascii_uppercase)[i] for i in range(self.width-2)]
        self.numeric_markers = list(range(1, len(self.alpha_markers)+1))
        alphanumeric_indices = []
        sq_index_list = []

        #   Matching "A" with "1" to create "A1","B" with "2" to create "B2", etc. 
        for letter in self.alpha_markers:
            for number in self.numeric_markers:
                alphanumeric_indices.append(letter + str(number))
        

        #   Creating a list of the indices of all in-bounds squares
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if self.squares[i][j].out_of_bounds == False:
                    sq_index_list.append(self.squares[i][j].index)
                    row.append(self.squares[i][j])
            self.gameplay_squares.append(row)
        

        #   Zipping alphanumeric_indices and sq_index_list into self.index_mapping
        #   Ex: "A1" matches with [1, 1] (not [0, 0], which is out of bounds)
        self.index_mapping = dict(list(zip(alphanumeric_indices, sq_index_list)))
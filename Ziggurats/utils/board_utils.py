
from .markers import markers 


LARGE_ZIG = 5
SMALL_ZIG = 3


pieces = {"no piece":           0,
          "small":              1,
          "medium":             2, 
          "large":              3,
          "prince":             4,
          "king":               5,
          "transport empty":    6,
          "transport full":     7,
          "promotion process":  8}


#   Consumes a Layout.layout a list containing each ziggurat's location
#   and size. The location of a ziggurat is referenced by the square
#   its left corner is on
#   Called in a loop by Board.create_ziggurats
def create_ziggurat_starting_at(x, y, size, squares, tops):

    for i in range(size):
        for j in range(size):
            first_level = squares[x+i][y+j]
            first_level.level = 1
            first_level.mark = "[1]"

    for i in range(size-2):
        for j in range(1, size-1):
            second_level = squares[x+(i+1)][y+j]
            second_level.level = 2
            second_level.mark = "[2]"

    if size == LARGE_ZIG:
        top_level = squares[x+2][y+2]
        top_level.level = 3
        top_level.mark = "[3]"
        tops.append(squares[x+2][y+2])

    if size == SMALL_ZIG:
        top_level = squares[x+1][y+1]
        top_level.level = 2
        top_level.mark = "[2]"


#   Utility function to set the marker of a square's level 
def reset_level_mark(square):
    if square.level == 0:
        square.mark = markers["GROUND_LEVEL_MARK"]
    if square.level == 1:
        square.mark = markers["ZIG_LOW_MARK"]
    if square.level == 2:
        square.mark = markers["ZIG_MED_MARK"]
    if square.level == 3:
        square.mark = markers["ZIG_TOP_MARK"]


#   Utility function for visual debugging
def allocate_mark(piece, p1_turn):
    if piece == pieces["small"]:
        return markers["P1_SMALL"] if p1_turn else markers["P2_SMALL"]
    if piece == pieces["medium"]:
        return markers["P1_MED"] if p1_turn else markers["P2_MED"]
    if piece == pieces["large"]:
        return markers["P1_LARGE"] if p1_turn else markers["P2_LARGE"]
    if piece == pieces["prince"]:
        return markers["P1_PRINCE"] if p1_turn else markers["P2_PRINCE"]
    if piece == pieces["king"]:
        return markers["P1_KING"] if p1_turn else markers["P2_KING"]
    if piece == pieces["transport empty"]:
        return markers["P1_TPORT_EMPTY"] if p1_turn else markers["P2_TPORT_EMPTY"]
    if piece == pieces["transport full"]:
        return markers["P1_TPORT_FULL"] if p1_turn else markers["P2_TPORT_FULL"]
    if piece == pieces["promotion process"]:
        return markers["P1_PROMO"] if p1_turn else markers["P2_PROMO"]



#   Removes old deadzones and creates new deadzones
#   Used in Board.update_game_state()
def deadzone_algorithm(squares, player_one_turn, p1_name, p2_name):
    deltas = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    #   Pass 1: remove old deadzones
    for i in range(len(squares)-1):
        for j in range(len(squares)-1):
            squares[i][j].p1_deadzone = False
            squares[i][j].p2_deadzone = False
            squares[i][j].mutual_deadzone = False
            if squares[i][j].piece == pieces["no piece"]:
                squares[i][j].ownership = None          # CAREFUL!!!
                reset_level_mark(squares[i][j])

    # Pass 2: create new deadzones
    for i in range(len(squares)-1):
        for j in range(len(squares)-1):
            p1_supports = 0
            p2_supports = 0
            current_square = squares[i][j]
            for delta in deltas:
                neighbour = squares[i + delta[0]][j + delta[1]]
                if neighbour.ownership == p1_name:
                    p1_supports += 1
                if neighbour.ownership == p2_name:
                    p2_supports += 1
            if p1_supports == 2 and p2_supports == 2:
                current_square.mutual_deadzone = True
                current_square.mark = markers["MUTUAL_DEADZONE"]
                break
            if p1_supports >= 2:
                current_square.p1_deadzone = True
                if current_square.ownership == p2_name and current_square.piece != ["no piece"]:
                    current_square.ownership = p1_name
                    current_square.piece = pieces["no piece"]
                    current_square.mark = markers["P1_DEADZONE"]
                if current_square.ownership == p1_name and current_square.piece != ["no piece"]:
                    allocate_mark(current_square.piece, player_one_turn)

            if p2_supports >= 2:
                current_square.p2_deadzone = True
                if current_square.ownership == p1_name and current_square.piece != ["no piece"]:
                    current_square.ownership = p2_name
                    current_square.piece = pieces["no piece"]
                    current_square.mark = markers["P2_DEADZONE"]
                if current_square.ownership == p2_name and current_square.piece != ["no piece"]:
                    allocate_mark(current_square.piece, player_one_turn)
            

#   Used to set pieces in a "promotion process" before becoming a king (if phase="turn_start")
#   Also used to promote a piece to a king (if phase="turn_end")
#   NOTE:   In terms of visual debugging, allocate_mark() cannot be used here, 
#           since the incoming player variable will not match the player owning a newly-promoted piece 
def make_promotions(promo_squares, player, p1_name, p2_name, phase="turn_start"):
    if phase == "turn_start":
        for sq in promo_squares:
            #   [0, 5] here == "no piece" or "king"
            if sq.piece not in [0, 5]:
                sq.piece = pieces["promotion process"]
                sq.promotion_process = True
                sq.ownership = player
                sq.mark = markers["P2_PROMO"] if player == p1_name else markers["P1_PROMO"]
    if phase == "turn_end":
        for sq in promo_squares:
            if sq.piece == pieces["promotion process"]:
                sq.piece = pieces["king"]
                sq.promotion_process = False
                sq.ownership = player
                sq.mark = markers["P1_KING"] if player == p1_name else markers["P2_KING"]



#   Movement deltas - added to a Square's index to create a movement vector
#   Used in Board.SP and Board.check_range_and_path
directions = {
    "north":     lambda distance:   [[0, i] for i in range(distance)],
    "south":     lambda distance:   [[0, -i] for i in range(distance)],
    "east":      lambda distance:   [[i, 0] for i in range(distance)], 
    "west":      lambda distance:   [[-i, 0] for i in range(distance)],
    "northeast": lambda distance:   [[i, i] for i in range(distance)],
    "northwest": lambda distance:   [[-i, i] for i in range(distance)],
    "southeast": lambda distance:   [[i, -i] for i in range(distance)],
    "southwest": lambda distance:   [[-i, -i] for i in range(distance)]
}


def recover_original_state(source_sq, target_sq, source_pc, target_pc, current_player, p1_turn):
    source_sq.piece = source_pc
    source_sq.ownership = current_player
    source_sq.mark = allocate_mark(source_pc, p1_turn)

    target_sq.piece = target_pc
    target_sq.ownership = current_player
    target_sq.mark = allocate_mark(source_pc, p1_turn)


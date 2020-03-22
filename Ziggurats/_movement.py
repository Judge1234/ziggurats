from .utils.markers import markers
from .utils.board_utils import pieces, reset_level_mark, allocate_mark, directions


#   --- MV defined below ---

def MV(self, source, target):
    #   check if there's a piece on the square you're trying to move from
    source_square = self.get_square_by_id(source)
    target_square = self.get_square_by_id(target)

    moving_piece = source_square.piece
    moving_mark = source_square.mark

    target_square.piece = moving_piece
    target_square.mark = moving_mark
    target_square.ownership = self.current_player

    reset_level_mark(source_square) 
    source_square.ownership = None
    source_square.piece = pieces["no piece"]

#   --- MG defined below ---

def MG(self, source, target):
    source_square = self.get_square_by_id(source)
    target_square = self.get_square_by_id(target)

    #   Merging a small with a medium to make a prince
    if target_square.piece == pieces["medium"]:
        if source_square.piece == pieces["small"]:
            target_square.piece = pieces["prince"]
            target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name
            target_square.mark = markers["P1_PRINCE"] if self.player_one_turn else markers["P2_PRINCE"]
            source_square.piece = pieces["no piece"]
            source_square.ownership = None
            reset_level_mark(source_square)
    
    #   Merging a prince with a large to make a king
    if target_square.piece == pieces["large"]:
        if source_square.piece == pieces["prince"]:
            target_square.piece = pieces["king"]
            target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name
            target_square.mark = markers["P1_KING"] if self.player_one_turn else markers["P2_KING"]
            source_square.piece = pieces["no piece"]
            source_square.ownership = None
            reset_level_mark(source_square)

    #   Merging a king with an empty transport to make a full transport
    if target_square.piece == pieces["transport empty"]:
        if source_square.piece == pieces["king"]:
            target_square.piece = pieces["transport full"]
            target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name
            target_square.mark = markers["P1_TPORT_FULL"] if self.player_one_turn else markers["P2_TPORT_FULL"]
            source_square.piece = pieces["no piece"]
            source_square.ownership = None
            reset_level_mark(source_square)

#   --- SP defined below ---

def SP(self, source, target, direction):

    source_square = self.get_square_by_id(source)
    target_square = self.get_square_by_id(target)


    #   Routine for splitting a prince
    if source_square.piece == pieces["prince"] and (target_square.piece == pieces["no piece"] or source == target):
        distance = 2
        if source_square != target_square:
            source_square.ownership = None
            source_square.piece = pieces["no piece"]
            reset_level_mark(source_square)

        target_square.piece = pieces["medium"]
        target_square.mark = markers["P1_MED"] if self.player_one_turn else markers["P2_MED"]
        target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name

        dx = directions[direction](distance)[1][0]
        dy = directions[direction](distance)[1][1]

        small_sq = self.squares[target_square.index[0] + dx][target_square.index[1] + dy]
        small_sq.piece = pieces["small"]
        small_sq.mark = markers["P1_SMALL"] if self.player_one_turn else markers["P2_SMALL"]
        small_sq.ownership = self.player_one_name if self.player_one_turn else self.player_two_name
    
    #   Routine for splitting a king
    if source_square.piece == pieces["king"] and (target_square.piece == pieces["no piece"] or source == target):
        distance = 3
        if source_square != target_square:
            source_square.ownership = None
            source_square.piece = pieces["no piece"]
            reset_level_mark(source_square)

        target_square.piece = pieces["large"]
        target_square.mark = markers["P1_LARGE"] if self.player_one_turn else markers["P2_LARGE"]
        target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name

        detatchments = ["medium", "small"]

        for i in range(1, len(detatchments) + 1):

            dx = directions[direction](distance)[i][0]
            dy = directions[direction](distance)[i][1]

            sq = self.squares[target_square.index[0] + dx][target_square.index[1] + dy]
            sq.piece = pieces[detatchments[i-1]]
            sq.mark = allocate_mark(sq.piece, self.player_one_turn)
            sq.ownership = self.player_one_name if self.player_one_turn else self.player_two_name

    #   Routine for unloading a full transport
    if source_square.piece == pieces["transport full"] and (target_square.piece == pieces["no piece"] or source == target):
        distance = 4
        if source_square != target_square:
            source_square.ownership = None
            source_square.piece = pieces["no piece"]
            reset_level_mark(source_square)

        target_square.piece = pieces["transport empty"]
        target_square.mark = markers["P1_TPORT_EMPTY"] if self.player_one_turn else markers["P2_TPORT_EMPTY"]
        target_square.ownership = self.player_one_name if self.player_one_turn else self.player_two_name

        detatchments = ["large", "medium", "small"]

        for i in range(1, len(detatchments) + 1):

            dx = directions[direction](distance)[i][0]
            dy = directions[direction](distance)[i][1]

            sq = self.squares[target_square.index[0] + dx][target_square.index[1] + dy]
            sq.piece = pieces[detatchments[i-1]]
            sq.mark = allocate_mark(sq.piece, self.player_one_turn)
            sq.ownership = self.player_one_name if self.player_one_turn else self.player_two_name





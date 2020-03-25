from .utils.board_utils import pieces, reset_level_mark

def check_hubris_rule(self):
    current_turn_data = self.p1_turn_data if self.player_one_turn else self.p2_turn_data
    for sq in self.zig_tops:
        if sq.piece == pieces["king"] and sq.index not in current_turn_data[-1]:
            print(current_turn_data)
            x = sq.index[0] - 1
            y = sq.index[1] - 1
            for i in range(3):
                for j in range(3):
                    level_2_sq = self.squares[x+i][y+j]
                    level_2_sq.piece = pieces["no piece"]
                    level_2_sq.ownership = None
                    reset_level_mark(level_2_sq)
from .utils.board_utils import pieces, reset_level_mark


def check_hubris_rule(self):
    current_turn_data = self.p1_turn_data if self.player_one_turn else self.p2_turn_data
    for sq in self.zig_tops:
        if sq.piece == pieces["king"] and sq.index not in current_turn_data[-1]:
            x = sq.index[0] - 1
            y = sq.index[1] - 1
            for i in range(3):
                for j in range(3):
                    hubris_sq = self.squares[x+i][y+j]
                    hubris_sq.piece = pieces["no piece"]
                    hubris_sq.ownership = None
                    reset_level_mark(hubris_sq)





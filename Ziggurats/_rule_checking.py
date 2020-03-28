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


def check_unholy_structs_rule(self):
    deltas = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for i in range(len(self.squares)-1):
        for j in range(len(self.squares)-1):
            current_square = self.squares[i][j]
            perimeter_count = 0
            for delta in deltas:
                neighbour = self.squares[i + delta[0]][j + delta[1]]
                if neighbour.ownership == self.current_player:
                    perimeter_count += 1

            if perimeter_count == 4:
                for delta in deltas:
                    neighbour = self.squares[i + delta[0]][j + delta[1]]
                    neighbour.piece = pieces["no piece"]
                    neighbour.ownership = None
                    neighbour.p1_deadzone = False
                    neighbour.p2_deadzone = False
                    neighbour.mutual_deadzone = False
                    reset_level_mark(neighbour)

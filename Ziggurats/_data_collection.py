from .utils.board_utils import pieces


def collect_data(self):
    default_value = 0
    p1_keys = ["p1 " + f"{p}" for p in list(pieces.keys())[1:]]
    p2_keys = ["p2 " + f"{p}" for p in list(pieces.keys())[1:]]
    self.display_data = dict.fromkeys(p1_keys + p2_keys, default_value)
    for i in range(len(self.squares)-1):
        for j in range(len(self.squares)-1):
            current_square = self.squares[i][j]
            for piece in pieces:
                if current_square.ownership == self.player_one_name and current_square.piece == pieces[piece]:
                    self.display_data["p1 " + f"{piece}"] += 1
                if current_square.ownership == self.player_two_name and current_square.piece == pieces[piece]:
                    self.display_data["p2 " + f"{piece}"] += 1
from .board_utils import pieces


class Square:
    def __init__(self, index):

        self.index = index
        self.mark = "[ ]"
        self.piece = pieces["no piece"]
        self.ownership = None
        self.level = 0
        self.promotion_process = False
        self.out_of_bounds = False 
        self.p1_deadzone = False
        self.p2_deadzone = False
        self.mutual_deadzone = False
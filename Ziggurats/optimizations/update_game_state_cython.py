
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



def update_game_state(self):
    if self.valid_move:

        #self.check_hubris_rule()

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
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
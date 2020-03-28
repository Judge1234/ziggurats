from .utils.board_utils import pieces, directions, reset_level_mark    



#   Checks to see if a move is within legal range.
#   Also checks to see if a piece's path is blocked (in the case of all commands)
#   Used in Board.validate()
def check_range_and_path(self, max_distance, index1, index2, command_type, SP_direction=None):
    x1 = index1[0]
    y1 = index1[1]
    x2 = index2[0]
    y2 = index2[1]
    
    dx = x2 - x1
    dy = y2 - y1

    if dx > max_distance or dy > max_distance:
        print("distance issue")
        return False

    distance = max(abs(x2 - x1), abs(y2 - y1)) 
    print("distance is ", distance, f"between [{x1}, {y1}] and [{x2}, {y2}]")
    direction = None

    #   Determine direction of travel
    if dx == 0 and dy > 0:
        direction = "north"
    elif dx == 0 and dy < 0:
        direction = "south"
    elif dx > 0 and dy == 0:
        direction = "east"
    elif dx < 0 and dy == 0:
        direction = "west"
    #   Diagonal directionality is asserted by insisting 
    #   that the absolute value of dx and dy are equal
    elif dx > 0 and dy > 0 and abs(dx) == abs(dy):
        direction = "northeast"
    elif dx < 0 and dy > 0 and abs(dx) == abs(dy):
        direction = "northwest"
    elif dx > 0 and dy < 0 and abs(dx) == abs(dy):
        direction = "southeast"
    elif dx < 0 and dy < 0 and abs(dx) == abs(dy):
        direction = "southwest"
    #   In this case there is no direction 
    #   (source == target)
    elif dx == 0 and dy == 0:
        deltas = [[0, 0]]
    else:
        return False

    print("checking CMD type for CRP")
    #   Pathing validation routine for "MV" and "SP" (in the case of source == target )
    if command_type == "MV" or (command_type == "SP" and dx != dy):
        print("MV or SP no-dir")
        deltas = list(directions[direction](distance + 1))[1:]
        print(deltas)

        for i in range(len(deltas)):
            in_path_sq = self.squares[x1 + deltas[i][0]][y1 + deltas[i][1]]
            if self.squares[x1][y1].piece in [pieces["transport empty"], pieces["transport full"]]:
                if in_path_sq.level != 0:
                    print("transport hit a ziggurat")
                    return False
            #   Accounting for opponent deadzones
            opponent_deadzone = in_path_sq.p2_deadzone if self.player_one_turn else in_path_sq.p1_deadzone
            if (in_path_sq.piece != pieces["no piece"] and in_path_sq != self.squares[x1][y1]) or \
                in_path_sq.out_of_bounds or in_path_sq.mutual_deadzone or opponent_deadzone: 
                return False
            

    if command_type == "MG":
        print("MG")
        deltas = list(directions[direction](distance + 1))[1: -1]
        print(deltas)

        for i in range(len(deltas)):
            in_path_sq = self.squares[x1 + deltas[i][0]][y1 + deltas[i][1]]
            #   Accounting for opponent deadzones
            opponent_deadzone = in_path_sq.p2_deadzone if self.player_one_turn else in_path_sq.p1_deadzone
            #   Ensure that the source square's piece is not confused for a piece that is
            #   blocking the movement path in the case of index1 == index2
            if (in_path_sq.piece != pieces["no piece"] and in_path_sq != self.squares[x1][y1]) or in_path_sq.out_of_bounds or \
                in_path_sq.mutual_deadzone or opponent_deadzone:
                print("something here")
                return False

    #   Validate split portion of SP commands
    if command_type == "SP":
        print("SP detected inside CRP")
        source_sq = self.squares[x1][y1]
        if source_sq.piece == pieces["prince"]:
            SP_distance = 2
        elif source_sq.piece == pieces["king"]:
            SP_distance = 3
        elif source_sq.piece == pieces["transport full"]:
            SP_distance = 4
        else:
            return False

        print("SP_direction = ", SP_direction)
        sp_vector_coords = directions[SP_direction](SP_distance)

        for i in sp_vector_coords[1:]:
            sp_sq = self.squares[x2 + i[0]][y2 + i[1]]
            opponent_deadzone = sp_sq.p2_deadzone if self.player_one_turn else sp_sq.p1_deadzone
            #   The first part of this condition is meant to prevent self-blocking
            #   in the case of "splitting backwards" as well as preventing re-promotion
            if sp_sq != self.squares[x1][y1] and (sp_sq.ownership != None or sp_sq.out_of_bounds) or \
               sp_sq.mutual_deadzone or opponent_deadzone or (source_sq.level == 3 and sp_sq == 3):
                return False

    return True


#   Main movement command validation routines
def validate(self, source, target, command_type, SP_direction=None):
    try:
        source_sq = self.get_square_by_id(source)
        target_sq = self.get_square_by_id(target)
    except (KeyError, IndexError):
        return False

    if source_sq.piece == None:
        return False

    #   Validation routine for MV command
    if command_type == "MV":
        print("command is MV")
        #   Ownership validation
        if source_sq.ownership == self.current_player and target_sq.ownership == None:
            if source_sq.piece == pieces["transport full"]:
                return False
            print("source is good, target is not owned")
            distance = 3 if source_sq.piece != pieces["transport empty"] else max(self.height, self.width)
            print("DISTANCE is", distance)
            idx1 = source_sq.index
            idx2 = target_sq.index
            #   Range, movement & promotion validation
            if self.check_range_and_path(distance, idx1, idx2, "MV") == True and source_sq.promotion_process == False:
                print("CRD is good")
                return True
        else:
            return False

    #   Validation routine for MG command
    if command_type == "MG":
        #   Ownership validation
        if source_sq.ownership == self.current_player and target_sq.ownership == self.current_player:
            idx1 = source_sq.index
            idx2 = target_sq.index
            distance = 3
            #   Validation by merging pairs
            if source_sq.piece == pieces["small"] and target_sq.piece == pieces["medium"]:
                if self.check_range_and_path(distance, idx1, idx2, "MG") == True and source_sq.promotion_process == False:
                    return True
            if source_sq.piece == pieces["prince"] and target_sq.piece == pieces["large"]:
                if self.check_range_and_path(distance, idx1, idx2, "MG") == True and source_sq.promotion_process == False:
                    return True
            if source_sq.piece == pieces["king"] and target_sq.piece == pieces["transport empty"]:
                if self.check_range_and_path(distance, idx1, idx2, "MG") == True and source_sq.promotion_process == False:
                    return True
            else:
                return False

    #   Validation routine for SP command
    if command_type == "SP":
        print("SP detected")
        #   Ownership validation
        if source_sq.ownership == self.current_player and target_sq.ownership == None or \
           (source_sq.ownership == self.current_player and source_sq == target_sq):
            print("I own the square")
            idx1 = source_sq.index
            idx2 = target_sq.index
            distance = 3 if source_sq.piece != pieces["transport full"] else max(self.height, self.width)
            print("source sq piece is ", source_sq.piece)
            print("DISTANCE is ", distance)
            if self.check_range_and_path(distance, idx1, idx2, "SP", SP_direction=SP_direction):
                return True
    else:
        return False




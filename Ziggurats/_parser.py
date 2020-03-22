from .utils.board_utils import pieces, allocate_mark, recover_original_state
from .primary_methods import get_square_by_id

#    --- Receives, parses and validates commands as a list of strings --- 

def parse(self, commands):
     cmd_size = len(commands)
     #    Case for cmd_size == 1
     if cmd_size == 1:
          return False

     #    Case for cmd_size == 2
     if cmd_size == 2:
          return False

     #    Case for cmd_size == 3
     if cmd_size == 3:
          if commands[2] == "MV":
               print("case size 3 is MV")
               source = commands[0]
               target = commands[1]
               if self.validate(source, target, "MV"):
                    print("good MV")
                    self.MV(source, target)
                    return True
               else:
                    return False
          
          if commands[2] == "MG":
               source = commands[0]
               target = commands[1]
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    return True
          else:
               return False

     #    Case for cmd_size == 4
     if cmd_size == 4:
          if commands[2] == "SP":
               source = commands[0]
               target = commands[1]
               direction = commands[3]
               if self.validate(source, target, "SP", SP_direction=direction):
                    self.SP(source, target, direction)
                    return True
          else:
               return False

     #    Case for cmd_size == 5
     if cmd_size == 5:
          return False

     #    Case for cmd_size == 6
     if cmd_size == 6:
          if commands[2] == "MG" and commands[5] == "MV":
               source = commands[0]
               target = commands[1]
               if self.validate(source, target, "MG"):
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MV"):
                         source = commands[0]
                         target = commands[1]
                         self.MG(source, target)
                         source = commands[3]
                         target = commands[4]
                         self.MV(source, target)
                         return True
               
          if commands[2] == "MG" and commands[5] == "MG":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         return True
                    else:
                         source_sq = self.get_square_by_id(commands[0])
                         target_sq = self.get_square_by_id(commands[1])

                         recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)

          else:
               return False

     #    Case for cmd_size == 7
     if cmd_size == 7:
          if commands[2] == "MG" and commands[5] == "SP":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    direction = commands[6]
                    if self.validate(source, target, "SP", SP_direction=direction):
                         self.SP(source, target, direction)
                         return True
                    else:
                         source_sq = self.get_square_by_id(commands[0])
                         target_sq = self.get_square_by_id(commands[1])

                         recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)


          if commands[2] == "MV" and commands[5] == "SP":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MV"):
                    self.MV(source, target)
                    source = commands[3]
                    target = commands[4]
                    direction = commands[6]
                    if self.validate(source, target, "SP", SP_direction=direction):
                         self.SP(source, target, direction)
                         return True
                    else:
                         source_sq = self.get_square_by_id(commands[0])
                         target_sq = self.get_square_by_id(commands[1])

                         recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)

          else:
               return False

     #    Case for cmd_size == 8
     if cmd_size == 8:
          return False

     #    Case for cmd_size == 9
     if cmd_size == 9:
          if commands[2] == "MG" and commands[5] == "MG" and commands[8] == "MV":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         source = commands[6]
                         target = commands[7]
                         if self.validate(source, target, "MV"):
                              self.MV(source, target)
                              return True
                         else:
                              source_sq = self.get_square_by_id(commands[0])
                              target_sq = self.get_square_by_id(commands[1])
                              
                              recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)

          if commands[2] == "MG" and commands[5] == "MG" and commands[8] == "MG":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         source = commands[6]
                         target = commands[7]
                         if self.validate(source, target, "MG"):
                              self.MG(source, target)
                              return True
                         else:
                              source_sq = self.get_square_by_id(commands[0])
                              target_sq = self.get_square_by_id(commands[1])
                              
                              recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)

          else:
               return False

     #    Case for cmd_size == 10
     if cmd_size == 10:
          if commands[2] == "MG" and commands[5] == "MG" and commands[8] == "SP":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         source = commands[6]
                         target = commands[7]
                         direction = commands[9]
                         if self.validate(source, target, "SP", SP_direction=direction):
                              self.SP(source, target, direction)
                              return True
                         else:
                              source_sq = self.get_square_by_id(commands[0])
                              target_sq = self.get_square_by_id(commands[1])

                              recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)


          if commands[2] == "MV" and commands[5] == "MG" and commands[8] == "SP":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MV"):
                    self.MV(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         source = commands[6]
                         target = commands[7]
                         direction = commands[9]
                         if self.validate(source, target, "SP", SP_direction=direction):
                              self.SP(source, target, direction)
                              return True
                         else:
                              source_sq = self.get_square_by_id(commands[0])
                              target_sq = self.get_square_by_id(commands[1])

                              recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)
          else:
               return False
          
     if cmd_size == 11:
          return False

     if cmd_size == 12:
          return False
     
     if cmd_size == 13:
          if commands[2] == "MG" and commands[5] == "MG" and commands[8] == "MG" and commands[11] == "SP":
               source = commands[0]
               target = commands[1]
               source_pc = self.get_square_by_id(source).piece
               target_pc = self.get_square_by_id(target).piece
               if self.validate(source, target, "MG"):
                    self.MG(source, target)
                    source = commands[3]
                    target = commands[4]
                    if self.validate(source, target, "MG"):
                         self.MG(source, target)
                         source = commands[6]
                         target = commands[7]
                         if self.validate(source, target, "MG"):
                              self.MG(source, target)
                              source = commands[9]
                              target = commands[10]
                              direction = commands[11]
                              if self.validate(source, target, "SP", SP_direction=direction):
                                   self.SP(source, target, direction)
                                   return True
                         else:
                              source_sq = self.get_square_by_id(commands[0])
                              target_sq = self.get_square_by_id(commands[1])

                              recover_original_state(source_sq, target_sq, source_pc, target_pc, self.current_player, self.p1_turn)

from flask import Flask, request, jsonify, redirect, url_for, render_template
from Ziggurats import Board
from Ziggurats.utils.board_lib import *
from Ziggurats.utils.board_utils import *
from Ziggurats.utils.markers import markers


app = Flask(__name__)
layout = Small_Standard_Layout
game = Board(layout.width, layout.height, "Player One", "Player Two")
game.update_game_state()
game.valid_move = True

game.create_ziggurats(layout.layout)

for piece in layout.p1_spawn_locations:
    game.place_piece(piece[0], piece[1], piece[2])

for piece in layout.p2_spawn_locations:
    game.place_piece(piece[0], piece[1], piece[2])



@app.route("/play", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        game.display()
        submission = request.form.get("command")
        command = submission.split()       
        if game.parse(command):
            game.valid_move = True
            if game.player_one_turn:
                game.move_history.append(str(game.player_one_name) + ": " + " ".join([i for i in game.p1_turn_data[-1]]))
            if not game.player_one_turn:
                game.move_history.append(str(game.player_two_name) + ": " + " ".join([i for i in game.p2_turn_data[-1]]))
            game.update_game_state()
            game.display()
        else:
            pass

    return render_template("debug.html", turn=game.current_player,
                                         p1_name=game.player_one_name,
                                         p2_name=game.player_two_name,
                                         pieces=game.display_data,
                                         game_history=game.move_history, 
                                         display=game.template_data)
    

if __name__ == "__main__":
    app.run(debug=True)




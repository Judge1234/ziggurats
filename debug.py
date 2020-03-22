from flask import Flask, request, jsonify, redirect, url_for, render_template
from Ziggurats import Board
from Ziggurats.utils.board_utils import *
from Ziggurats.utils.markers import markers


app = Flask(__name__)
game = Board(13, 13, "Player One", "Player Two")
game.update_game_state()
game.valid_move = True

fake_layout = [["D4", LARGE_ZIG]]

game.create_ziggurats(fake_layout)

game.player_one_turn = True
game.place_piece("king", "A4", "P1")
game.place_piece("king", "A5", "P1")
game.place_piece("king", "A7", "P1")
game.place_piece("king", "A8", "P1")
game.player_one_turn = False
game.place_piece("king", "K4", "P2")
game.place_piece("king", "K5", "P2")
game.place_piece("king", "K7", "P2")
game.place_piece("king", "K8", "P2")
game.player_one_turn = True



@app.route("/play", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        game.display()
        submission = request.form.get("command")
        command = submission.split()
        game.display()
        if game.parse(command):
            game.valid_move = True
            game.update_game_state()
            game.display()
        else:
            pass

    return render_template("debug.html", turn=game.current_player, 
                                         display=game.template_data)
    


    
if __name__ == "__main__":
    app.run(debug=True)

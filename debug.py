from flask import Flask, request, jsonify, redirect, url_for, render_template
from Ziggurats import Board
from Ziggurats.utils.board_utils import *
from Ziggurats.utils.markers import markers


app = Flask(__name__)
game = Board(13, 17, "Player One", "Player Two")
game.update_game_state()
game.valid_move = True

fake_layout = [["D6", LARGE_ZIG]]

game.create_ziggurats(fake_layout)

game.player_one_turn = True

game.place_piece("king", "A6", "P1")
game.place_piece("king", "A7", "P1")
game.place_piece("king", "A8", "P1")
game.place_piece("king", "A9", "P1")
game.place_piece("king", "A10", "P1")
game.player_one_turn = False

game.place_piece("king", "K6", "P2")
game.place_piece("king", "K7", "P2")
game.place_piece("king", "K8", "P2")
game.place_piece("king", "K9", "P2")
game.place_piece("king", "K10", "P2")
game.player_one_turn = True

history = []

@app.route("/play", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        game.display()
        submission = request.form.get("command")
        command = submission.split()       
        if game.parse(command):
            game.valid_move = True
            if game.player_one_turn:
                history.append(str(game.player_one_name) + ": " + " ".join([i for i in game.p1_turn_data[-1]]))
            if not game.player_one_turn:
                history.append(str(game.player_two_name) + ": " + " ".join([i for i in game.p2_turn_data[-1]]))
            game.update_game_state()
            game.display()
        else:
            pass

    

    return render_template("debug.html", turn=game.current_player,
                                         p1_name=game.player_one_name,
                                         p2_name=game.player_two_name,
                                         pieces=game.display_data,
                                         game_history=history, 
                                         display=game.template_data)
    


    
if __name__ == "__main__":
    app.run(debug=True)




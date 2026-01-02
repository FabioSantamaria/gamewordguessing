from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from game_logic import GameLogic
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session
CORS(app)

game_logic = GameLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/games', methods=['POST'])
def create_game():
    game_id = game_logic.create_new_game()
    return jsonify({"game_id": game_id, "message": "Game created successfully"}), 201

@app.route('/api/games/<game_id>/join', methods=['POST'])
def join_game(game_id):
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    player_name = data.get('player_name')
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    player_name = player_name.upper()
    game_id = game_id.upper()
    
    if not game_logic.get_game(game_id):
         return jsonify({"error": "Game not found"}), 404

    if game_logic.add_player(player_name, game_id) or game_logic.player_exists_in_game(player_name, game_id):
        # Store in session
        session['player_name'] = player_name
        session['game_id'] = game_id
        return jsonify({"message": f"Joined game {game_id}", "player_name": player_name}), 200
    else:
        return jsonify({"error": "Could not join game. Name might be taken or game error."}), 400

@app.route('/api/games/<game_id>/start', methods=['POST'])
def start_game(game_id):
    game_id = game_id.upper()
    if game_logic.start_game(game_id):
        return jsonify({"message": "Game started"}), 200
    return jsonify({"error": "Could not start game (need 2+ players)"}), 400

@app.route('/api/games/<game_id>/status', methods=['GET'])
def game_status(game_id):
    # Try to get player_name from query param, then fallback to session
    player_name = request.args.get('player_name')
    if not player_name and 'player_name' in session:
        player_name = session['player_name']

    if not player_name:
        return jsonify({"error": "player_name required"}), 400
    
    game_id = game_id.upper()
    player_name = player_name.upper()
        
    game_data = game_logic.get_game(game_id)
    
    if not game_data:
        return jsonify({"error": "Game not found"}), 404
        
    visible_data = game_logic.get_visible_data_for_player(player_name, game_id)
    active = game_logic.is_game_active(game_id)
    players = game_logic.get_players(game_id)
    
    # Check if player is assigned
    # Note: get_player_assignment returns empty dict if not assigned or not found
    assignment = game_logic.get_player_assignment(player_name, game_id)
    
    return jsonify({
        "game_id": game_id,
        "active": active,
        "players": players,
        "visible_data": visible_data,
        "assignment": assignment,
        "is_player_in_game": player_name in players
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

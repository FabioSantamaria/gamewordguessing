import random
import os
import string
import json
from typing import List, Dict, Tuple, Optional

class GameLogic:
    def __init__(self):
        self.games = {}  # Dictionary to store multiple games by game_id
        self.current_game_id = None
        self.personajes = []
        self.contextos = []
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_data")
        
        # Create game_data directory if it doesn't exist
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)
            
        self.load_data()
        self.load_games_from_json()
    
    def generate_game_id(self) -> str:
        """Generate a unique 6-character game ID"""
        while True:
            game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if game_id not in self.games:
                return game_id
    
    def create_new_game(self) -> str:
        """Create a new game session and return the game_id"""
        game_id = self.generate_game_id()
        self.games[game_id] = {
            'players': [],
            'assignments': {},
            'created_at': None,
            'active': False
        }
        self.current_game_id = game_id
        self.save_game_to_json(game_id)
        return game_id
    
    def get_game(self, game_id: str) -> Optional[Dict]:
        """Get game data by game_id"""
        return self.games.get(game_id)
    
    def set_current_game(self, game_id: str) -> bool:
        """Set the current active game"""
        if game_id in self.games:
            self.current_game_id = game_id
            return True
        return False
    
    def get_current_game_data(self) -> Optional[Dict]:
        """Get current game data"""
        if self.current_game_id:
            return self.games.get(self.current_game_id)
        return None
    
    def load_data(self):
        """Load personajes and contextos from data files"""
        try:
            # Load personajes
            with open('data/personajes.txt', 'r', encoding='utf-8') as f:
                self.personajes = [line.strip() for line in f.readlines() if line.strip()]
            
            # Load contextos
            with open('data/contextos.txt', 'r', encoding='utf-8') as f:
                self.contextos = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError as e:
            print(f"Error loading data files: {e}")
            # Fallback data if files don't exist
            self.personajes = ["Harry Potter", "Sherlock Holmes", "Superman", "Batman"]
            self.contextos = ["En una cita romántica", "En el supermercado", "En una entrevista de trabajo", "En el dentista"]
    
    def add_player(self, player_name: str, game_id: str = None) -> bool:
        """Add a player to the specified game"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return False
        
        game_data = self.games[target_game_id]
        if player_name and player_name not in game_data['players']:
            game_data['players'].append(player_name)
            self.save_game_to_json(target_game_id)
            return True
        return False
    
    def remove_player(self, player_name: str, game_id: str = None) -> bool:
        """Remove a player from the specified game"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return False
        
        game_data = self.games[target_game_id]
        if player_name in game_data['players']:
            game_data['players'].remove(player_name)
            if player_name in game_data['assignments']:
                del game_data['assignments'][player_name]
            self.save_game_to_json(target_game_id)
            return True
        return False
    
    def start_game(self, game_id: str = None) -> bool:
        """Start the game by assigning random personajes and contextos to players"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return False
        
        game_data = self.games[target_game_id]
        if len(game_data['players']) < 2:
            return False
        
        # Clear previous assignments
        game_data['assignments'] = {}
        
        # Create random assignments for each player
        available_personajes = self.personajes.copy()
        available_contextos = self.contextos.copy()
        
        for player in game_data['players']:
            # Randomly select personaje and contexto
            personaje = random.choice(available_personajes)
            contexto = random.choice(available_contextos)
            
            # Remove selected items to avoid duplicates (optional)
            if len(available_personajes) > 1:
                available_personajes.remove(personaje)
            if len(available_contextos) > 1:
                available_contextos.remove(contexto)
            
            # If we run out of unique items, refill the lists
            if not available_personajes:
                available_personajes = self.personajes.copy()
            if not available_contextos:
                available_contextos = self.contextos.copy()
            
            game_data['assignments'][player] = {
                'personaje': personaje,
                'contexto': contexto
            }
        
        game_data['active'] = True
        self.save_game_to_json(target_game_id)
        return True
    
    def get_visible_data_for_player(self, current_player: str, game_id: str = None) -> List[Dict]:
        """Get the game data visible to a specific player (all except their own row)"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return []
        
        game_data = self.games[target_game_id]
        visible_data = []
        
        for player in game_data['players']:
            if player != current_player and player in game_data['assignments']:
                visible_data.append({
                    'JUGADOR': player,
                    'PERSONAJE': game_data['assignments'][player]['personaje'],
                    'CONTEXTO': game_data['assignments'][player]['contexto']
                })
        
        return visible_data
    
    def get_player_assignment(self, player_name: str, game_id: str = None) -> Dict:
        """Get the assignment for a specific player"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return {}
        
        game_data = self.games[target_game_id]
        return game_data['assignments'].get(player_name, {})
    
    def is_game_active(self, game_id: str = None) -> bool:
        """Check if the game is currently active"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return False
        
        game_data = self.games[target_game_id]
        return game_data.get('active', False) and len(game_data.get('assignments', {})) > 0
    
    def reset_game(self, game_id: str = None):
        """Reset the specified game state"""
        target_game_id = game_id or self.current_game_id
        if target_game_id and target_game_id in self.games:
            self.games[target_game_id] = {
                'players': [],
                'assignments': {},
                'created_at': None,
                'active': False
            }
            self.save_game_to_json(target_game_id)
    
    def get_all_assignments(self, game_id: str = None) -> Dict:
        """Get all assignments for the specified game"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return {}
        
        game_data = self.games[target_game_id]
        return game_data['assignments'].copy()
    
    def get_players(self, game_id: str = None) -> List[str]:
        """Get list of players in the specified game"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return []
        
        game_data = self.games[target_game_id]
        return game_data['players'].copy()
    
    def player_exists_in_game(self, player_name: str, game_id: str) -> bool:
        """Check if a player exists in the specified game"""
        if game_id not in self.games:
            return False
        
        game_data = self.games[game_id]
        return player_name in game_data['players']
        
    def save_game_to_json(self, game_id: str):
        """Save a specific game to a JSON file"""
        if game_id not in self.games:
            return False
        
        game_data = self.games[game_id]
        json_file_path = os.path.join(self.json_dir, f"{game_id}.json")
        
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game to JSON: {e}")
            return False
            
    def reload_game_from_json(self, game_id: str) -> bool:
        """Reload a specific game from its JSON file"""
        if not game_id:
            return False
            
        json_file_path = os.path.join(self.json_dir, f"{game_id}.json")
        
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    game_data = json.load(f)
                    self.games[game_id] = game_data
                return True
            return False
        except Exception as e:
            print(f"Error reloading game from JSON: {e}")
            return False
    
    def load_games_from_json(self):
        """Load all saved games from JSON files"""
        if not os.path.exists(self.json_dir):
            return
        
        try:
            for filename in os.listdir(self.json_dir):
                if filename.endswith('.json'):
                    game_id = filename[:-5]  # Remove .json extension
                    json_file_path = os.path.join(self.json_dir, filename)
                    
                    with open(json_file_path, 'r', encoding='utf-8') as f:
                        game_data = json.load(f)
                        self.games[game_id] = game_data
        except Exception as e:
            print(f"Error loading games from JSON: {e}")
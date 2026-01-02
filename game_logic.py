import random
import os
import string
from typing import List, Dict, Tuple, Optional

class GameLogic:
    def __init__(self):
        self.games = {}  # Dictionary to store multiple games by game_id
        self.current_game_id = None
        self.personajes = []
        self.contextos = []
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
        self.load_data()
    
    def generate_game_id(self) -> str:
        """Generate a unique 3-character game ID"""
        while True:
            game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
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
        return True
    
    def get_visible_data_for_player(self, current_player: str, game_id: str = None) -> List[Dict]:
        """Get the game data visible to a specific player (all except their own row)"""
        target_game_id = game_id or self.current_game_id
        if not target_game_id or target_game_id not in self.games:
            return []
        
        game_data = self.games[target_game_id]
        visible_data = []

        print(game_data)
        
        for player in game_data['players']:
            if player != current_player and player in game_data['assignments']:
                visible_data.append({
                    'JUGADOR': player,
                    'PERSONAJE': game_data['assignments'][player]['personaje'],
                    'CONTEXTO': game_data['assignments'][player]['contexto']
                })
        
        print(visible_data)

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

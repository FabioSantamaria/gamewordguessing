import random
import os
from typing import List, Dict, Tuple

class GameLogic:
    def __init__(self):
        self.players = []
        self.game_assignments = {}
        self.personajes = []
        self.contextos = []
        self.load_data()
    
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
    
    def add_player(self, player_name: str) -> bool:
        """Add a player to the game if not already exists"""
        if player_name and player_name not in self.players:
            self.players.append(player_name)
            return True
        return False
    
    def remove_player(self, player_name: str) -> bool:
        """Remove a player from the game"""
        if player_name in self.players:
            self.players.remove(player_name)
            if player_name in self.game_assignments:
                del self.game_assignments[player_name]
            return True
        return False
    
    def start_game(self) -> bool:
        """Start the game by assigning random personajes and contextos to players"""
        if len(self.players) < 2:
            return False
        
        # Clear previous assignments
        self.game_assignments = {}
        
        # Create random assignments for each player
        available_personajes = self.personajes.copy()
        available_contextos = self.contextos.copy()
        
        for player in self.players:
            # Randomly select personaje and contexto
            personaje = random.choice(available_personajes)
            contexto = random.choice(available_contextos)
            
            # Remove selected items to avoid duplicates (optional - you can comment these lines if you want duplicates)
            if len(available_personajes) > 1:
                available_personajes.remove(personaje)
            if len(available_contextos) > 1:
                available_contextos.remove(contexto)
            
            # If we run out of unique items, refill the lists
            if not available_personajes:
                available_personajes = self.personajes.copy()
            if not available_contextos:
                available_contextos = self.contextos.copy()
            
            self.game_assignments[player] = {
                'personaje': personaje,
                'contexto': contexto
            }
        
        return True
    
    def get_visible_data_for_player(self, current_player: str) -> List[Dict]:
        """Get the game data visible to a specific player (all except their own row)"""
        visible_data = []
        
        for player in self.players:
            if player != current_player and player in self.game_assignments:
                visible_data.append({
                    'JUGADOR': player,
                    'PERSONAJE': self.game_assignments[player]['personaje'],
                    'CONTEXTO': self.game_assignments[player]['contexto']
                })
        
        return visible_data
    
    def get_player_assignment(self, player_name: str) -> Dict:
        """Get the assignment for a specific player (for admin view or debugging)"""
        return self.game_assignments.get(player_name, {})
    
    def is_game_active(self) -> bool:
        """Check if the game is currently active"""
        return len(self.game_assignments) > 0
    
    def reset_game(self):
        """Reset the game state"""
        self.players = []
        self.game_assignments = {}
    
    def get_all_assignments(self) -> Dict:
        """Get all assignments (for admin view)"""
        return self.game_assignments.copy()
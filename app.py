import streamlit as st
import pandas as pd
from game_logic import GameLogic

# Configure page
st.set_page_config(
    page_title="Juego de Adivinanzas Multijugador",
    page_icon="🎭",
    layout="wide"
)

# Initialize game logic in session state
if 'game' not in st.session_state:
    st.session_state.game = GameLogic()

# Initialize session state variables
if 'current_player' not in st.session_state:
    st.session_state.current_player = ""
if 'current_game_id' not in st.session_state:
    st.session_state.current_game_id = ""

def main():
    st.title("🎭 Juego de Adivinanzas Multijugador")
    
    # Game connection section at the top
    st.header("🔗 Conexión al Juego")
    
    col1, col2 = st.columns(2)
    
    with col1:
        game_id_input = st.text_input(
            "ID del Juego (para unirse a un juego existente):",
            value=st.session_state.current_game_id,
            placeholder="Ej: ABC123",
            help="Deja vacío para crear un nuevo juego"
        )
    
    with col2:
        player_name_input = st.text_input(
            "Tu Nombre:",
            value=st.session_state.current_player,
            placeholder="Ingresa tu nombre"
        ).upper()
    
    # Connection buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎮 Unirse/Crear Juego", type="primary"):
            if player_name_input:
                if game_id_input:
                    # Try to join existing game
                    if st.session_state.game.get_game(game_id_input.upper()):
                        st.session_state.current_game_id = game_id_input.upper()
                        st.session_state.game.set_current_game(game_id_input.upper())
                        
                        # Add player to the game
                        if st.session_state.game.add_player(player_name_input, game_id_input.upper()):
                            st.session_state.current_player = player_name_input
                            st.success(f"¡Te has unido al juego {game_id_input.upper()}!")
                        else:
                            if st.session_state.game.player_exists_in_game(player_name_input, game_id_input.upper()):
                                st.session_state.current_player = player_name_input
                                st.success(f"¡Bienvenido de vuelta, {player_name_input}!")
                            else:
                                st.error("No se pudo unir al juego. El nombre puede estar en uso.")
                        st.rerun()
                    else:
                        st.error(f"No se encontró el juego con ID: {game_id_input.upper()}")
                else:
                    # Create new game
                    new_game_id = st.session_state.game.create_new_game()
                    st.session_state.current_game_id = new_game_id
                    st.session_state.game.add_player(player_name_input, new_game_id)
                    st.session_state.current_player = player_name_input
                    st.success(f"¡Nuevo juego creado! ID: {new_game_id}")
                    st.rerun()
            else:
                st.error("Por favor ingresa tu nombre")
    
    with col2:
        if st.button("🔄 Actualizar Conexión"):
            if st.session_state.current_game_id and st.session_state.current_player:
                # Reload the game data from JSON file
                if st.session_state.game.reload_game_from_json(st.session_state.current_game_id):
                    st.session_state.game.set_current_game(st.session_state.current_game_id)
                    st.success("Datos del juego actualizados desde archivo")
                else:
                    st.session_state.game.set_current_game(st.session_state.current_game_id)
                    st.warning("No se encontró archivo de juego, usando datos en memoria")
                st.session_state.game.start_game(st.session_state.current_game_id)
                st.rerun()
    
    with col3:
        if st.button("🚪 Salir del Juego"):
            if st.session_state.current_game_id and st.session_state.current_player:
                st.session_state.game.remove_player(st.session_state.current_player, st.session_state.current_game_id)
            st.session_state.current_player = ""
            st.session_state.current_game_id = ""
            st.success("Has salido del juego")
            st.rerun()
    
    # Game controls
    if st.session_state.current_game_id:
        st.subheader("Controles del Juego")
        
        control_col1, control_col2 = st.columns(2)
        
        with control_col1:
            if st.button("🎮 Iniciar Nuevo Juego"):
                if st.session_state.game.start_game(st.session_state.current_game_id):
                    st.success("¡Juego iniciado! Se han asignado personajes y contextos.")
                    st.rerun()
                else:
                    st.error("No se pudo iniciar el juego. Se necesitan al menos 2 jugadores.")
        
        with control_col2:
            if st.button("🔄 Reiniciar Juego"):
                # do you really want to reset the game? yes or no
                st.warning("⚠️ ¡Advertencia! Esto eliminará todos los jugadores y reiniciará el juego.")
                st.info("¿Estás seguro de que deseas reiniciar el juego?")
                if st.button("Confirmar Reinicio"):
                    st.session_state.game.reset_game(st.session_state.current_game_id)
                    st.success("Juego reiniciado. Todos los jugadores han sido eliminados.")
                    st.rerun()
                if st.button("Cancelar"):
                    st.info("Reinicio del juego cancelado.")
                    st.rerun()
    
    # Game status and information
    if st.session_state.current_game_id and st.session_state.current_player:
        st.header(f"🎲 Juego: {st.session_state.current_game_id}")
        
        # Display connected players
        players = st.session_state.game.get_players(st.session_state.current_game_id)
        st.subheader("👥 Jugadores Conectados")
        st.write(", ".join(players))
        
        # Game activity
        if st.session_state.game.is_game_active(st.session_state.current_game_id):
            st.success("✅ El juego está activo")
            
            # Player's assignment - hidden since players need to guess their own character and context
            st.subheader("🎭 Tu Misión")
            st.info("¡Adivina tu personaje y contexto formulando preguntas de sí/no al resto de jugadores!")
            
            # Table of other players (visible to current player)
            st.subheader("📋 Tabla de Juego")
            visible_data = st.session_state.game.get_visible_data_for_player(st.session_state.current_player, st.session_state.current_game_id)
            
            if visible_data:
                df = pd.DataFrame(visible_data)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.info("No hay datos para mostrar en la tabla")
        else:
            st.warning("⏳ El juego aún no ha comenzado")
            st.info("Espera a que se inicie el juego para recibir tu personaje y contexto")
    else:
        st.info("🎯 Ingresa un ID de juego para unirte o deja el campo vacío para crear uno nuevo")
    
    # Instructions
    with st.expander("📝 Instrucciones del Juego"):
        st.markdown("""
        ### Cómo Jugar
        1. **Unirse al Juego**: Ingresa tu nombre y un ID de juego existente, o crea uno nuevo.
        2. **Iniciar el Juego**: Cualquier jugador puede iniciar el juego cuando haya al menos 2 jugadores.
        3. **Adivinar**: Cada jugador recibe un personaje y un contexto. ¡Debes adivinar quién eres basándote en las respuestas de los demás!
        4. **Interactuar**: En tu turno, haz preguntas de sí / no para interactuar con los demás jugadores.
        
        ### Consejos
        - No reveles directamente el personaje o contexto de otro jugador
        - Haz preguntas indirectas para obtener pistas sobre tu personaje
        - ¡Diviértete interpretando mientras interactúas con los demás!
        """)



if __name__ == "__main__":
    main()
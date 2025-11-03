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
if 'show_admin' not in st.session_state:
    st.session_state.show_admin = False

def main():
    st.title("🎭 Juego de Adivinanzas Multijugador")
    st.markdown("---")
    
    # Sidebar for game controls
    with st.sidebar:
        st.header("🎮 Controles del Juego")
        
        # Player name input
        player_name = st.text_input("Tu nombre:", value=st.session_state.current_player)
        
        if st.button("Unirse al Juego"):
            if player_name:
                if st.session_state.game.add_player(player_name):
                    st.session_state.current_player = player_name
                    st.success(f"¡Bienvenido {player_name}!")
                    st.rerun()
                else:
                    st.warning("Este nombre ya está en uso o es inválido")
            else:
                st.error("Por favor ingresa tu nombre")
        
        # Show current players
        if st.session_state.game.players:
            st.subheader("👥 Jugadores Conectados")
            for i, player in enumerate(st.session_state.game.players, 1):
                st.write(f"{i}. {player}")
        
        st.markdown("---")
        
        # Game controls
        if len(st.session_state.game.players) >= 2:
            if st.button("🚀 Iniciar Juego", type="primary"):
                if st.session_state.game.start_game():
                    st.success("¡Juego iniciado!")
                    st.rerun()
                else:
                    st.error("Error al iniciar el juego")
        else:
            st.info("Se necesitan al menos 2 jugadores para iniciar")
        
        if st.session_state.game.is_game_active():
            if st.button("🔄 Reiniciar Juego"):
                st.session_state.game.reset_game()
                st.session_state.current_player = ""
                st.success("Juego reiniciado")
                st.rerun()
        
        # Admin toggle
        st.markdown("---")
        if st.checkbox("👑 Vista de Administrador"):
            st.session_state.show_admin = True
        else:
            st.session_state.show_admin = False
    
    # Main game area
    if not st.session_state.game.is_game_active():
        st.info("🎯 **Instrucciones del Juego:**")
        st.markdown("""
        1. **Cada jugador** debe unirse al juego ingresando su nombre
        2. **Objetivo:** Adivinar tu propio PERSONAJE y CONTEXTO
        3. **Regla:** Puedes ver la información de todos los demás jugadores, pero NO la tuya
        4. **Estrategia:** Haz preguntas a los otros jugadores para descubrir tu identidad
        5. **Ganador:** El primero en adivinar correctamente su PERSONAJE y CONTEXTO
        """)
        
        if len(st.session_state.game.players) >= 2:
            st.success("✅ ¡Listos para jugar! Haz clic en 'Iniciar Juego' en la barra lateral.")
        else:
            st.warning(f"⏳ Esperando jugadores... ({len(st.session_state.game.players)}/2 mínimo)")
    
    else:
        # Game is active
        if st.session_state.show_admin:
            show_admin_view()
        elif st.session_state.current_player:
            show_player_view()
        else:
            st.warning("⚠️ Por favor ingresa tu nombre y únete al juego para ver tu vista personalizada")

def show_player_view():
    """Show the game view for a specific player"""
    current_player = st.session_state.current_player
    
    if current_player not in st.session_state.game.players:
        st.error("❌ No estás registrado en este juego. Por favor únete primero.")
        return
    
    st.header(f"🎭 Vista de {current_player}")
    st.markdown("### 📋 Información de otros jugadores:")
    st.info("💡 **Recuerda:** No puedes ver tu propia información. ¡Pregunta a los demás para descubrirla!")
    
    # Get visible data for current player
    visible_data = st.session_state.game.get_visible_data_for_player(current_player)
    
    if visible_data:
        # Create DataFrame and display as table
        df = pd.DataFrame(visible_data)
        
        # Style the table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "JUGADOR": st.column_config.TextColumn("👤 JUGADOR", width="medium"),
                "PERSONAJE": st.column_config.TextColumn("🎭 PERSONAJE", width="medium"),
                "CONTEXTO": st.column_config.TextColumn("🎬 CONTEXTO", width="large")
            }
        )
        
        st.markdown("---")
        st.markdown("### 🤔 ¿Ya sabes quién eres?")
        
        # Guessing section
        col1, col2 = st.columns(2)
        
        with col1:
            guess_personaje = st.text_input("Tu PERSONAJE:")
        
        with col2:
            guess_contexto = st.text_input("Tu CONTEXTO:")
        
        if st.button("🎯 Verificar Respuesta"):
            player_assignment = st.session_state.game.get_player_assignment(current_player)
            
            if (guess_personaje.strip().lower() == player_assignment['personaje'].lower() and 
                guess_contexto.strip().lower() == player_assignment['contexto'].lower()):
                st.balloons()
                st.success(f"🎉 ¡CORRECTO! {current_player} ha ganado!")
                st.success(f"Eras: **{player_assignment['personaje']}** en **{player_assignment['contexto']}**")
            else:
                st.error("❌ Incorrecto. ¡Sigue preguntando a los demás!")
                
                # Show hints
                if guess_personaje.strip().lower() == player_assignment['personaje'].lower():
                    st.info("✅ El PERSONAJE es correcto")
                if guess_contexto.strip().lower() == player_assignment['contexto'].lower():
                    st.info("✅ El CONTEXTO es correcto")
    
    else:
        st.warning("⏳ Esperando que se unan más jugadores...")

def show_admin_view():
    """Show admin view with all assignments"""
    st.header("👑 Vista de Administrador")
    st.warning("⚠️ Esta vista muestra toda la información del juego. ¡No hagas trampa!")
    
    assignments = st.session_state.game.get_all_assignments()
    
    if assignments:
        # Create complete DataFrame
        admin_data = []
        for player, assignment in assignments.items():
            admin_data.append({
                'JUGADOR': player,
                'PERSONAJE': assignment['personaje'],
                'CONTEXTO': assignment['contexto']
            })
        
        df = pd.DataFrame(admin_data)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "JUGADOR": st.column_config.TextColumn("👤 JUGADOR", width="medium"),
                "PERSONAJE": st.column_config.TextColumn("🎭 PERSONAJE", width="medium"),
                "CONTEXTO": st.column_config.TextColumn("🎬 CONTEXTO", width="large")
            }
        )
    else:
        st.info("No hay asignaciones activas")

if __name__ == "__main__":
    main()
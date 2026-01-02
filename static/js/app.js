let currentGameId = null;
let currentPlayerName = null;
let pollInterval = null;

// Helper for alerts
function showAlert(message, type = 'danger') {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

async function handleCreate() {
    const nameInput = document.getElementById('playerName');
    const name = nameInput.value.trim();
    if (!name) {
        showAlert("Por favor ingresa tu nombre", 'warning');
        return;
    }

    try {
        const res = await fetch('/api/games', { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
            // Now join the created game
            await joinGameRequest(data.game_id, name);
        } else {
            showAlert(data.error || "Error creando juego");
        }
    } catch (e) {
        showAlert("Error de conexión");
        console.error(e);
    }
}

async function handleJoin() {
    const nameInput = document.getElementById('playerName');
    const gameIdInput = document.getElementById('gameIdInput');
    const name = nameInput.value.trim();
    const gameId = gameIdInput.value.trim();

    if (!name) {
        showAlert("Por favor ingresa tu nombre", 'warning');
        return;
    }
    if (!gameId) {
        showAlert("Por favor ingresa el ID del juego", 'warning');
        return;
    }

    await joinGameRequest(gameId, name);
}

async function joinGameRequest(gameId, name) {
    try {
        const res = await fetch(`/api/games/${gameId}/join`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_name: name })
        });
        const data = await res.json();
        
        if (res.ok) {
            currentGameId = gameId.toUpperCase();
            currentPlayerName = data.player_name || name.toUpperCase(); // Use server normalized name
            showGameScreen();
            startPolling();
        } else {
            showAlert(data.error || "Error uniéndose al juego");
        }
    } catch (e) {
        showAlert("Error de conexión");
        console.error(e);
    }
}

function showGameScreen() {
    document.getElementById('login-section').classList.add('d-none');
    document.getElementById('game-section').classList.remove('d-none');
    document.getElementById('displayGameId').textContent = currentGameId;
    document.getElementById('displayPlayerName').textContent = currentPlayerName;
}

function showLoginScreen() {
    document.getElementById('login-section').classList.remove('d-none');
    document.getElementById('game-section').classList.add('d-none');
    stopPolling();
    currentGameId = null;
    currentPlayerName = null;
}

async function startGame() {
    if (!currentGameId) return;
    try {
        const res = await fetch(`/api/games/${currentGameId}/start`, { method: 'POST' });
        const data = await res.json();
        if (!res.ok) {
            showAlert(data.error || "Error iniciando juego");
        }
    } catch (e) {
        console.error(e);
    }
}

function startPolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(updateGameState, 2000); // Poll every 2s
    updateGameState(); // Run immediately
}

function stopPolling() {
    if (pollInterval) clearInterval(pollInterval);
}

async function updateGameState() {
    if (!currentGameId || !currentPlayerName) return;

    // We can rely on session now if desired, but sending query param is safe fallback
    try {
        const res = await fetch(`/api/games/${currentGameId}/status?player_name=${encodeURIComponent(currentPlayerName)}`, {
            cache: "no-store"
        });
        
        if (res.status === 404) {
            // Game deleted?
            showAlert("El juego ya no existe");
            showLoginScreen();
            return;
        }
        
        const data = await res.json();
        
        if (data.error) {
            // Handle specific errors
            return;
        }

        if (!data.is_player_in_game) {
            // Player was removed (e.g. via reset)
            showAlert("Has sido desconectado del juego (¿Reinicio?)");
            showLoginScreen();
            return;
        }

        renderGameState(data);
    } catch (e) {
        console.error("Polling error", e);
    }
}

function renderGameState(data) {
    // Update Active Status
    const badge = document.getElementById('gameStatusBadge');
    const waitingMsg = document.getElementById('waiting-message');
    const gameBoard = document.getElementById('game-board');

    if (data.active) {
        badge.className = "badge bg-success";
        badge.textContent = "Activo";
        gameBoard.classList.remove('d-none');
        waitingMsg.classList.add('d-none');
    } else {
        badge.className = "badge bg-secondary";
        badge.textContent = "Esperando";
        gameBoard.classList.add('d-none');
        waitingMsg.classList.remove('d-none');
    }

    // Update Players List
    const list = document.getElementById('playersList');
    list.innerHTML = '';
    data.players.forEach(p => {
        const badgeSpan = document.createElement('span');
        badgeSpan.className = `badge ${p === currentPlayerName ? 'bg-primary' : 'bg-info'} fs-6`;
        badgeSpan.textContent = p;
        list.appendChild(badgeSpan);
    });

    // Update Game Board
    if (data.active && data.visible_data) {
        const tbody = document.getElementById('gameTableBody');
        tbody.innerHTML = '';
        data.visible_data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${row.JUGADOR}</strong></td>
                <td>${row.PERSONAJE}</td>
                <td>${row.CONTEXTO}</td>
            `;
            tbody.appendChild(tr);
        });
    }
}

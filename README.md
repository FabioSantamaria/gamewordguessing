# 🎭 Juego de Adivinanzas Multijugador

Un juego multijugador divertido donde cada jugador debe adivinar su propio PERSONAJE y CONTEXTO basándose en lo que ven de los demás jugadores.

## 🎮 Cómo Jugar

1. **Únete al juego**: Ingresa tu nombre y haz clic en "Unirse al Juego"
2. **Espera a otros jugadores**: Se necesitan al menos 2 jugadores
3. **Inicia el juego**: Un jugador hace clic en "Iniciar Juego"
4. **Observa y pregunta**: Puedes ver la información de todos los demás, pero no la tuya
5. **Adivina**: Cuando creas saber tu identidad, ingresa tu respuesta
6. **¡Gana!**: El primero en adivinar correctamente su PERSONAJE y CONTEXTO gana

## 🚀 Instalación y Ejecución Local

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona o descarga el proyecto**
   ```bash
   git clone <tu-repositorio>
   cd gamewordguessing
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv .venv
   ```

3. **Activa el entorno virtual**
   - En Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta la aplicación**
   ```bash
   streamlit run app.py
   ```

6. **Abre tu navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`
   - Si no se abre automáticamente, ve a esa dirección manualmente

## 📁 Estructura del Proyecto

```
gamewordguessing/
├── .venv/                 # Entorno virtual (no incluido en git)
├── data/                  # Archivos de datos del juego
│   ├── personajes.txt     # Lista de personajes
│   └── contextos.txt      # Lista de contextos/situaciones
├── app.py                 # Aplicación principal de Streamlit
├── game_logic.py          # Lógica del juego
├── requirements.txt       # Dependencias de Python
├── .gitignore            # Archivos a ignorar en git
└── README.md             # Este archivo
```

## 🌐 Despliegue en Streamlit Community Cloud

### Pasos para desplegar:

1. **Sube tu código a GitHub**
   - Crea un repositorio en GitHub
   - Sube todos los archivos del proyecto

2. **Ve a Streamlit Community Cloud**
   - Visita [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub

3. **Despliega tu aplicación**
   - Haz clic en "New app"
   - Selecciona tu repositorio
   - Especifica la rama (main/master)
   - Especifica el archivo principal: `app.py`
   - Haz clic en "Deploy"

4. **¡Listo!**
   - Tu aplicación estará disponible en una URL pública
   - Comparte la URL con tus amigos para jugar

## 🎯 Características

- **Multijugador**: Varios jugadores pueden unirse desde diferentes dispositivos
- **Vista personalizada**: Cada jugador ve información diferente
- **Interfaz en español**: Toda la UI está en español
- **Fácil de usar**: Interfaz intuitiva con Streamlit
- **Datos personalizables**: Puedes modificar los archivos en `data/` para cambiar personajes y contextos
- **Vista de administrador**: Para supervisar el juego

## 🛠️ Personalización

### Agregar más personajes o contextos:

1. Edita `data/personajes.txt` para agregar más personajes
2. Edita `data/contextos.txt` para agregar más situaciones
3. Cada línea del archivo representa una opción
4. Reinicia la aplicación para cargar los nuevos datos

### Modificar la interfaz:

- Edita `app.py` para cambiar textos, colores o layout
- Modifica `game_logic.py` para cambiar las reglas del juego

## 🐛 Solución de Problemas

- **Error al cargar datos**: Verifica que los archivos en `data/` existan y tengan contenido
- **Problemas de conexión**: Asegúrate de que todos los jugadores estén en la misma URL
- **El juego no inicia**: Verifica que haya al menos 2 jugadores conectados

## 📝 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y mejorarlo.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el juego, no dudes en crear un pull request o abrir un issue.
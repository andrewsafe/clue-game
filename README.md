Clue Game Web Application
This project is a web-based implementation of the classic Clue/Cluedo board game. It features a Flask backend for game logic and state management, and a React frontend for the user interface. The game supports multiple players, each with a unique player_id, and includes a real-time chat system integrated into the gameplay screen.

Multiple Players: Users can join the game from different browsers. Each player is uniquely identified on both the server and the client.
Turns and Moves: The game enforces turn order. Players can only move, suggest, or accuse on their own turn.
Real-Time Updates: Using Socket.IO, all players see live updates for board changes, suggestions, accusations, and game progress.
Chat System: Players can exchange messages in real-time. System messages and in-game status updates also appear in the same chat interface.
Visibility of Cards: Each player can view their own cards. These cards are private and not exposed to other players.
Technology Stack
Backend:

Flask: Handles HTTP routes and Socket.IO communication.
Python & Socket.IO: Real-time events (player actions, chat messages, game states).
Game Logic: Classes for GameSystem, TurnManager, BoardManager, Solution, Card, Suggestion, Accusation.
Frontend:

React.js: Handles the UI with components for different screens (Start, Lobby, Game, End).
Socket.IO Client: Connects to the Flask backend for real-time updates.
CSS: Custom styling for a dark, modern theme.

Getting Started
Backend Setup
Install Python Dependencies:

bash
pip install -r requirements.txt
Run the Flask Server:

bash
flask run
Or, if using socketio.run(app):

bash
python app.py
The server should start on http://localhost:5000.

Frontend Setup
Navigate to client Directory:

bash
cd client
Install Frontend Dependencies:

bash
npm install
Run the React Development Server:

bash
npm start
The React app will start on http://localhost:3000. If configured to use localhost:5000 for the backend, the frontend and backend will communicate seamlessly.

Gameplay Flow
Join the Game: Players start on the StartScreen, entering a name to join.
Lobby: Once a player joins, they appear in the LobbyScreen with any other waiting players. The host or a designated player can start the game.
Game Start: Upon starting, the server deals cards and picks a solution. The GameScreen is displayed, showing the board, the current player, and available actions.
Turns and Actions: Each turn, the active player can move, make suggestions, or accusations. Other players see these actions in real-time.
Game End: The game ends when a correct accusation is made or all but one player have been eliminated by incorrect accusations.
Unique Player Screens
The server generates a unique player_id for each player upon joining. This player_id ensures that each client screen can display personalized data (e.g., the player's own cards).

Key Points:

The player_id is sent to the client once the player is added.
The React app stores this player_id and uses it to filter player-specific data.
Only the player's own information and actions are displayed as relevant to them.
Chat System Integration
The chat is integrated directly into the GameScreen. Players and the system send messages to the same messages array. Chat messages and game status updates both appear in the chat interface.

How It Works:

Server: Listens to chat_message events and broadcasts them via chat_broadcast.
Client (App.js): Handles chat_broadcast events and updates a messages state array.
Client (GameScreen.js): Renders the messages array as a unified stream of chat and system messages.
Sending a Message:

A player types in the chat input box and clicks "Send".
The message is emitted to the server with player_id and message.
The server broadcasts it to all clients, who update their messages array and rerender the chat box.
Game Status Messaging
Previously, system or game status messages were displayed separately. Now, these messages (e.g., "Player X made a suggestion", "Player Y moved to Lounge", "Game Over") are appended to the messages array as system messages. They appear in the chat panel, giving a single unified log of all game-related events.

Implementation:

Events like suggestion_made, accusation_made, or move_made now append a message to the messages array in App.js with a player_id: "SYSTEM" and player_name: "Game".
The chat panel distinguishes system messages (italicized, a different class) from player messages.
Styles and Theming
The project uses a dark theme to match the game's ambiance. The GameScreen.css sets a dark background, teal/blue highlights, and subtle accents. The chat styles are integrated into the same theme, ensuring visual consistency.

Key elements:

Dark Backgrounds (#121212, #1a1a1a, #1e1e1e) and Teal/Blue Highlights (#80d8ff, #1565c0, #004d99).
Buttons, selects, and message boxes follow similar styling rules.
System messages are italicized, and player’s own messages are highlighted to distinguish them from others.
Enjoy playing and experimenting with the Clue web application!

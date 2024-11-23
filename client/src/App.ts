import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import "./css/App.css";
import StartScreen from "./StartScreen.js";
import LobbyScreen from "./LobbyScreen.js";
import GameScreen from "./GameScreen.js";
import EndScreen from "./EndScreen.js";

// Create socket connection
// const socket = io("https://peppy-empanada-ec068d.netlify.app/", {
// const socket = io("http://localhost:5000", {
const socket = io("http://127.0.0.1:5000", {
  transports: ["websocket", "polling"],
});

function App() {
  const [screen, setScreen] = useState("start");
  const [playerId, setPlayerId] = useState("");
  const [players, setPlayers] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState("");
  const [character, setCharacter] = useState("");
  const [location, setLocation] = useState("");
  const [winner, setWinner] = useState(null);
  const [message, setMessage] = useState("");
  const [moves, setMoves] = useState([]);
  const [gameState, setGameState] = useState(null);

  useEffect(() => {
    socket.on("player_added", (data) => {
      if (data.error) {
        console.error(data.error);
      } else {
        // Store the player_id in loginId
        setPlayerId(data.player_id);
        setMessage(data.message);
        console.log(`Player added with ID: ${data.player_id}`);
      }
    });

    socket.on("return_players", (data) => {
      setPlayers(data.players);
    });

    socket.on("game_started", (data) => {
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);
      setMessage(data.message);
      setScreen("game");
      socket.emit("detailed_board");
      socket.emit("get_moves", data.current_player);
    });

    socket.on("board_response", (data) => {
      setGameState(data);
    });

    socket.on("next_turn", (data) => {
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);
      socket.emit("get_moves", data.current_player);
    });

    socket.on("move_options", (data) => {
      setMoves(data.moves);
      setLocation(data.currentLocation);
    });

    socket.on("move_made", (data) => {
      console.log("Move Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("suggestion_made", (data) => {
      console.log("Suggestion Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("accusation_made", (data) => {
      console.log("Accusation Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("game_over", (data) => {
      setWinner(data.winner);
      setMessage(data.message);
      setScreen("end");
    });

    return () => {
      socket.off("return_players");
      socket.off("game_started");
      socket.off("board_response");
      socket.off("next_turn");
      socket.off("move_options");
      socket.off("move_made");
      socket.off("suggestion_made");
      socket.off("accusation_made");
      socket.off("game_over");
    };
  }, []);

  const handleAddPlayer = (player) => {
    socket.emit("add_player", player);
    setScreen("lobby");
  };

  const handleStartGame = () => {
    socket.emit("start_game");
    socket.emit("get_players");
  };

  const handleMove = (moveChoice) => {
    if (!moveChoice) {
      alert("Please select a location to move to.");
      return;
    }
    socket.emit("make_move", moveChoice);
    socket.emit("detailed_board");
    socket.emit("end_turn");
  };

  const handleSuggestion = (suggestion) => {
    if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
      alert("Please complete all suggestion fields.");
      return;
    }
    socket.emit("make_suggestion", suggestion);
    socket.emit("detailed_board");
    socket.emit("end_turn");
  };

  const handleAccusation = (accusation) => {
    if (!accusation.character || !accusation.weapon || !accusation.room) {
      alert("Please complete all accusation fields.");
      return;
    }
    socket.emit("make_accusation", accusation);
    socket.emit("end_turn");
  };

  return (
    <div className="app">
      {screen === "start" && <StartScreen onAddPlayer={handleAddPlayer} />}
      {screen === "lobby" && (
        <LobbyScreen players={players} onStartGame={handleStartGame} />
      )}
      {screen === "game" && (
        <GameScreen
          currentPlayer={currentPlayer}
          onMove={handleMove}
          onSuggestion={handleSuggestion}
          onAccusation={handleAccusation}
          message={message}
          moves={moves}
          location={location}
          gameState={gameState}
          character={character}
          players={players}
          playerId={playerId}
        />
      )}
      {screen === "end" && <EndScreen winner={winner} message={message} />}
    </div>
  );
}

export default App;

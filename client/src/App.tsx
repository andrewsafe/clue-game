import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import "./css/App.css";
import StartScreen from "./StartScreen";
import LobbyScreen from "./LobbyScreen";
import GameScreen from "./GameScreen";
import EndScreen from "./EndScreen";
import { v4 as uuidv4 } from "uuid";
import {
  PlayerAddedData,
  ReturnPlayersData,
  GameStartedData,
  BoardResponseData,
  NextTurnData,
  MoveOptionsData,
  GenericMessageData,
  GameOverData,
  SuggestionOrAccusation,
  Player,
} from "./types";

// Create socket connection
// const socket = io("https://peppy-empanada-ec068d.netlify.app/", {
const socket = io("http://localhost:5000", {
  // const socket = io("http://127.0.0.1:5000", {
  transports: ["websocket", "polling"],
});

const App: React.FC = () => {
  const [screen, setScreen] = useState<"start" | "lobby" | "game" | "end">(
    "start"
  );
  const [playerId, setPlayerId] = useState<string>("");
  const [players, setPlayers] = useState<Player[]>([]);
  const [currentPlayer, setCurrentPlayer] = useState<string>("");
  const [character, setCharacter] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [winner, setWinner] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [moves, setMoves] = useState<string[]>([]);
  const [gameState, setGameState] = useState<string[][]>([]);

  useEffect(() => {
    socket.on("player_added", (data: PlayerAddedData) => {
      if (data.error) {
        console.error(data.error);
      } else {
        // Store the player_id in loginId
        setPlayerId(data.player_id);
        setMessage(data.message);
        console.log(`Player added with ID: ${data.player_id}`);
      }
    });

    socket.on("return_players", (data: ReturnPlayersData) => {
      setPlayers(data.players);
    });

    socket.on("game_started", (data: GameStartedData) => {
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);
      setMessage(data.message);
      setScreen("game");
      socket.emit("detailed_board");
      socket.emit("get_moves", data.current_player);
    });

    socket.on("board_response", (data: BoardResponseData) => {
      setGameState(data);
    });

    socket.on("next_turn", (data: NextTurnData) => {
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);
      socket.emit("get_moves", data.current_player);
    });

    socket.on("move_options", (data: MoveOptionsData) => {
      setMoves(data.moves);
      setLocation(data.currentLocation);
    });

    socket.on("move_made", (data: GenericMessageData) => {
      console.log("Move Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("suggestion_made", (data: GenericMessageData) => {
      console.log("Suggestion Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("accusation_made", (data: GenericMessageData) => {
      console.log("Accusation Made: ", data.message);
      setMessage(data.message);
    });

    socket.on("game_over", (data: GameOverData) => {
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

  const handleAddPlayer = (player: { playerName: string }) => {
    const newPlayer: Player = {
      id: uuidv4(),
      name: player.playerName,
      character: "", // Provide a default or placeholder value
      cards: [], // Optional: Provide an empty array if necessary
    };
    socket.emit("add_player", newPlayer);
    setScreen("lobby");
  };

  const handleStartGame = () => {
    console.log("Start Game button clicked");
    socket.emit("start_game");
    socket.emit("get_players");
  };

  const handleMove = (moveChoice: string) => {
    if (!moveChoice) {
      alert("Please select a location to move to.");
      return;
    }
    socket.emit("make_move", moveChoice);
    socket.emit("detailed_board");
    socket.emit("end_turn");
  };

  const handleSuggestion = (suggestion: SuggestionOrAccusation) => {
    if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
      alert("Please complete all suggestion fields.");
      return;
    }
    socket.emit("make_suggestion", suggestion);
    socket.emit("detailed_board");
    socket.emit("end_turn");
  };

  const handleAccusation = (accusation: SuggestionOrAccusation) => {
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
};

export default App;

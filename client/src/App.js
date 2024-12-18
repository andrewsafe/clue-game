import React, { useState, useEffect, act } from "react";
import io from "socket.io-client";
import "./css/App.css";
import StartScreen from "./StartScreen";
import LobbyScreen from "./LobbyScreen";
import GameScreen from "./GameScreen";
import EndScreen from "./EndScreen.js";

// Create socket connection
const socket = io("https://clue-game-server.onrender.com/", {
// const socket = io("http://localhost:5000", {
  // const socket = io("http://127.0.0.1:5000", {
  transports: ["websocket", "polling"],
});

function App() {
  const [screen, setScreen] = useState("start");
  const [playerId, setPlayerId] = useState("");
  const [players, setPlayers] = useState([]);
  const [localPlayer, setLocalPlayer] = useState(null);
  const [currentPlayer, setCurrentPlayer] = useState("");
  const [character, setCharacter] = useState("");
  const [location, setLocation] = useState("");
  const [winner, setWinner] = useState(null);
  const [message, setMessage] = useState("");
  const [moves, setMoves] = useState([]);
  const [gameState, setGameState] = useState(null);
  const [revealOptions, setRevealOptions] = useState([]); // Cards to reveal
  const [disproveSuggestionState, setDisproveSuggestionState] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inRoom, setInRoom] = useState(false);
  const [playerMoved, setPlayerMoved] = useState(false);
  const [actionMade, setActionMade] = useState(false);
  const [cannotMove, setCannotMove] = useState(false);
  const [movedBySuggestion, setMovedBySuggestion] = useState(false);

  useEffect(() => {
    socket.on("player_added", (data) => {
      if (data.error) {
        console.error(data.error);
      } else {
        // Store the player_id in loginId
        setPlayerId(data.player_id);
        setMessage(data.message);
        setMessages((prev) => [
          ...prev,
          { player_id: "SYSTEM", player_name: "Game", message: data.error },
        ]);
        console.log(`Player added with ID: ${data.player_id}`);
      }
    });

    socket.on("chat_broadcast", (data) => {
      setMessages((prevMessages) => [...prevMessages, data]);
    });

    socket.on("return_players", (data) => {
      if (data.error) {
        console.error(data.error);
        setMessage(data.error);
      } else {
        setPlayers([data.players]);
        for (let player of data.players) {
          if (player.id === playerId) {
            console.log("Match");
            setLocalPlayer(player);
          }
        }
      }
    });

    socket.on("game_started", (data) => {
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.error },
      ]);
      setScreen("game");
      socket.emit("detailed_board");
      socket.emit("get_moves", data.current_player);
    });

    socket.on("board_response", (data) => {
      setGameState(data);
    });

    socket.on("next_turn", (data) => {
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
      setCurrentPlayer(data.current_player);
      setCharacter(data.character);

      if (
        localPlayer.name === data.current_player &&
        data.moved_by_suggestion
      ) {
        setMovedBySuggestion(true);
      }
      socket.emit("get_moves", data.current_player);
    });

    socket.on("move_options", (data) => {
      setMoves(data.moves);
      setLocation(data.currentLocation);
      if (data.currentLocation.length < 5 || data.currentLocation[4] !== "w") {
        setInRoom(true);
      } else {
        setInRoom(false);
      }

      if (data.moves.length === 0) {
        setCannotMove(true);
      }
    });

    socket.on("move_made", (data) => {
      console.log("Move Made: ", data.message);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
      setGameState(data.board);
    });

    socket.on("suggestion_made", (data) => {
      if (data.error) {
        setMessage(data.error);
        setMessages((prev) => [
          ...prev,
          { player_id: "SYSTEM", player_name: "Game", message: data.error },
        ]);
      } else {
        console.log("Suggestion Made: ", data.message);
        setMessage(data.message);
        setMessages((prev) => [
          ...prev,
          { player_id: "SYSTEM", player_name: "Game", message: data.message },
        ]);
      }
    });

    socket.on("suggestion_incorrect", (data) => {
      console.log(data.cards);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
      setDisproveSuggestionState(true);
      setRevealOptions(data.cards);
    });

    socket.on("suggestion_disproved", (data) => {
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
    });

    socket.on("accusation_made", (data) => {
      console.log("Accusation Made: ", data.message);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
    });

    socket.on("player_disconnected", (data) => {
      console.log(data.message);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
      setPlayers(data.remaining_players.map((name) => ({ name })));
    });

    socket.on("game_over", (data) => {
      setWinner(data.winner);
      setMessage(data.message);
      setMessages((prev) => [
        ...prev,
        { player_id: "SYSTEM", player_name: "Game", message: data.message },
      ]);
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
      socket.off("suggestion_incorrect");
      socket.off("suggestion_disproved");
      socket.off("chat_broadcast");
      socket.off("player_disconnected");
      socket.off("game_over");
    };
  }, [playerId, localPlayer]);

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
    setLocation(moveChoice);
    setMessages((prev) => [
      ...prev,
      {
        player_id: "SYSTEM",
        player_name: "Game",
        message: `You have moved your Character ${character} to Room ${moveChoice}.`,
      },
    ]);
    socket.emit("make_move", moveChoice);
    if (moveChoice.length < 5 || moveChoice[4] !== "w") {
      setInRoom(true);
    } else {
      setInRoom(false);
    }
    setLocalPlayer((prevState) => ({
      ...prevState, // Keep the previous properties
      location: moveChoice, // Update the location
    }));
    setActionMade(true);
    setPlayerMoved(true);
    socket.emit("detailed_board");
  };

  const handleSuggestion = (suggestion) => {
    if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
      alert("Please complete all suggestion fields.");
      return;
    }
    let [charId, charStr] = suggestion.character.split(',');
    let [weaponId, weaponStr] = suggestion.weapon.split(',');

    setMessages((prev) => [
      ...prev,
      {
        player_id: "SYSTEM",
        player_name: "Game",
        message: `You are making a suggestion with Suspect: ${charStr}, Weapon: ${weaponStr}, and Room: ${suggestion.room}.`,
      },
    ]);
    
    suggestion.character = charId;
    suggestion.weapon = weaponId;
    switch (suggestion.room) {
      case "Hall":
        suggestion.room = "1";
        break;
      case "Lounge":
        suggestion.room = "2";
        break;
      case "Library":
        suggestion.room = "3";
        break;
      case "Kitchen":
        suggestion.room = "4";
        break;
      case "Billiard Room":
        suggestion.room = "5";
        break;
      case "Study":
        suggestion.room = "6";
        break;
      case "Ballroom":
        suggestion.room = "7";
        break;
      case "Dining Room":
        suggestion.room = "8";
        break;
      default:
        suggestion.room = "9";
        break;
    }
    socket.emit("make_suggestion", suggestion);
    setActionMade(true);
    socket.emit("detailed_board");
  };

  const handleDisproveSuggestion = (revealedCard) => {
    if (!revealedCard) {
      alert("Please select a card to disprove.");
      return;
    }
    setDisproveSuggestionState(false);
    socket.emit(
      "disprove_suggestion",
      localPlayer.name,
      revealedCard,
      currentPlayer
    );
  };

  const handleAccusation = (accusation) => {
    if (!accusation.character || !accusation.weapon || !accusation.room) {
      alert("Please complete all accusation fields.");
      return;
    }
    socket.emit("make_accusation", accusation);
    setActionMade(true);
  };

  const handleEndTurn = () => {
    setMovedBySuggestion(false);
    setActionMade(false);
    setCannotMove(false);
    setPlayerMoved(false);
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
          onDisproveSuggestion={handleDisproveSuggestion}
          onEndTurn={handleEndTurn}
          moves={moves}
          location={location}
          gameState={gameState}
          character={character}
          playerId={playerId}
          localPlayer={localPlayer}
          revealOptions={revealOptions}
          disproveSuggestionState={disproveSuggestionState}
          socket={socket}
          messages={messages}
          inRoom={inRoom}
          playerMoved={playerMoved}
          actionMade={actionMade}
          cannotMove={cannotMove}
          movedBySuggestion={movedBySuggestion}
        />
      )}
      {screen === "end" && <EndScreen winner={winner} message={message} />}
    </div>
  );
}

export default App;

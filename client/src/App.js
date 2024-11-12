/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import io from "socket.io-client";
import "./App.css";

function App() {
  const [gameState, setGameState] = useState(null);
  const [optionTable, setOptionTable] = useState("");
  const [playerId, setPlayerId] = useState("");
  const [newPlayerName, setNewPlayerName] = useState("");
  const [message, setMessage] = useState("");
  const [playerCreated, setPlayerCreated] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState("");
  const [players, setPlayers] = useState([]);
  const [playerCards, setPlayerCards] = useState([]);
  const [turnStarted, setTurnStarted] = useState(false);
  const [destination, setDestination] = useState("");
  const [suggestion, setSuggestion] = useState({
    character: "",
    weapon: "",
    room: "",
  });
  const [accusation, setAccusation] = useState({
    character: "",
    weapon: "",
    room: "",
  });
  const [showMoveButtons, setShowMoveButtons] = useState(false);
  const availableCharacters = [
    "Colonel Mustard",
    "Professor Plum",
    "Mrs. Peacock",
    "Miss Scarlett",
    "Reverend Green",
    "Mrs. White",
  ];
  const [assignedCharacters, setAssignedCharacters] = useState([]);
  const [displayPlayerInfo, setDisplayPlayerInfo] = useState("");

  const socket = io("http://localhost:5000");

  const handleDetailedBoard = (data) => {
    console.log("Response data:", data);
    setGameState(data);
    socket.off("detailed_board_response", handleDetailedBoard);
  };

  useEffect(() => {
    if (playerCreated && gameStarted) {
      fetchGameState();
    }
    return () => {
      socket.off("detailed_board_response", handleDetailedBoard);
    };
  }, [playerCreated, gameStarted]);

  const fetchGameState = () => {
    socket.emit("detailed_board");

    const handleDetailedBoard = (data) => {
      console.log("Response data:", data);
      setGameState(data);
      socket.off("detailed_board_response", handleDetailedBoard);
    };

    socket.on("detailed_board_response", handleDetailedBoard);
  };

  const handleStartGame = () => {
    socket.emit("start_game");

    const handleStartGameResponse = (data) => {
      if (data.status === "success") {
        setMessage(data.message);
        setGameStarted(true);
        console.log("Game started:", data);
        fetchOptionTable();
        fetchPlayersAndCards();
      } else {
        console.error("Error starting the game:", data.message);
        setMessage("An error occurred: " + data.message);
      }
      socket.off("start_game_response", handleStartGameResponse);
    };

    socket.on("start_game_response", handleStartGameResponse);
  };

  const fetchOptionTable = () => {
    socket.emit("get_option_table");

    const handleOptionTableResponse = (data) => {
      if (data.error) {
        console.error("Error fetching option table:", data.error);
      } else {
        setOptionTable(data.optionTable);
        console.log("Option table fetched:", data);
      }
      socket.off("option_table_response", handleOptionTableResponse);
    };

    socket.on("option_table_response", handleOptionTableResponse);
  };

  const fetchPlayersAndCards = () => {
    socket.emit("get_players");

    const handleGetPlayersResponse = (data) => {
      if (data.error) {
        console.error("Error fetching players and cards:", data.error);
      } else {
        setPlayers(data.players);
        setPlayerCards(data.players.map((player) => player.cards));
        console.log("Players and cards fetched:", data);
      }
      socket.off("get_players_response", handleGetPlayersResponse);
    };

    socket.on("get_players_response", handleGetPlayersResponse);
  };

  const fetchCurrentPlayer = () => {
    socket.emit("get_current_player");

    const handleCurrentPlayerResponse = (data) => {
      if (data.error) {
        console.error("Error fetching current player:", data.error);
      } else {
        setDisplayPlayerInfo(data.current_player);
        console.log("Current player fetched:", data);
      }
      socket.off("get_current_player_response", handleCurrentPlayerResponse);
    };

    socket.on("get_current_player_response", handleCurrentPlayerResponse);
  };

  const handleTurn = (action) => {
    if (!playerId) {
      alert("Please enter a player ID");
      return;
    }

    socket.emit("player_turn", { action });

    const handleTurnResponse = (data) => {
      if (data.error) {
        console.error("Error:", data.error);
        setMessage("An error occurred: " + data.error);
      } else {
        setMessage(data.message);
        if (action === "start") {
          setTurnStarted(true);
          fetchCurrentPlayer();
        } else if (action === "end") {
          setTurnStarted(false);
        }
        setGameOver(data.gameOver);
      }
      socket.off("player_turn_response", handleTurnResponse);
    };

    socket.on("player_turn_response", handleTurnResponse);
  };

  const handleMovePlayer = () => {
    socket.emit("get_move_options");

    const handleMoveOptionsResponse = (data) => {
      if (data.error) {
        console.error("Error fetching move options:", data.error);
        setMessage("An error occurred: " + data.error);
      } else {
        const options = data.options.map((option) => option.direction);
        setMessage(
          `You are currently at ${
            data.currentLocation
          }. Available moves: ${options.join(", ")}`
        );
        setOptionTable(data.options);
        setShowMoveButtons(true); // Show movement buttons
      }
      socket.off("move_options_response", handleMoveOptionsResponse);
    };

    socket.on("move_options_response", handleMoveOptionsResponse);
  };

  const handleMove = (direction) => {
    socket.emit("move_player", { direction });

    const handleMoveResponse = (data) => {
      if (data.error) {
        console.error(`Error moving player ${direction}:`, data.error);
        setMessage("An error occurred: " + data.error);
      } else {
        setMessage(data.message);
        fetchGameState();
        setShowMoveButtons(false);
        setTimeout(() => {
          handleTurn("end");
        }, 3000);
      }
      socket.off("move_player_response", handleMoveResponse);
    };

    socket.on("move_player_response", handleMoveResponse);
  };

  const handleMakeSuggestion = () => {
    if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
      alert("Please complete all suggestion fields");
      return;
    }

    socket.emit("player_suggestion", { suggestion });

    const handleSuggestionResponse = (data) => {
      if (data.error) {
        console.error("Error making suggestion:", data.error);
        setMessage("An error occurred: " + data.error);
      } else {
        setMessage(data.message);
        setSuggestion({ character: "", weapon: "", room: "" });
        setTimeout(() => {
          handleTurn("end");
        }, 3000);
      }
      socket.off("player_suggestion_response", handleSuggestionResponse);
    };

    socket.on("player_suggestion_response", handleSuggestionResponse);
  };

  const handleMakeAccusation = () => {
    if (!accusation.character || !accusation.weapon || !accusation.room) {
      alert("Please complete all accusation fields");
      return;
    }

    socket.emit("player_accusation", { accusation });

    const handleAccusationResponse = (data) => {
      if (data.error) {
        console.error("Error making accusation:", data.error);
        setMessage("An error occurred: " + data.error);
      } else {
        setMessage(data.message);
        setGameOver(data.gameOver);
        setAccusation({ character: "", weapon: "", room: "" });
        setTimeout(() => {
          handleTurn("end");
        }, 3000);
      }
      socket.off("player_accusation_response", handleAccusationResponse);
    };

    socket.on("player_accusation_response", handleAccusationResponse);
  };

  const handleAddPlayer = () => {
    if (!newPlayerName) {
      alert("Please enter a player name");
      return;
    }

    const unassignedCharacters = availableCharacters.filter(
      (character) => !assignedCharacters.includes(character)
    );

    if (unassignedCharacters.length === 0) {
      alert("All characters have been assigned. No more players can be added.");
      return;
    }

    const randomCharacter =
      unassignedCharacters[
        Math.floor(Math.random() * unassignedCharacters.length)
      ];

    socket.emit("add_player", {
      playerName: newPlayerName,
      character: randomCharacter,
    });

    const handleAddPlayerResponse = (data) => {
      if (data.error) {
        console.error("Error:", data.error);
        if (data.error.includes("already exists")) {
          setMessage(
            `${newPlayerName} already exists. Continuing to the game.`
          );
          setPlayerCreated(true);
          setPlayerId(newPlayerName);
          setDisplayPlayerInfo(`${newPlayerName} = ${randomCharacter}`);
        } else {
          setMessage("An error occurred: " + data.error);
        }
      } else {
        setMessage(`${data.message}`);
        setNewPlayerName("");
        setPlayerCreated(true);
        setPlayerId(newPlayerName);
        setDisplayPlayerInfo(`${newPlayerName} = ${randomCharacter}`);
        setAssignedCharacters([...assignedCharacters, randomCharacter]);
      }
      socket.off("add_player_response", handleAddPlayerResponse);
    };

    socket.on("add_player_response", handleAddPlayerResponse);
  };

  return (
    // The start page to add a new player
    <div className="app">
      <h1>Clue Game</h1>
      {!playerCreated ? (
        <div className="player-controls">
          <h2>Create a New Player</h2>
          <input
            type="text"
            placeholder="Enter your name"
            value={newPlayerName}
            onChange={(e) => setNewPlayerName(e.target.value)}
            className="input"
          />
          <button onClick={handleAddPlayer} className="button start-button">
            Create Player
          </button>
        </div>
      ) : !gameOver ? (
        // The web page that cycles through the game logic
        <div className="main-container">
          <div className="left-panel">
            <div className="player-info">
              <h3>Current Player: </h3>
              <input
                type="text"
                value={displayPlayerInfo}
                readOnly
                className="input uneditable"
              />
              {message && (
                <div className="game-state">
                  <p>{message}</p>
                </div>
              )}
              {!gameStarted ? (
                <button
                  onClick={handleStartGame}
                  className="button start-button"
                >
                  Start Game
                </button>
              ) : (
                <div className="turn-controls">
                  {!showMoveButtons && (
                    <>
                      <button
                        onClick={() => handleTurn("start")}
                        className="button start-button"
                      >
                        Start Turn
                      </button>
                      {/* <button
                        onClick={() => handleTurn("end")}
                        className="button end-button"
                      >
                        End Turn
                      </button> */}
                    </>
                  )}
                  {turnStarted && (
                    <div>
                      {!showMoveButtons ? (
                        <div>
                          <button
                            onClick={handleMovePlayer}
                            className="button-blue"
                          >
                            Move Player
                          </button>
                        </div>
                      ) : (
                        <div>
                          <p>{message}</p>{" "}
                          {/* Show possible movement directions */}
                          <button
                            className="button-blue"
                            onClick={() => handleMove("left")}
                          >
                            Left
                          </button>
                          <button
                            className="button-blue"
                            onClick={() => handleMove("right")}
                          >
                            Right
                          </button>
                          <button
                            className="button-blue"
                            onClick={() => handleMove("up")}
                          >
                            Up
                          </button>
                          <button
                            className="button-blue"
                            onClick={() => handleMove("down")}
                          >
                            Down
                          </button>
                        </div>
                      )}
                      {!showMoveButtons && (
                        <>
                          <br />
                          <div>
                            <input
                              type="text"
                              placeholder="Character"
                              value={suggestion.character}
                              onChange={(e) =>
                                setSuggestion({
                                  ...suggestion,
                                  character: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <input
                              type="text"
                              placeholder="Weapon"
                              value={suggestion.weapon}
                              onChange={(e) =>
                                setSuggestion({
                                  ...suggestion,
                                  weapon: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <input
                              type="text"
                              placeholder="Room"
                              value={suggestion.room}
                              onChange={(e) =>
                                setSuggestion({
                                  ...suggestion,
                                  room: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <button
                              onClick={handleMakeSuggestion}
                              className="button-blue"
                            >
                              Make a Suggestion
                            </button>
                          </div>
                          <br />
                          <div className="accusation-controls">
                            <input
                              type="text"
                              placeholder="Character"
                              value={accusation.character}
                              onChange={(e) =>
                                setAccusation({
                                  ...accusation,
                                  character: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <input
                              type="text"
                              placeholder="Weapon"
                              value={accusation.weapon}
                              onChange={(e) =>
                                setAccusation({
                                  ...accusation,
                                  weapon: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <input
                              type="text"
                              placeholder="Room"
                              value={accusation.room}
                              onChange={(e) =>
                                setAccusation({
                                  ...accusation,
                                  room: e.target.value,
                                })
                              }
                              className="input input-small"
                            />
                            <button
                              onClick={handleMakeAccusation}
                              className="button-blue"
                            >
                              Make an Accusation
                            </button>
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
          {gameStarted && (
            <div className="right-panel">
              {/* Display the option table above the game board */}
              {optionTable}

              <h2>Game Board</h2>
              {gameState ? (
                <div className="board">
                  {gameState.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                      {row.map((cell, cellIndex) => (
                        <div key={cellIndex} className="board-cell">
                          <pre>{cell}</pre>
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              ) : (
                <p>Loading game state...</p>
              )}
              <div className="players-info">
                <h3>Players and Their Cards</h3>
                {players.length > 0 ? (
                  <ul className="player-list">
                    {players.map((player, index) => (
                      <li key={index} className="player-item">
                        <strong>{player.name}</strong>
                        {player.cards && player.cards.length > 0 ? (
                          <div className="cards-list">
                            {player.cards.map((card, cardIndex) => (
                              <span key={cardIndex} className="card-item">
                                {card.name}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span className="no-cards">No cards assigned</span>
                        )}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No players found</p>
                )}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="game-over">
          <h2>Game Over</h2>
          <h3>Player {displayPlayerInfo} wins!</h3>
          <p>Thank you for playing!</p>
          {/* <button onClick={() => window.location.reload()} className="button">
            Play Again
          </button> */}
        </div>
      )}
    </div>
  );
}

export default App;

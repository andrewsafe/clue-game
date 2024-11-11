import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [gameState, setGameState] = useState(null);
  const [optionTable, setOptionTable] = useState("");
  const [playerId, setPlayerId] = useState("");
  const [newPlayerName, setNewPlayerName] = useState("");
  const [message, setMessage] = useState("");
  const [playerCreated, setPlayerCreated] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
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

  axios.defaults.baseURL = "http://localhost:5000";

  useEffect(() => {
    if (playerCreated && gameStarted) {
      fetchGameState();
    }
  }, [playerCreated, gameStarted]);

  const fetchGameState = () => {
    axios
      .get("/detailed-board")
      .then((response) => {
        console.log("Response data:", response.data);
        setGameState(response.data);
      })
      .catch((error) => {
        console.error("Error fetching game state:", error);
      });
  };

  const handleStartGame = () => {
    axios
      .post("/start-game")
      .then((response) => {
        setMessage(response.data.message);
        setGameStarted(true);
        console.log("Game started:", response.data);
        //
        fetchOptionTable();
        // Fetch the players and their cards
        fetchPlayersAndCards();
      })
      .catch((error) => {
        console.error("Error starting the game:", error);
        setMessage(
          "An error occurred: " +
            (error.response?.data?.message || error.message)
        );
      });
  };

  const fetchOptionTable = () => {
    axios
      .get("/api/optionTable") // Make sure this endpoint returns the option table
      .then((response) => {
        setOptionTable(response.data.optionTable);
        console.log("Option table fetched:", response.data);
      })
      .catch((error) => {
        console.error("Error fetching players and cards:", error);
      });
  };

  const fetchPlayersAndCards = () => {
    axios
      .get("/api/players") // Make sure this endpoint returns players and their cards
      .then((response) => {
        setPlayers(response.data.players);
        setPlayerCards(response.data.cards);
        console.log("Players and cards fetched:", response.data);
      })
      .catch((error) => {
        console.error("Error fetching players and cards:", error);
      });
  };

  const handleTurn = (action) => {
    if (!playerId) {
      alert("Please enter a player ID");
      return;
    }

    axios
      .post("/api/players/turn", {
        action: action,
        playerId: playerId,
      })
      .then((response) => {
        setMessage(response.data.message);
        if (action === "start") {
          setTurnStarted(true);
        } else if (action === "end") {
          setTurnStarted(false);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setMessage(
          "An error occurred: " + (error.response?.data?.error || error.message)
        );
      });
  };

  const handleMovePlayer = () => {
    axios
      .post("/api/players/move", {
        playerId: playerId,
        destination: destination,
      })
      .then((response) => {
        const options = response.data.options.map((option) => option.direction);
        setMessage(
          `You are currently at ${
            response.data.currentLocation
          }. Available moves: ${options.join(", ")}`
        );
        setShowMoveButtons(true); // Show movement buttons
      })
      .catch((error) => {
        console.error("Error fetching move options:", error);
        setMessage(
          "An error occurred: " + (error.response?.data?.error || error.message)
        );
      });
  };

  const handleMove = (direction) => {
    axios
      .post("/api/players/move", {
        playerId: playerId,
        direction: direction,
      })
      .then((response) => {
        setMessage(response.data.message);
        fetchGameState();
        setShowMoveButtons(false); // Hide movement buttons after move
        setTimeout(() => {
          handleTurn("end");
        }, 3000);
      })
      .catch((error) => {
        console.error(`Error moving player ${direction}:`, error);
        setMessage(
          "An error occurred: " + (error.response?.data?.error || error.message)
        );
      });
  };

  const handleMakeSuggestion = () => {
    if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
      alert("Please complete all suggestion fields");
      return;
    }

    axios
      .post("/api/players/suggestion", {
        playerId: playerId,
        suggestion: suggestion,
      })
      .then((response) => {
        setMessage(response.data.message);
        setSuggestion({ character: "", weapon: "", room: "" });
        setTimeout(() => {
          handleTurn("end");
        }, 3000);
      })
      .catch((error) => {
        console.error("Error making suggestion:", error);
        setMessage(
          "An error occurred: " + (error.response?.data?.error || error.message)
        );
      });
  };

  const handleMakeAccusation = () => {
    if (!accusation.character || !accusation.weapon || !accusation.room) {
      alert("Please complete all accusation fields");
      return;
    }

    axios
      .post("/api/players/accusation", {
        playerId: playerId,
        accusation: accusation,
      })
      .then((response) => {
        setMessage(response.data.message);
        setAccusation({ character: "", weapon: "", room: "" });
        setTimeout(() => {
          handleTurn("end");
        }, 3000); // Adjust the delay as needed
      })
      .catch((error) => {
        console.error("Error making accusation:", error);
        setMessage(
          "An error occurred: " + (error.response?.data?.error || error.message)
        );
      });
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

    axios
      .post("/api/players/add", {
        playerName: newPlayerName,
        character: randomCharacter,
      })
      .then((response) => {
        setMessage(`${response.data.message}`);
        setNewPlayerName("");
        setPlayerCreated(true);
        setPlayerId(newPlayerName); // Keep only the player name here
        setDisplayPlayerInfo(`${newPlayerName} = ${randomCharacter}`); // Set combined info for display
        setAssignedCharacters([...assignedCharacters, randomCharacter]); // Track assigned characters
      })
      .catch((error) => {
        console.error("Error:", error);
        if (
          error.response &&
          error.response.data.error.includes("already exists")
        ) {
          setMessage(
            `${newPlayerName} already exists. Continuing to the game.`
          );
          setPlayerCreated(true);
          setPlayerId(newPlayerName);
          setDisplayPlayerInfo(`${newPlayerName} = ${randomCharacter}`);
        } else {
          setMessage(
            "An error occurred: " +
              (error.response?.data?.error || error.message)
          );
        }
      });
  };

  return (
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
      ) : (
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
      )}
    </div>
  );
}

export default App;

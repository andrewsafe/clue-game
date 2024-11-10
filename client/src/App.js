import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Ensure this file includes the CSS for layout and styling

function App() {
  const [gameState, setGameState] = useState(null);
  const [playerId, setPlayerId] = useState("");
  const [newPlayerName, setNewPlayerName] = useState("");
  const [message, setMessage] = useState("");
  const [playerCreated, setPlayerCreated] = useState(false);

  useEffect(() => {
    if (playerCreated) {
      axios
        .get("http://localhost:5000/detailed-board")
        .then((response) => {
          console.log("Response data:", response.data);
          setGameState(response.data);
        })
        .catch((error) => {
          console.error("Error fetching game state:", error);
        });
    }
  }, [playerCreated]);

  const handleTurn = (action) => {
    if (!playerId) {
      alert("Please enter a player ID");
      return;
    }

    axios
      .post("http://localhost:5000/api/players/turn", {
        action: action,
        playerId: playerId,
      })
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
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

    axios
      .post("http://localhost:5000/api/players/add", {
        playerName: newPlayerName,
      })
      .then((response) => {
        setMessage(response.data.message);
        setNewPlayerName("");
        setPlayerCreated(true);
        setPlayerId(newPlayerName);
      })
      .catch((error) => {
        console.error("Error:", error);
        if (
          error.response &&
          error.response.data.error.includes("already exists")
        ) {
          setMessage(
            `"${newPlayerName}" already exists. Continuing to the game.`
          );
          setPlayerCreated(true);
          setPlayerId(newPlayerName);
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
          <button onClick={handleAddPlayer} className="button">
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
                value={playerId}
                readOnly
                className="input uneditable"
              />
              {message && (
                <div className="game-state">
                  <p>{message}</p>
                </div>
              )}
              <div className="turn-controls">
                <button
                  onClick={() => handleTurn("start")}
                  className="button start-button"
                >
                  Start Turn
                </button>
                <button
                  onClick={() => handleTurn("end")}
                  className="button end-button"
                >
                  End Turn
                </button>
              </div>
            </div>
          </div>
          <div className="right-panel">
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
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Import the CSS file

function App() {
  const [gameState, setGameState] = useState({});
  const [move, setMove] = useState("");

  useEffect(() => {
    axios
      .get("http://localhost:5000/game")
      .then((response) => {
        setGameState(response.data);
      })
      .catch((error) => console.error("Error fetching game state:", error));
  }, []);

  const handleMove = () => {
    axios
      .post("http://localhost:5000/game", { move })
      .then((response) => {
        setGameState(response.data);
        setMove(""); // Clear input field after move
      })
      .catch((error) => console.error("Error making move:", error));
  };

  return (
    <div className="app">
      <h1>Clue Game</h1>
      <div>
        <h2>Game State</h2>
        <pre className="game-state">{JSON.stringify(gameState, null, 2)}</pre>
      </div>
      <div>
        <h3>Make a Move</h3>
        <input
          type="text"
          value={move}
          onChange={(e) => setMove(e.target.value)}
          placeholder="Enter your move"
          className="input"
        />
        <button onClick={handleMove} className="button">
          Submit Move
        </button>
      </div>
    </div>
  );
}

export default App;

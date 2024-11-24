import React, { useState } from "react";
import "./css/StartScreen.css";
import { StartScreenProps } from "./types";

const StartScreen: React.FC<StartScreenProps> = ({ onAddPlayer }) => {
  const [playerName, setPlayerName] = useState<string>("");

  //const [character, setCharacter] = useState("");
  //const [availableCharacters, setAvailableCharacters] = useState([]);

  const handleAddPlayer = () => {
    if (!playerName.trim()) {
      alert("Player name cannot be empty");
      return;
    }
    onAddPlayer({ playerName });
    setPlayerName("");
  };

  return (
    <div>
      <h1>Clue Game</h1>
      <input
        type="text"
        placeholder="Player Name"
        value={playerName}
        onChange={(e) => setPlayerName(e.target.value)}
      />
      <button onClick={handleAddPlayer}>Add Player</button>
    </div>
  );
};

export default StartScreen;

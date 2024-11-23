Simport React, { useState } from "react";
import "./css/StartScreen.css";

function StartScreen({ onAddPlayer }) {
    const [playerName, setPlayerName] = useState("");
    //const [character, setCharacter] = useState("");
    //const [availableCharacters, setAvailableCharacters] = useState([]);

    const handleAddPlayer = () => {
        onAddPlayer({ playerName });
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
}

export default StartScreen;

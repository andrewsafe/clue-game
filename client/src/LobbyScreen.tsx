import React from "react";
import "./css/LobbyScreen.css";

// Define the props type
type LobbyScreenProps = {
  players: { name: string; character: string }[]; // Array of players
  onStartGame: () => void; // Function to start the game
};

const LobbyScreen: React.FC<LobbyScreenProps> = ({ players, onStartGame }) => {
  return (
    <div>
      <h2>Waiting Room</h2>
      <ul>
        {players.map((player, index) => (
          <li key={index}>
            {player.name} as {player.character}
          </li>
        ))}
      </ul>
      <button onClick={onStartGame} disabled={players.length < 2}>
        Start Game
      </button>
    </div>
  );
};

export default LobbyScreen;

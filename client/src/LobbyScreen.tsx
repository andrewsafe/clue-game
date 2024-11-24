import React from "react";
import "./css/LobbyScreen.css";
import { LobbyScreenProps } from "./types";

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

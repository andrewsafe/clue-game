import React from "react";
import "./css/LobbyScreen.css";

function LobbyScreen({ players, onStartGame }) {
    return (
        <div>
            <h2>Waiting Room</h2>
            <ul>
                {players.map((player, index) => (
                    <li key={index}>{player.name} as {player.character}</li>
                ))}
            </ul>
            <button onClick={onStartGame}>
                Start Game
            </button>
        </div>
    );
}

export default LobbyScreen;
//disabled = { players.length < 2
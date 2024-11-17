import React, { useState } from "react";
import "./css/GameScreen.css";

function GameScreen({ currentPlayer, onMove, onSuggestion, onAccusation, message, moves, location, gameState, character, players, playerId }) {
    const [moveChoice, setMoveChoice] = useState("");
    const [suggestion, setSuggestion] = useState({ character: "", weapon: "", room: "" });
    const [accusation, setAccusation] = useState({ character: "", weapon: "", room: "" });

    const handleMove = () => {
        onMove(moveChoice);
    };

    const handleSuggestion = () => {
        if (!suggestion.character || !suggestion.weapon || !suggestion.room) {
            alert("Please complete all suggestion fields");
            return;
        }
        console.log("Suggestion:", suggestion);
        onSuggestion(suggestion);
    };

    const handleAccusation = () => {
        onAccusation(accusation);
    };

    return (
        <div className="game-screen">
            <h2>Current Player: {currentPlayer}</h2>
            <h3>Current Character: {character}</h3>
            <h3>Current Location: {location}</h3>
            {message && <p>{message}</p>}
            <h2>Game Board</h2>
            {gameState && gameState.length > 0 ? (
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
                <p>Loading game board...</p>
            )}
            <div>
                <h3>Make a Move</h3>
                <select onChange={(e) => setMoveChoice(e.target.value)} value={moveChoice}>
                    <option value="">Select Move</option>
                    {moves.map((move, index) => (
                        <option key={index} value={move}>
                            {move}
                        </option>
                    ))}
                </select>
                <button onClick={handleMove}>Move</button>
            </div>

            <div>
                <h3>Make a Suggestion</h3>
                <select onChange={(e) => setSuggestion(prev => ({ ...prev, character: e.target.value }))}>
                    <option value="">Select Suspect</option>
                    <option value="1">Colonel Mustard</option>
                    <option value="2">Professor Plum</option>
                    <option value="3">Reverend Green</option>
                    <option value="4">Mrs. Peacock</option>
                    <option value="5">Miss Scarlett</option>
                    <option value="6">Mrs. White</option>
                </select>
                <select onChange={(e) => setSuggestion(prev => ({ ...prev, weapon: e.target.value }))}>
                    <option value="">Select Weapon</option>
                    <option value="1">Dagger</option>
                    <option value="2">Candlestick</option>
                    <option value="3">Revolver</option>
                    <option value="4">Rope</option>
                    <option value="5">Lead Pipe</option>
                    <option value="6">Wrench</option>
                </select>
                <select onChange={(e) => setSuggestion(prev => ({ ...prev, room: e.target.value }))}>
                    <option value="">Select Room</option>    
                    <option value="1">Hall</option>
                    <option value="2">Lounge</option>
                    <option value="3">Library</option>
                    <option value="4">Kitchen</option>
                    <option value="5">Billiard Room</option>
                    <option value="6">Study</option>
                    <option value="7">Ballroom</option>
                    <option value="8">Dining Room</option>
                    <option value="9">Conservatory</option>
                </select>
                <button onClick={handleSuggestion}>Suggest</button>
            </div>

            <div>
                <h3>Make an Accusation</h3>
                <select onChange={(e) => setAccusation(prev => ({ ...prev, character: e.target.value }))}>
                    <option value="">Select Suspect</option>
                    <option value="1">Colonel Mustard</option>
                    <option value="2">Professor Plum</option>
                    <option value="3">Reverend Green</option>
                    <option value="4">Mrs. Peacock</option>
                    <option value="5">Miss Scarlett</option>
                    <option value="6">Mrs. White</option>
                </select>
                <select onChange={(e) => setAccusation(prev => ({ ...prev, weapon: e.target.value }))}>
                    <option value="">Select Weapon</option>
                    <option value="1">Dagger</option>
                    <option value="2">Candlestick</option>
                    <option value="3">Revolver</option>
                    <option value="4">Rope</option>
                    <option value="5">Lead Pipe</option>
                    <option value="6">Wrench</option>
                </select>
                <select onChange={(e) => setAccusation(prev => ({ ...prev, room: e.target.value }))}>
                    <option value="">Select Room</option>
                    <option value="1">Hall</option>
                    <option value="2">Lounge</option>
                    <option value="3">Library</option>
                    <option value="4">Kitchen</option>
                    <option value="5">Billiard Room</option>
                    <option value="6">Study</option>
                    <option value="7">Ballroom</option>
                    <option value="8">Dining Room</option>
                    <option value="9">Conservatory</option>
                </select>
                <button onClick={handleAccusation}>Accuse</button>
            </div>
            <div className="players-info">
                <h3>Players and Their Cards</h3>
                {players.length > 0 ? (
                    <ul className="player-list">
                        {players.filter((player) => player.id === playerId).map((player, index) => (
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
    );
}

export default GameScreen;

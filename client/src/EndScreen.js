import React from "react";
import "./css/EndScreen.css";

function EndScreen({ winner, message }) {
  return (
    <div>
      <h1>Game Over</h1>
      <h2>Winner: {winner}</h2>
      <h2>{message}</h2>
    </div>
  );
}

export default EndScreen;

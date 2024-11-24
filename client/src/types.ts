export type SuggestionOrAccusation = {
  character: string;
  weapon: string;
  room: string;
};

export type Player = {
  name: string;
  character: string;
  cards?: { name: string }[];
  id: string;
};

export type PlayerAddedData = {
  player_id: string;
  message: string;
  error?: string;
};

export type ReturnPlayersData = {
  players: Player[];
};

export type GameStartedData = {
  current_player: string;
  character: string;
  message: string;
};

export type BoardResponseData = string[][];

export type NextTurnData = {
  current_player: string;
  character: string;
};

export type MoveOptionsData = {
  moves: string[];
  currentLocation: string;
};

export type GenericMessageData = {
  message: string;
};

export type GameOverData = {
  winner: string;
  message: string;
};

export type EndScreenProps = {
  winner: string;
  message: string;
};

export type StartScreenProps = {
  onAddPlayer: (player: { playerName: string }) => void;
};

export type GameScreenProps = {
  currentPlayer: string;
  onMove: (moveChoice: string) => void;
  onSuggestion: (suggestion: SuggestionOrAccusation) => void;
  onAccusation: (accusation: SuggestionOrAccusation) => void;
  message: string;
  moves: string[];
  location: string;
  gameState: string[][]; // Assuming each cell is a string ........ check this
  character: string;
  players: Player[];
  playerId: string;
};

export type LobbyScreenProps = {
  players: { name: string; character: string }[];
  onStartGame: () => void;
};

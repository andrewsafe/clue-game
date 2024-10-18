from game_system.game_system import GameSystem
from game_system.turn_manager import TurnManager

def main():
    # Create a GameSystem instance
    game = GameSystem()

    # Add players to the game
    game.add_player("Andrew")
    game.add_player("Justin")
    game.add_player("Elliot")

    # Start the game
    game.start_game()

    # Create a TurnManager instance
    turn_manager = TurnManager(game.players)

    # Simulate a few turns
    for _ in range(len(game.players)):
        current_player = turn_manager.current_player()
        print(f"It's {current_player.name}'s turn.")
        # Simulate some action (like making a suggestion or moving)
        # For now, we'll just print the cards they have
        print(f"{current_player.name}'s cards: {current_player.show_cards()}")

        # Advance to the next player's turn
        turn_manager.next_turn()

    # Reset turns and show the current player again
    turn_manager.reset_turns()
    print(turn_manager)  # Output: Current turn: Alice

if __name__ == "__main__":
    main()

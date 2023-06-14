import pygame
import GameStates, ResourceManager


class AppleGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Apple Game (It wis already finished and not a work in progress)")

    def start_game(self):
        game = GameStates.GameController(ResourceManager.ORIGINAL_CAPTION)
        pygame.display.set_icon(ResourceManager.GFX["UI"]["Smiley"])
        state_dictionary = {
            "Title": GameStates.MainMenu(),
            "Game": GameStates.Game(),
            "Paused": GameStates.Paused(),
            "Winscreen": GameStates.Winscreen()
        }
        game.state_machine.setup_states(state_dictionary, "Title")
        game.main()

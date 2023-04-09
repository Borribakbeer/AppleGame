import pygame
from . import GameStates, ResourceManager


class AppleGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Apple Game (It wis already finished and not a work in progress)")

    def start_game(self):
        game = GameStates.GameController(ResourceManager.ORIGINAL_CAPTION)
        state_dictionary = {
            "Title": GameStates.MainMenu(),
            "Game": GameStates.Game()
        }
        game.state_machine.setup_states(state_dictionary, "Title")
        game.main()





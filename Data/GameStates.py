import pygame as pg
import random
import Utils.ParentComponents
from Utils import state_machine, Tools, ParentComponents
from StateBuilders import MainMenuBuilder, GameBuilder, PausedBuilder, WinscreenBuilder
from Stats import AppleStats
from ResourceManager import *
import ResourceManager
from Components import camera, UIDrawer, SoundPlayer
import json

TIME_PER_UPDATE = 16.0  # Milliseconds


class GameController(object):
    # The class that controls the game states

    def __init__(self, caption):
        pg.display.set_mode(SCREEN_SIZE)
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.fps_visible = True
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

        self.musicqueue = list(MUSIC_PATHS)
        randomIndex = random.randint(0, len(self.musicqueue) - 1)
        pg.mixer.music.load(open(os.path.join("Resources", "Sounds", "Music", self.musicqueue[randomIndex]) +".ogg"),)
        pg.mixer.music.play()
        del self.musicqueue[randomIndex]
        pg.mixer.music.set_endevent(ENDING_MUSIC)
        if ResourceManager.MUTED_MUSIC:
            pg.mixer.music.pause()

    def update(self, dt):
        # Updates the currently active state.
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now, dt)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.screen.fill((100, 0, 255))
            self.state_machine.draw(self.screen, interpolate)
            pg.display.update()
            self.show_fps()

    def event_loop(self):
        # Process events

        for event in pg.event.get():
            self.state_machine.get_event(event)
            
            game = self.state_machine.state_dict["Game"]
            if event.type == pg.QUIT:
                self.done = True
            # Input
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                if self.keys[pg.K_m]:
                    if ResourceManager.MUTED_MUSIC:
                        ResourceManager.MUTED_MUSIC = False
                        pg.mixer.music.unpause()
                    else:
                        ResourceManager.MUTED_MUSIC = True
                        pg.mixer.music.pause()

            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            # Reset game
            elif event.type == RESET_GAME:
                game = self.state_machine.state_dict["Game"]
                saveRead = open("AppleGame.save", "r")
                save = json.load(saveRead)
                saveRead.close()

                if save["Score"][0] > game.score[0]:
                    f = open("AppleGame.save", "w")
                    f.write('{ "Score":' + str(game.score) + '}')
                    f.close()
                self.state_machine.state_dict["Game"] = Game(self.now)
                game.done = True

            if event.type == ENDING_MUSIC:
                self.QueueMusic()


    def QueueMusic(self):
        if len(self.musicqueue) <= 0:
            self.musicqueue = list(MUSIC_PATHS)

        randomIndex = random.randint(0, len(self.musicqueue) - 1)
        pg.mixer.music.load(os.path.join("Resources", "Sounds", "Music", self.musicqueue[randomIndex] + ".ogg"))
        pg.mixer.music.play()
        del self.musicqueue[randomIndex]

    def toggle_show_fps(self, key):
        # Press f5 to turn on/off displaying the framerate in the caption.
        if key == pg.K_F5:
            self.fps_visible = not self.fps_visible
            if not self.fps_visible:
                pg.display.set_caption(self.caption)

    def show_fps(self):
        # Display the current FPS in the window caption if fps_visible is True.

        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

    def main(self):
        # Main loop for entire program. Uses a constant timestep (TIME_PER_UPDATE).
        lag = 0.0
        while not self.done:
            dt = self.clock.tick(self.fps)
            lag += dt
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update(dt)
                lag -= TIME_PER_UPDATE
            self.draw(lag / TIME_PER_UPDATE)
        



class MainMenu(state_machine.State):
    def __init__(self):
        state_machine.State.__init__(self)
        self.elements = self.make_elements()

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

    def make_elements(self):
        group = pg.sprite.LayeredUpdates()
        group.add(MainMenuBuilder.TitleImage(), MainMenuBuilder.AnyKey(), MainMenuBuilder.AppleGlow(), MainMenuBuilder.Apple(), MainMenuBuilder.Player(), layer=1)
        return group

    def update(self, keys, now, dt):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)

    def draw(self, surface, interpolate):
        self.elements.draw(surface)

    def get_event(self, event):
        """
        Get events from Control.  Currently changes to next state on any key
        press.
        """
        if event.type == pg.KEYDOWN:
            self.next = "Game"
            self.done = True


class Game(state_machine.State):
    def __init__(self, now):
        state_machine.State.__init__(self)
        self.camera = camera.Camera()
        self.uibuilder = UIDrawer.UIDrawer()
        self.soundplayer = SoundPlayer.SoundPlayer(self)
        self.elements = GameBuilder.make_elements(self.camera)
        self.colliders = []
        for collider in self.elements.get_objects():
            if("Collider" in collider.tags):
                self.colliders.append(collider)

        self.keys = []

        self.maxapples = len(AppleStats.apples)
        self.applecount = self.maxapples
        self.runstarttime = now
        
        self.score = [0, 0]



    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

    def update(self, keys, now, dt):
        self.now = now
        self.elements.update(now, keys, self, dt)

    def draw(self, surface, interpolate):
        self.camera.draw_frame(surface, self.elements)
        self.uibuilder.draw(surface, self)

    def get_event(self, event):
        self.elements.get_event(event)
        if event.type == pg.KEYDOWN:
            self.keys = pg.key.get_pressed()
            self.elements.get_keys(self.keys)

            if(self.keys[pg.K_ESCAPE]):
                self.next = "Paused"
                self.done = True
                
            if(self.keys[pg.K_r]):
                pg.event.post(pg.event.Event(RESET_GAME))
                self.next = "Game"
                self.done = True

        elif event.type == pg.KEYUP:
            self.keys = pg.key.get_pressed()
            self.elements.get_keys(self.keys)
        self.camera.get_event(event)            


class Paused(state_machine.State):
    def __init__(self):
        state_machine.State.__init__(self)
        self.elements = self.make_elements()

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

    def make_elements(self):
        group = pg.sprite.LayeredUpdates()
        group.add(PausedBuilder.PressSpace(), PausedBuilder.PausedText(), layer=1)
        return group

    def update(self, keys, now, dt):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)

    def draw(self, surface, interpolate):
        surface.fill((100, 50, 50))
        self.elements.draw(surface)

    def get_event(self, event):
        """
        Get events from Control.  Currently changes to next state on any key
        press.
        """
        if event.type == pg.KEYDOWN:
            self.next = "Game"
            self.done = True


class Winscreen(state_machine.State):
    def __init__(self):
        state_machine.State.__init__(self)
        self.elements = self.make_elements()

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

    def make_elements(self):
        group = pg.sprite.LayeredUpdates()
        group.add(WinscreenBuilder.RestartButton(), layer=1)
        group.add(WinscreenBuilder.WinText(), layer=2)
        return group

    def update(self, keys, now, dt):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)

    def draw(self, surface, interpolate):
        surface.fill((50, 100, 200))
        self.elements.draw(surface)

    def get_event(self, event):
        for sprite in self.elements.get_sprites_from_layer(1):
            sprite.get_event(event)

        if event.type == RESET_GAME:
            self.next = "Game"
            self.done = True
        pass
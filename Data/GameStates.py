import pygame as pg
from .Utils import state_machine
from .Utils import Tools
from .StateBuilders import MainMenuBuilder
from . import ResourceManager
from .Components import player, camera

TIME_PER_UPDATE = 16.0  # Milliseconds


class GameController(object):
    # The class that controls the game states

    def __init__(self, caption):
        pg.display.set_mode(ResourceManager.SCREEN_SIZE)
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.fps_visible = True
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

    def update(self):
        # Updates the currently active state.
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.screen.fill((100, 0, 255))
            self.state_machine.draw(self.screen, interpolate)
            pg.display.update()
            self.show_fps()

    def event_loop(self):
        """
        Process all events and pass them down to the state_machine.
        The f5 key globally turns on/off the display of FPS in the caption
        """

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state_machine.get_event(event)

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
        # Main loop for entire program. Uses a constant timestep.
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
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
        group.add(MainMenuBuilder.AnyKey(), MainMenuBuilder.TitleImage(), layer=1)
        return group

    def update(self, keys, now):
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
    def __init__(self):
        state_machine.State.__init__(self)
        self.elements = self.make_elements()
        self.camera = camera.Camera()
        self.keys = []

    def startup(self, now, persistant):
        self.persist = persistant
        self.start_time = now

    def make_elements(self):
        group = Tools.GameObjectsCollection()
        group.add(player.Player((0, 0)))
        return group

    def update(self, keys, now):
        """Updates the title screen."""
        self.now = now
        self.elements.update(now)

    def draw(self, surface, interpolate):
        self.camera.draw_frame(surface, self.elements)
        # self.elements.draw(surface)

    def get_event(self, event):
        self.elements.get_event(event)
        if event.type == pg.KEYDOWN:
            self.keys = pg.key.get_pressed()
            self.elements.get_keys(self.keys)
        elif event.type == pg.KEYUP:
            self.keys = pg.key.get_pressed()
            self.elements.get_keys(self.keys)




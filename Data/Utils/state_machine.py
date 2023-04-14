# A Base Statemachine where all statemachines can derive from

class StateMachine(object):

    def __init__(self):
        # if the statemachine has finished processing
        self.done = False
        # dictionary <string, state>
        self.state_dict = {}
        # name of the current state
        self.state_name = None
        # current state
        self.state = None
        # current time
        self.now = None

    def setup_states(self, state_dict, start_state):
        # Set up the dictionary and start state

        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, keys, now, dt):
        """
            Checks if a state is done or has called for a game quit.
            State is flipped if necessary and State.update is called.
        """

        self.now = now
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(keys, now, dt)

    def flip_state(self):
        """
        When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed.
        """
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.now, persist)
        self.state.previous = previous

    def get_event(self, event):
        """
        Pass events down to current State.
        """
        self.state.get_event(event)

    def draw(self, surface, interpolate):
        self.state.draw(surface, interpolate)


class State(object):
    def __init__(self):
        # start time
        self.start_time = 0.0
        # current time
        self.now = 0.0
        # if the state has finished
        self.done = False
        # if the state should stop
        self.quit = False
        # the next state to transfer to
        self.next = None
        # the previous state that came before
        self.previous = None
        # list of persistant variables between states
        self.persist = {}

    def get_event(self, event):
        """
        Process the events from the main event loop.
        This is where we transfer to other states
        """
        pass

    def startup(self, now, persistant):
        """
        Save persistant variables and
        set the start time of the State to the current time.
        """
        self.persist = persistant
        self.start_time = now

    def cleanup(self):
        """
        Add variables that should persist between states to the self.persist dictionary.
        Then reset State.done to False.
        """
        self.done = False
        return self.persist

    def update(self, keys, now, dt):
        """Update function for state.  Must be overloaded in children."""
        pass

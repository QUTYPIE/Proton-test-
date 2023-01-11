from abc import ABCMeta, abstractmethod, abstractproperty


class CliGame(object):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.config = config
        self.winner = None
        self.num_players = 0
        self._messages = []  # accumulates messages to print to console

    def queue_message(self, value):
        if value:  # ignore Nones
            self._messages.append(value)

    @property
    def messages(self):
        return self._messages

    @abstractproperty
    def screen_min_rows(self):pass

    @abstractproperty
    def screen_min_columns(self):pass

    @abstractproperty
    def banner(self):pass

    @abstractproperty
    def const_strings(self):pass

    @abstractproperty
    def name(self):pass

    @abstractmethod
    def next_turn(self):pass

    @abstractmethod
    def get_state_drawing(self):
        """ Returns a string that represents the internal state.
            Could be printed directly by the launcher"""
        pass


    @abstractmethod
    def reset(self):
        """ reset to initial state, conserves config"""
        pass
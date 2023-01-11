import sys
import signal
import subprocess
import time
from random import randint, sample
from games_exceptions import ErrorGettingConsoleDimensions
from games_exceptions import ConsoleDimenisionsTooSmall


class Launcher(object):
    """ Handles :
    1- the lifecycle of a CliGame
    2- handles all printing, prints game's splash screen, state and messages from game
    3- catches keyboard interrupts to exit game
    4- loops for player turns
    input is delegated to game via next_turn() method
    """
    max_popup_messages = 3

    def __init__(self, game):
        """
        Launches the game: initialize Launcher, print banner, prompt to start
        :param game: CliGame object
        """
        try:
            console_rows, console_columns = Launcher.get_console_dimensions()
            if console_columns < game.screen_min_columns or console_rows < game.screen_min_rows:
                raise ConsoleDimenisionsTooSmall("For '{}', min {}x{}".
                      format(game.name, game.screen_min_rows, game.screen_min_columns))
        except ErrorGettingConsoleDimensions:
            # not critical, we can live with it
            print ("Couldn't verify console dimensions, recommended min {}x{}".
                format(game.screen_min_rows,game.screen_min_columns))

        self.exit = False
        self.set_exit_handler()
        self.game = game
        if not self.game.dump:  # dont interrupt if dump mode is on
            self.print_banner()
            #  wait for user input to start the Game
            raw_input(self.game.const_strings.START_GAME)

    @staticmethod
    def clean_screen():
        print 100 * "\n"

    @staticmethod
    def get_console_dimensions():
        try:
            output = subprocess.check_output(["stty","size"])
            rows, columns = output.split()
            return int(rows), int(columns)
        except (OSError,ValueError) as ex:
            raise ErrorGettingConsoleDimensions(ex.message)

    def print_banner(self):
        for x in xrange(3):
            time.sleep(0.5)
            self.clean_screen()
            time.sleep(0.5)
            print self.game.banner

    def loop(self):
        self.clean_screen()
        while not self.exit and not self.game.winner:
            print "\n" + self.game.get_state_drawing()
            self.print_pending_messages()
            self.game.next_turn()
            self.clean_screen()
        print "\n" + self.game.get_state_drawing()
        self.print_popup([self.game.winner])
        if not self.game.dump:
            if self.play_again() :
                self.game.reset()
                self.loop()

    def play_again(self):
        user_input = raw_input(self.game.const_strings.PLAY_AGAIN)
        if user_input.lower() == "n":
            return False
        return True

    def print_pending_messages(self):
        """ Check if game wants to display messages"""
        if self.game.messages:
            if len(self.game.messages) > self.max_popup_messages:
                # limit popup messages
                self.print_popup(sample(self.game.messages, self.max_popup_messages))
            else:
                self.print_popup(self.game.messages)

            del self.game.messages[:]

    @staticmethod
    def print_popup(messages, left=None):
        """
        Formats messages into popup message then prints it
        :param messages: list of strings
        :param left: optional, determine which side is the popup
        >>> Launcher.print_popup(["msg1","msg1","msg2"], left=True)
        ,------.
        | msg1  |
        | msg2  |
        |/------
        <BLANKLINE>

        >>> Launcher.print_popup(["msg1","msg1","msg2"], left=False)
        ,------.
        | msg1  |
        | msg2  |
         ------\|
        <BLANKLINE>

        """

        max_popup_length = len(max(messages, key=len)) + 2
        top_boarder = "," + ("-" * max_popup_length) + "."
        if not left:  # if not specified, alter left and right popups
            left = randint(0, 1)
        if left:
            bottom_boarder = "|/" + ("-" * max_popup_length)
        else:
            bottom_boarder = " " + ("-" * max_popup_length) + "\|"

        popup = top_boarder + "\n"

        for msg in set(messages):
            popup += ("| " + msg + (" " * (max_popup_length - len(msg))) + "|") + "\n"
        popup += bottom_boarder + "\n"
        print popup

    def set_exit_handler(self):
        """ catch ctrl-c to exit cli game"""
        signal.signal(signal.SIGINT, self.catch_ctrl_c)

    def catch_ctrl_c(self, *args):
        print 2 * "\n" + self.game.const_strings.EXIT
        self.exit = True
        sys.exit(0)


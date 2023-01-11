import signal
import time
from copy import deepcopy
from random import randint
from constants import English, Spanish, TerrainTypes
from games.cli_game import CliGame
from camels_race_exceptions import ErrorInConfig, InputTimedOut
from camel import CamelTypes
from utils import get_current_time_in_ms, json_load, pickle_list_to_file
from collections import namedtuple, OrderedDict
from operator import itemgetter

languages = {"english": English, "spanish": Spanish}
input_result = namedtuple("input_result", "turbo weapon steps")


class CamelRace(CliGame):
    # loads strings from the game's module to support basic internationalization
    name = "Camel Race"
    const_strings = languages["english"]

    # Drawing related class variables
    splash_screen = """
        @@@@#;',    @@@@
      @@@@@@@@@     @@@@@
      @@@@@@@.     @@@@@@
         @@@@`   .@@@@@@@@
         @@@@   @@@@@@@@@@@@
         @@@@  @@@@@@@@@@@@@.
         +@@@@@@@@@@@@@@@@@@@
          @@@@@@@@@@@@@@@@@@@
          `@@@@@@@@@@@@@@@@@#
            @@@@@@@@@@@@@@@@
              @@@@@@@@@@+@@@
             @@@@@@@@,   ,@@
            @@@  @@       ;@#
            @@   '@'       @@
            @+    @@       ,@:
            @@    @@       +@
            '@    @@       @@
             @@   @@       @@
             +    @'       @
                  @`      @@
    """
    screen_min_rows = 24
    screen_min_columns = 80
    finish_line = ("|F|", "|I|", "|N|")
    start_lines = (("C|", "P|", "U|"), ("Y|", "O|", "U|"))
    finish_line_width = len(finish_line[0])
    start_lines_width = len(start_lines[0][0])
    camel_width = 9
    side_lane = None
    winner_camel_position = screen_min_columns - finish_line_width - start_lines_width - camel_width
    lane_separator = "-" * screen_min_columns + "\n"
    visible_lane = screen_min_columns - finish_line_width - start_lines_width - camel_width

    banner = "\n" * 100
    banner += splash_screen
    banner += "\n          " + const_strings.WELCOME + "\n"

    def __init__(self, config, dump=False):
        """ create camels from config using factory
        if dump is True, saves a copy of state after each round
        """
        super(CamelRace, self).__init__(config)
        self.dump = dump
        self.states_to_dump = []  # useful for blackbox testing and debugging
        self.results_to_dump = [] # useful for blackbox testing and debugging
        self.T = self.config.T
        self.Tp = self.config.Tp
        self.X = self.config.X
        self.language = self.config.language
        self.terrain = self.config.terrain

        self.camels = self.config.camels  # ordered dict: camel name to camel object
        self.lane_2_camel = self.config.lane_2_camel  # direct mapping of lane to camel name
        self.results = {}  # holds input result per camel_name

        self.const_strings = languages[self.language]
        self.num_players = len(self.camels)
        self.user_io = InputProcessor(self.Tp, self.X)

        signal.signal(signal.SIGALRM, self.alarmHandler)

    def reset(self):
        for camel in self.camels.values():
            camel.reset()
        del self.messages[:]
        self.winner = None

    def get_state_drawing(self):
        """ draws race field, terrain and camels, only uses camels{}
        :return: screen: string that reflects race state
        """
        if not self.side_lane:  # change drawing according to terrain
            self.side_lane = TerrainTypes.icon[self.terrain] * self.screen_min_columns + "\n"
        screen = self.side_lane
        camels = self.camels.values()
        for camel_name, camel in self.camels.items():
            start_line_type = (1,0)[camel.player == "cpu"]
            for row in (0,1,2):  # draw row by row
                screen += (self.start_lines[start_line_type][row] +
                           " " * camel.position +  # leading space
                           camel.icon[row] +  # part of camel in this row
                           " " * (self.visible_lane - camel.position)   # space till finish line
                           + self.finish_line[row] + "\n")  # finish line
            # print line separator after each lane, except last one
            if camels.index(camel) != self.num_players-1:
                screen += self.lane_separator
        screen += self.side_lane
        return screen

    def alarmHandler(self, *args):
        raise InputTimedOut

    def next_turn(self):
        """ main logic driver of the race
        for each camel, gets input from player or cpu
            gets isolated result and get dequeue messages to display
        finally updates overall state by composing results from all camels
        """
        for camel in self.camels.values():
            if camel.player.lower() != "cpu":
                requested_input = self.user_io.get_challenge()  # get 3 letters string
                signal.alarm(self.T / 1000)
                start_time = get_current_time_in_ms()
                try:
                    user_input = raw_input(
                        "{}, {} [ {} ]:".format(
                        camel.player, CamelRace.const_strings.INPUT_TURN, requested_input))

                except InputTimedOut:
                    user_input = ''
                else:
                    signal.alarm(0)
                finish_time = get_current_time_in_ms()

                time_taken = finish_time - start_time
                result = self.user_io.process_input(requested_input, user_input, time_taken)

                #  comment following line to return to user after entering
                #  (no need to wait until T), it makes better game play experience IMHO
                time.sleep(abs(self.T - time_taken) / 1000) # only real players are paused
            else:
                result = self.user_io.get_random_result()
                if self.dump:
                    self.results_to_dump.append(deepcopy(result))

            self.queue_message(Commenter.get_comment(camel.name, result, self.const_strings))
            self.results[camel.name] = result

        # update positions after each round (for all camels)
        self.update_camels_positions()
        self.check_for_winner()
        if self.dump:
            self.dump_game_state()

    def dump_game_state(self):
        """ saves a copy of self.camels at the end of each round
        when we have a winner, saves the list to a json file"""
        self.states_to_dump.append(deepcopy(self.camels))
        if self.winner:  # save once game finished
            pickle_list_to_file("state.pkl",self.states_to_dump)
            pickle_list_to_file("results.pkl", self.results_to_dump)

    def update_camels_positions(self):
        """ updates camels positions taking into account camel's results
        and interaction with other camels"""

        # update chasers and forward lists of each camel
        self.calculate_relative_positions()

        # update received attacks of each camel
        for camel in self.camels.values():
            if self.results[camel.name].weapon:
                camel.use_weapon(self.camels)

        # Accumulate everything:
        #         new position = old position +
        #                        steps as result from input +
        #                        turbo_boost_effect +
        #                        attacks effect +
        #                        Strenght_reduction

        # I consider speed reduction = steps reduction
        for camel in self.camels.values():
            turbo_effect = 0  # positive percent
            attacks_effect = camel.absorb_attacks()  # negative percent and/or absolute value
            steps_from_input = self.results[camel.name].steps  # positive absolute value

            if self.results[camel.name].turbo:
                turbo_effect = camel.get_turbo_boost(self.terrain)
            final_percent = turbo_effect + camel.strength - attacks_effect["percent"]
            final_steps = steps_from_input - attacks_effect["absolute"]
            camel.position += int(final_steps * ((100 + final_percent) / 100.0))

    def calculate_relative_positions(self):
        """calculates relative positions and update camel.forward_camels
         and camel.chaser_camels for each camel in self.camels{}

        camels at the same position dont count as chaser nor forward
        'not the most pythonic method but it is late at night!'
        """

        # construct 2d array of position differences
        # each line represents differences between positions of other camels
        positions_differences = []
        for lane in xrange(self.num_players):
            positions_differences.append([])
            for other_camel in self.camels.values():
                positions_differences[lane].append(
                    self.lane_2_camel[lane].position - other_camel.position)

        lane = 0
        for diffs in positions_differences:
            # we need nearest to zero differences
            # get list of (camel index, relative diff to camel at that index)
            negative_diffs = [(i,diff) for i, diff in enumerate(diffs) if diff < 0]
            positive_diffs = [(i,diff) for i, diff in enumerate(diffs) if diff > 0]

            del self.lane_2_camel[lane].forward_camels[:]
            if negative_diffs:
                # get indexes with max negative value to find forward camels
                max_neg_diff = max(negative_diffs, key=itemgetter(1))[1]
                self.lane_2_camel[lane].forward_camels.extend(
                    [self.lane_2_camel[i].name for i,diff in negative_diffs if diff == max_neg_diff])

            del self.lane_2_camel[lane].chaser_camels[:]
            if positive_diffs:
                # get indexes with min positive value to find chaser camels
                min_pos_diff = min(positive_diffs, key=itemgetter(1))[1]
                self.lane_2_camel[lane].chaser_camels.extend(
                    [self.lane_2_camel[i].name for i,diff in positive_diffs if diff == min_pos_diff])
            lane +=1

    def check_for_winner(self):
        """ check if any camel reached finish line
        also checkes if tie has occurred
        modifies self.winner"""
        winners = []
        for camel in self.camels.values():
            if camel.position == self.winner_camel_position:
                winners.append(camel.name)

        if len(winners) > 1:
            self.winner = self.const_strings.TIE
        elif len(winners) == 1:
            self.winner = self.const_strings.WINNER.format(winners[0])


class InputProcessor(object):
    """ processes user input according to game rules, also simulates cpu players"""

    # use ascii codes to avoid different locales problems
    inputs = [chr(ascii_letter) for ascii_letter in xrange(65, 91)]
    inputs.extend(["I","U"]) # some extra turbo

    def __init__(self, Tp, X):
        self.Tp = Tp
        self.X = X

    @staticmethod
    def get_challenge():
        requested_input = ""
        for _ in (1, 2, 3):
            requested_input += InputProcessor.inputs[
                randint(0, len(InputProcessor.inputs)-1)]
        return requested_input

    def process_input(self, requested_input, user_input, time_taken):
        """ get the result of the input without taking into account other camels
        :param requested_input: string of three letters
        :param user_input: string of whatever user input
        :param time_taken: time consumed by player to enter
        :return: result:  namedtuple("input_result", "turbo weapon steps")
        """
        """ """
        user_input = user_input.upper()

        turbo = self.check_turbo(requested_input)
        weapon = False
        steps = 0

        if len(user_input) in (3, 6) and user_input[0:3] == requested_input:
            if time_taken <= self.Tp / 2:
                steps = self.X
            elif time_taken <= self.Tp:
                steps = self.X / 2

            # check if player stroked both input and reversed input within time T'
            if len(user_input) == 6 and steps != 0:
                if (user_input[0] == user_input[5] and
                            user_input[1] == user_input[4] and
                            user_input[2] == user_input[3]):
                    weapon = True

        return input_result(turbo=turbo, weapon=weapon, steps=steps)

    def get_random_result(self):
        """ get results when player is cpu,
        returns normalized random values to simulate humans
        :return: namedtuple("input_result", "turbo weapon steps")"""
        turbo = self.check_turbo(self.get_challenge())

        if self.Tp > 10000:
            # be fair with cpu, with 10s X is achievable even for 4004 :D
            steps = self.X
        else:
            steps = (self.X, self.X / 2, self.X / 2, self.X / 2, self.X / 2, 0)[randint(0, 5)]

        weapon = False
        if steps != 0:
            weapon = (True, False, False)[randint(0, 2)]

        return input_result(turbo=turbo, weapon=weapon, steps=steps)

    @staticmethod
    def check_turbo(requested_input):
        """
        turbo activation only depends on requested_input
        :param requested_input:
        :return: boolean reflecting if turbo was activated
        """
        if "I" in requested_input or "U" in requested_input:
            return True
        return False


class Commenter(object):
    """ used as code organizer for the comments related static method(s)"""

    @staticmethod
    def get_comment(name, result, strings):
        """
        :param name: camel name
        :param result:  namedtuple("input_result", "turbo weapon steps")
        :param strings: comment strings of one languages
        :return:
        """
        nice_word = strings.COMMENT_NICE_WORDS[randint(0, 3)]
        if result.weapon and result.turbo:
            comment = strings.COMMENT_WOW.format(name)
        elif result.turbo:
            comment = strings.COMMENT_TURBO.format(nice_word, name)
        elif result.weapon:
            comment = strings.COMMENT_WEAPON.format(nice_word, name)
        elif not randint(0, 2):  # if none applies, then third fo the time make another comment
            if randint(0, 1):  # can be generic or personalized per camel
                comment = strings.COMMENTS_RAND_PERS[randint(0, 2)].format(name)
            else:
                comment = strings.COMMENTS_RAND_GEN[randint(0, 8)]
        else:
            comment = None

        return comment


class CamelRaceGameConfig(object):
    """ parses and validates configs, instantiates camels as part of configs"""

    # DefaultConfigs applies when a key is missing, only in file mode as keys are
    # enforced in interactive mode
    DefaultConfigs = namedtuple("DefaultConfigs", "T TP X TERRAIN LANGUAGE")
    default_Configs = DefaultConfigs(T=6,
                                     TP=4,
                                     X=10,
                                     TERRAIN="Sand",
                                     LANGUAGE="English")

    def __init__(self, config):
        """
        Parse and validate configs
        instantiate camel objects and equip them with weapons
        :param config: json representation of global config and camels
        """

        try:
            global_config = config.get("global")
            self.T = 1000 * int(global_config.get("T", CamelRaceGameConfig.default_Configs.T))
            self.Tp = 1000 * int(global_config.get("Tp", CamelRaceGameConfig.default_Configs.TP))
            if self.T < self.Tp:
                raise ErrorInConfig("T must be bigger than Tp")
            self.X = int(global_config.get("X", CamelRaceGameConfig.default_Configs.X))
            self.terrain = global_config.get("terrain", CamelRaceGameConfig.default_Configs.TERRAIN)
            if self.terrain not in TerrainTypes.types:
                raise ErrorInConfig("Terrain {} not supported".format(self.terrain))
            self.language = global_config.get("language", CamelRaceGameConfig.default_Configs.LANGUAGE).lower()
            if self.language not in languages:
                raise ErrorInConfig("Not supported language {}".format(self.language))

            self.camels = OrderedDict()
            self.lane_2_camel = {}
            lane = 0
            for camel_config in config["camels"]:
                camel_name = camel_config.get("name")
                if camel_name in self.camels:
                    raise ErrorInConfig("Camel name must be unique, {} repeated".
                                         format(camel_name))

                self.camels[camel_name] = self.get_camel_from_json(camel_config)
                self.camels[camel_name].equip_weapon(impact=self.X)
                self.lane_2_camel[lane] = self.camels[camel_name]
                lane += 1

            self.num_players= len(self.camels)

        except (KeyError,ValueError) as ex:
            raise ErrorInConfig(ex.message)

    @staticmethod
    def get_camel_from_json(json_dict):
        """Camels factory method from json
        :raises keyError: raises an exception
        """
        camel_type = json_dict.get("type")
        if camel_type in CamelTypes.class_map:
            # return the corresponding camel object
            return CamelTypes.class_map[camel_type](
                json_dict.get("name"), json_dict.get("player").lower(),
                CamelRace.winner_camel_position)

    @staticmethod
    def prompt_for_config():
        """
        :return: CamelRaceGameConfig
        """

        config_option = raw_input("Enter 'C' for config mode or [enter] to load config from file:")
        if config_option.lower() != "c":
            configs = json_load(raw_input("Enter config file name [config.json]:").strip() or "config.json")
        else:
            try:
                num_camels = int(raw_input("Enter number of camels (minimum 1) default [3]:") or "3")
                if num_camels <= 0:
                    num_camels = 1
                camels = []
                for i in xrange(num_camels):
                    camel = {}
                    camel["name"] = raw_input(
                        "[config camel {}] Enter camel name:".format(i)).strip()  or "camel_{}".format(i+1)
                    camel["type"] = raw_input(
                        "[config camel {}] Enter camel type '[Bactrian] Domestic Dromedary':".format(i)).strip()  or "Bactrian"
                    camel["player"] = raw_input(
                        "[config camel {}] Enter player name or [cpu]:".format(i)).strip()  or "cpu"
                    camels.append(camel)
                global_configs = {}
                global_configs["T"] = abs(int(raw_input("Enter T [6]:") or "6"))
                global_configs["Tp"] = abs(int(raw_input("Enter Tp [4]:") or "4"))
                global_configs["X"] = abs(int(raw_input("Enter X [10]:") or "10"))
                global_configs["terrain"] = raw_input("Enter terrain type '[Sand] Mud Grass':").strip() or "Sand"
                global_configs["language"] = raw_input("Enter UI language '[English] Spanish':").strip() or "English"

                configs = {"global":global_configs, "camels":camels}
            except ValueError as ex:
                raise ErrorInConfig("Error Getting config from user:{}".format(ex.message))

        return CamelRaceGameConfig(configs)

    def __eq__(self, other):
        globals_are_equal = (self.T == other.T and
        self.Tp == other.Tp and
        self.X == other.X and
        self.language == self.language and
        self.terrain == other.terrain)

        camles_are_equal = True
        for camel_name in self.camels.keys():
            if camel_name in other.camels:
                if not (self.camels[camel_name] == other.camels[camel_name]):
                    camles_are_equal = False
                    break
            else:
                camles_are_equal = False
                break

        return globals_are_equal and camles_are_equal
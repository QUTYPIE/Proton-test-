#!/usr/bin/env python
import sys
from games.camels_race.race_game import CamelRace, ErrorInConfig, CamelRaceGameConfig
from games.games_exceptions import ConsoleDimenisionsTooSmall
from games.cli_game_launcher import Launcher


def main():
    try:
        # ask user to enter config or load from file
        game_config = CamelRaceGameConfig.prompt_for_config()
        # create game
        game = CamelRace(game_config)
        # Launch game using console launcher
        cli_game_launcher = Launcher(game)
        cli_game_launcher.loop()

    except ConsoleDimenisionsTooSmall as ex:
        print "Console is too small :", ex.message
        sys.exit(-1)
    except ErrorInConfig as ex:
        print "Configuration Error :", ex.message

if __name__ == '__main__':
    main()

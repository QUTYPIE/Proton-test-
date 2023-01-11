"""Contains Strings and possibly another constants"""

class English():
    WELCOME = "Welcome To Camel Race!"
    START_GAME = "Ready To Start An Epic Adventure? Press Any Key to Start:"
    INPUT_TURN = "Enter"
    EXIT = "Bye Bye!"
    COMMENT_WOW = "Wow, '{}' activates Turbo and uses weapon"
    COMMENT_TURBO = "{}, '{}' activates Turbo"
    COMMENT_WEAPON =  "{}, '{}' uses weapon"
    COMMENT_NICE_WORDS = ["Nice", "Cool", "Look!","Awsome!"]
    COMMENTS_RAND_PERS = ["'{}' looks tired today",
                          "'{}' is one of the best cammels",
                          "'{}' is working hard"]
    COMMENTS_RAND_GEN = [".....terrain is not helping ",
                         "...nice day for camel races",
                         "Typical spanish race!....",
                         "..What a great number of people watching",
                         "I love camels",
                         "Camels can survive 7 months without water!",
                         "...really cute animals",
                         "..greeting from the stadium..",
                         "These type of races move a lot of money!.."]
    TIE = "TIE!"
    WINNER = "The winner is {}, Congratulations!!!"
    PLAY_AGAIN = "Hit any button to play again, 'n' to exit:"


class Spanish():
    WELCOME = "Bienvenid@ a Camel Race!"
    START_GAME = "Listo Para Emprender Una Aventura Epica? Pulsa Para Empezar:"
    INPUT_TURN = "Entra"
    EXIT = "Adios!"
    COMMENT_WOW = "yuju, '{}' activa el turbo y usa su arma"
    COMMENT_TURBO = "{}, '{}' activa el turbo "
    COMMENT_WEAPON =  "{}, '{}' usa su arma"
    COMMENT_NICE_WORDS = ["Guay", "Como Mola!", "Fijate!","Genial!"]
    COMMENTS_RAND_PERS = ["'{}' parece cansado hoy",
                          "'{}' es uno de los mejores camellos",
                          "'{}' esta trabajando duro"]
    COMMENTS_RAND_GEN = [".....el suelo no ayuda",
                         "...buen dia para carrera de camellos",
                         "Tipico en los pueblos!....",
                         "..Cuanta gente viendo!",
                         "Adoro a los camellos",
                         "Un camellos puede vivir 7 meses sin agua!",
                         "...Que monos los camellos",
                         "..saludos desde el estadio..",
                         "Estas carreras mueven mucha pasta!.."]
    TIE = "EMPATE!"
    WINNER = "El Ganador es {}, Enhorabuena!!!"
    PLAY_AGAIN = "Pulsa cualquier tecla para jugar otra vez, 'n' para salir:"


class TerrainTypes(object):
    """ Enum like class for terrain types"""
    types = ["Mud", "Grass", "Sand"]
    Mud, Grass, Sand = types
    icon = {Mud:"~", Grass:"/", Sand:"="}
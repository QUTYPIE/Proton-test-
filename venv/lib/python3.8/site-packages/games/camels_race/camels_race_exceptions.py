class ErrorInConfig(Exception):
    pass


class InputTimedOut(Exception):
    """ raised by sigalarm handler """
    pass
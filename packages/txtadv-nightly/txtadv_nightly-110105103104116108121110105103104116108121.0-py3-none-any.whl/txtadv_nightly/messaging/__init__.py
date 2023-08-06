"""The messaging/error components of txtadv."""
from inspect import FrameInfo
import inspect

from txtadv.color import colored


def no_origin():
    """The no origin mode of logging."""
    return [FrameInfo('', 0, '', '', 0, 0), FrameInfo('', 0, '', '', 0, 0)]


origin = inspect.stack


def setinfomode(mode):
    """Set the info mode of messaging."""
    inspect.stack = mode


def error(message, target):
    """Print an error to the target."""

    ocolored(message, target, 'red')


def info(message, target):
    """Print an info message to the target"""
    ocolored(message, target, 'black')


def ocolored(message, target, color):
    """Print an colored message to the target if it is supported."""
    try:
        if target.colored:
            if inspect.stack == origin:
                target.outstream.write(
                    colored(
                        inspect.stack()[1].function.upper() + ": " + message,
                        color))
                target.write(
                    colored(
                        inspect.stack()[1].function.upper() + ": " + message,
                        color))
            else:
                target.outstream.write(colored(message, color))
                target.write(colored(message, color))
        else:
            if inspect.stack == origin:
                target.outstream.write(inspect.stack()[1].function.upper() +
                                       ": " + message)
                target.write(inspect.stack()[1].function.upper() + ": " +
                             message)
            else:
                target.outstream.write(message)
                target.write(message)
    except AttributeError:
        if inspect.stack == origin:
            target.write(inspect.stack()[1].function.upper() + ": " + message)
        else:
            target.write(message)
    try:
        target.outstream.flush()
    except AttributeError:
        target.flush()

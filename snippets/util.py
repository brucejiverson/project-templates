from __future__ import annotations

import datetime
import json
import logging
import math
import os
import re
import string
import time
from collections import Counter
from typing import Any, ClassVar, Mapping

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIRECTORY = os.path.join(root_dir, "logs")

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

CONFIG_FILE_PATH = os.path.join(root_dir, "config.json")


################# UTIL #################
def wait_for_ms(sleep_time_ms: float):
    """Waits for the given time in milliseconds.

    This function is included to avoid using time.sleep(), as time.sleep() is not very precise at the millisecond level.

    Arguments:
        sleep_time_ms {float} -- The time to wait in milliseconds
    """

    if sleep_time_ms <= 0:
        return
    start_time = time.time()
    sleep_time_s = sleep_time_ms / 1000
    while 1:
        if time.time() >= start_time + sleep_time_s:
            return


class ColoredConsoleFormatter(logging.Formatter):
    """
    A logging formatter that differentiates log levels using console color
    escapes. This works by injecting custom attributes into the record before
    forwarding it to the parent class.
    This implementation currently requires the ``'{'`` format style.
    :param str fmt: a standard str.format-style format string. Arbitrary color
    :param str datefmt: date format string
    :param colorspec: a mapping of log level to ``{color name: color definition}``.
        Color names are expected to follow the pattern ``nameColor`` and will not be
        properly handled otherwise. The default colorspec defines ``levelColor`` and
        ``messageColor``.
    """

    colors: ClassVar[dict[int, dict[str, str]]] = {
        logging.DEBUG: {"levelColor": "\033[0;37m", "messageColor": "\033[0;37m"},
        logging.INFO: {"levelColor": "\033[1;32m", "messageColor": "\033[0m"},
        logging.WARNING: {"levelColor": "\033[1;33m", "messageColor": "\033[0m"},
        logging.ERROR: {"levelColor": "\033[1;31m", "messageColor": "\033[0;1m"},
        logging.CRITICAL: {"levelColor": "\033[1;37;41m", "messageColor": ""},
    }

    default_format = "{levelColor}{asctime}{levelname:>8}{messageColor} {name}: {message}"
    # default_format = "{messageColor}{asctime} {levelColor}{levelname:>8}{messageColor} {name}: {message}"

    COLOR_RESET = "\033[0m"

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        colorspec: Mapping[int, Mapping[str, str]] | None = None,
    ):
        if not colorspec:
            colorspec = self.colors

        # there is, as far as I know, no reason to support a nonexistent format
        # string.
        if fmt is None:
            fmt = self.default_format

        if not fmt.endswith(self.COLOR_RESET):
            fmt += self.COLOR_RESET

        # sanity check that the colorspec is supported
        color_keys = {key for _, key, *_ in string.Formatter().parse(fmt) if key and key.endswith("Color")}

        for level, color_defs in colorspec.items():
            if not color_keys.issubset(color_defs):
                missing_colors = {*color_keys}.difference(color_defs)
                raise ValueError(
                    f"The provided colorspec is missing the color definitions {missing_colors} at level {level}"
                )

        self._defined_levels = sorted(colorspec.keys())
        self._colorspec = colorspec
        super().__init__(fmt, datefmt, style="{")

    def set_colorspec(self, spec: dict[int, dict[str, str]]) -> None:
        new_colorspec = {level: colors.copy() for level, colors in spec.items()}
        self._colorspec = new_colorspec

    def _get_level_spec(self, level: int) -> dict[str, str]:
        if level in self._colorspec:
            return dict(self._colorspec[level])
        for defined in self._defined_levels:
            if level <= defined:
                break
        # memoize
        approximate_level = dict(self._colorspec[defined])
        self._colorspec[level] = approximate_level  # type: ignore[index]
        return approximate_level

    def format(self, record):
        """Format the specified record as text."""
        for name, color in self._get_level_spec(record.levelno).items():
            setattr(record, name, color)

        return super().format(record)


def get_formatted_logger(name: str | None = None, level: str = "INFO", save_to_file: bool = True):
    """Returns a logger with a generic format"""
    if name is None:
        name = ""
    logger = logging.getLogger(name)

    # Create formatters and add it to handlers, add the handles to the logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    # console_format = logging.Formatter('%(asctime)s; %(name)s; %(levelname)s; %(message)s')
    console_format = ColoredConsoleFormatter()
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Create handlers. These say what to do with items as they get added to the logger
    if save_to_file:
        # get the folder path by eliminating the file name
        # check if the folder exists. If not, create it
        file_path = os.path.join(LOG_DIRECTORY, "{:%Y-%m-%d_%H-%M-%S}.txt".format(datetime.datetime.now()))
        # Create formatters and add it to handlers, add the handles to the logger
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        file_format = logging.Formatter("%(name)s; %(levelname)s; %(message)s")  # %(asctime)s;
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    # logger.info(f'Initialized logger {name}')
    return logger


# set up the root logger
print(f"cwd: {os.getcwd()}")
root_logger = get_formatted_logger("common_python_tools", level="DEBUG")

logger = logging.getLogger(__name__)
logger.setLevel(20)


def update_dict_with_value(d: dict, key: str, value: Any):
    """Useful for updating the cycling_config.json file with new values.
    Recursively searches through a dictionary and updates the value of the
    first key that matches the input key.

    Arguments:
        d {dict} -- The dictionary to search
        key {str} -- The key to search for
        value {Any} -- The value to update the key with
    """
    for k, v in d.items():
        if isinstance(v, dict):
            update_dict_with_value(v, key, value)
        elif k == key:
            logger.info(f"Updating config parameter {k} to {value}")
            d[k] = value


def read_config() -> dict[str, Any]:
    """Reads the config file at cycling_config.json and returns a dictionary with the contents."""
    try:
        with open(CONFIG_FILE_PATH) as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(
            f"Could not find config file at {CONFIG_FILE_PATH}. This is necessary for some processes involving lab instruments"
        )
    return {}


def get_port_from_config(config_key: str) -> str:
    """Returns the serial port from the cycling_config.json file"""
    config = read_config()
    if config_key in config["ports"].keys():
        return config["ports"][config_key]
    return f"NO PORT CONFIGURED FOR {config_key}"


# used for the cosine similarity function
WORD = re.compile(r"\w+")


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def get_cosine_similarity(str_1: str, str_2: str) -> float:
    """Returns the cosine similarity of two strings. The strings are first converted to vectors of word counts.

    https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings
    Another resource: https://pypi.org/project/strsimpy/
    """
    vec1, vec2 = text_to_vector(str_1), text_to_vector(str_2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator


def get_class_instance_from_args_or_kwargs(args: tuple, kwargs: dict, class_type: type) -> Any:
    """Returns the first instance of class_type in args or kwargs

    Args:
        args (tuple): The args to search
        kwargs (dict): The kwargs to search
        class_type (type): The type to search for

    Returns:
        Any: The first instance of class_type in args or kwargs
    """
    for arg in args:
        if isinstance(arg, class_type):
            return arg
    for kwarg in kwargs.values():
        if isinstance(kwarg, class_type):
            return kwarg
    return None


def prettify_dict(d: dict[Any, Any]) -> str:
    result = ""
    for k, v in d.items():
        result += f"{k}: {v}\n"
    return result


def get_lastest_git_tag() -> str:
    """Retrieves the latest tag on the repository.
    Raises an exception if there is an error.
    Note that doesn't work with light weight tags.
    Requires gitpython to be installed.
    """
    import git

    repo = git.Repo(root_dir)
    annotated_tags = [tag for tag in repo.tags if tag.tag is not None]
    tags = sorted(annotated_tags, key=lambda t: t.tag.tagged_date)
    latest_tag = tags[-1].tag.tag
    logger.info(f"Latest git tag on repo: {latest_tag}")
    return latest_tag


def get_latest_commit_hash() -> str:
    """Retrieves the latest commit hash on the repository.
    Raises an exception if there is an error.
    Requires gitpython to be installed.
    """
    import git

    repo = git.Repo(root_dir)
    latest_commit_hash = repo.head.object.hexsha
    logger.info(f"Latest commit hash on repo: {latest_commit_hash}")
    return latest_commit_hash

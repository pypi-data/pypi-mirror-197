"""module used for defining puzzle decorator for submitting or solving problem"""
from enum import Enum
from typing import Callable, List, Optional, TypeVar

from .cache_file import get_cache_file_data
from .config_file import get_all_session
from .server_action import submit_output

T = TypeVar("T")


class OperationType(Enum):
    SUBMIT = "submit"
    SOLVE = "solve"


class _Puzzle:
    """Puzzle class for handling a puzzle decorator"""

    def __init__(
        self,
        function: Callable[[str], T],
        year: int,
        day: int,
        part: int,
        operation_type: OperationType,
        sessions: Optional[List[str]] = None,
    ):
        """Initialize _Puzzle class"""
        self.function: Callable[[str], T] = function
        self.year: int = year
        self.day: int = day
        self.part: int = part
        self.operation_type: OperationType = operation_type
        if sessions is None:
            self.sessions: List[str] = get_all_session()
        else:
            self.sessions: List[str] = sessions

    def __repr__(self):
        """Return repr value of class which is set to function __name__"""
        return "{}".format(self.function.__name__)

    def get_function(self):
        """Get function from a class"""
        return self.function

    def __call__(self, input: Optional[str] = None):
        """Caller for _Puzzle class"""
        for session in self.sessions:
            if input is None:
                input = get_cache_file_data(self.year, self.day, session)
            answer = self.function(input)
            if answer is not None:
                if self.operation_type == OperationType.SUBMIT:
                    message = submit_output(
                        self.year, self.day, self.part, session, answer
                    )
                    if message.contains("Congratulation"):
                        print(
                            "{}:{}-{}-{}: {} {} {}".format(
                                session,
                                self.year,
                                self.day,
                                self.part,
                                answer,
                                "\u2713",
                                message,
                            )
                        )
                    else:
                        print(
                            "{}:{}-{}-{}: {} {} {}".format(
                                session,
                                self.year,
                                self.day,
                                self.part,
                                answer,
                                "\u274C",
                                message,
                            )
                        )
                elif self.operation_type == OperationType.SOLVE:
                    print(
                        "{}:{}-{}-{}: {}".format(
                            session, self.year, self.day, self.part, answer
                        )
                    )


def submit(
    year: int,
    day: int,
    part: int,
    session_list: Optional[List[str]] = None,
):
    """
    Puzzle decorator used to submit a solution to advent_of_code server and provide
    result. If input_file is not present then it tries to download file and cache it
    for submitting solution else it require to be provided with input_file path which
    input it can use.
    """

    def _action(function):
        return _Puzzle(
            function=function,
            operation_type=OperationType.SUBMIT,
            year=year,
            day=day,
            part=part,
            sessions=session_list,
        )

    return _action


def solve(
    year: int,
    day: int,
    part: int,
    session_list: Optional[List[str]] = None,
):
    """
    Puzzle decorator used to only solve a problem & print output value. It doesn't
    submit output to advent of code server to validate whether an answer is correct
    or not. By default it downloads input file from advent-of-code server. Puzzle
    can also be solved by using custom file location with help of input_file parameter
    while using input_file year, day, part are required even if they are not used for
    only reference purpose of printing output.
    """

    def _action(function):
        return _Puzzle(
            function=function,
            operation_type=OperationType.SOLVE,
            year=year,
            day=day,
            part=part,
            sessions=session_list,
        )

    return _action

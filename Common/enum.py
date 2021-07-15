from enum import Enum

class Direction(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4

class Trip_status(Enum):
    Created = 1
    Accepted = 2
    Ongoing = 3
    Finished = 4

class Driver_status(Enum):
    Available = 1
    Not_available = 2

class Driver_answer(Enum):
    Accept = 1
    Refuse = 2
    Already_refused = 3
    Busy = 4

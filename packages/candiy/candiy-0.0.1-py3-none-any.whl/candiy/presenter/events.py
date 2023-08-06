from enum import Enum, auto


class EventID(Enum):
    HEARTBEAT = auto()
    SPY = auto()
    POWER = auto()
    TESTER_MODE = auto()
    XCP_MODE = auto()
    XCP_GET_ECU_INFO = auto()

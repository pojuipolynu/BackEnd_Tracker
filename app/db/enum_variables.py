from enum import Enum

class InviteStatus(Enum):
    PENDING = "PENDING"
    DECLINED = "DECLINED"
    ACCEPTED = "ACCEPTED"

class PointsCalculations(Enum):
    USER_COUNT = 2
    HEADSTART_POINTS_COEF = 5

class CreationLimits(Enum):
    HABBIT_MIN = 1
    HABBIT_MAX = 5
    ACTIVE_ROOM_MAX = 20
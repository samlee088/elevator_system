from collections import deque
import heapq
import time
from enum import Enum

class State(Enum):
    IDLE = 1
    UP = 2
    DOWN = 3
    EMERGENCY = 4

class ElevatorType(Enum):
    PASSENGER = 1
    SERVICE = 2


class RequestOrigin(Enum):
    INSIDE = 1
    OUTSIDE = 2

class DoorState(Enum):
    OPEN = 1
    CLOSED = 2

class Request:
    def __init__(self, origin, origin_floor, destination_floor=None):
        self.origin = origin
        self.direction = State.IDLE
        self.origin_floor = origin_floor
        self.destination_floor = destination_floor
        self.elevator_type = ElevatorType.PASSENGER
    
        # Determine direction if both origin_floor and destination_floor are provided
        if destination_floor is not None:
            if origin_floor > destination_floor:
                self.direction = State.DOWN
            elif origin_floor < destination_floor:
                self.direction = State.UP
    
    def get_origin_floor(self):
        return self.origin_floor
    
    def get_destination_floor(self):
        return self.destination_floor
    
    def get_origin(self):
        return self.get_origin
    
    def get_direction(self):
        return self.direction
    
    # To determine order within the heap
    def _lt_(self, other):
        return self.destination_floor < other.destination_floor
    
    

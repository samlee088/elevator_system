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
    

class ServiceRequest(Request):
    def __init__(self, origin, current_floor = None, destination_floor = None):
        if current_floor is not None and destination_floor is not None:
            super().__init__(origin, current_floor, destination_floor)
        else:
            super().__init__(origin, destination_floor)
        self.elevator_type = ElevatorType.SERVICE

class Elevator:
    def __init__(self, current_floor, emergency_status):
        self.current_floor = current_floor
        self.state = State.IDLE
        self.emergency_status = emergency_status
        self.door_state = DoorState.CLOSED

    def open_doors(self):
        self.door_state = DoorState.OPEN
        print(f"Doors are OPEN on floor {self.current_floor}")

    def close_doors(self):
        self.door_state = DoorState.CLOSED
        print("Doors are CLOSED")

    def wait_for_seconds(self, seconds):
        time.sleep(seconds)

    def operate(self):
        pass

    def process_emergency(self):
        pass

    def get_current_floor(self):
        return self.current_floor
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state

    def set_current_floor(self, floor):
        self.current_floor = floor

    def get_door_state(self):
        return self.door_state
    
    def set_emergency_status(self, status):
        self.emergency_status = status


class PassengerElevator(Elevator):

    def __init__(self, current_floor, emergency_status):
        super().__init__(current_floor, emergency_status)
        self.passenger_up_queue = []
        self.passenger_down_queue = []

    def operate(self):
        while self.passenger_up_queue or self.passenger_down_queue:
            self.process_requests()
        self.set_state(State.IDLE)
        print("All requests have been fulfilled, elevator is now", self.get_state())
    
    def process_emergency(self):
        self.passenger_up_queue.clear()
        self.passenger_down_queue.clear()
        self.set_current_floor(1)
        self.set_state(State.idle)
        self.open_doors()
        self.set_emergency_status(True)
        print("Queues cleared, current floor is",
              self.get_current_floor(), ". Doors are", self.get_door_state())
        
    def add_up_request(self, request):
        if request.get_origin() == RequestOrigin.OUTSIDE:
            pick_up_request = Request(request.get_origin(), request.get_origin_floor(), request.get_origin_floor())
            heapq.heappush(self.passenger_up_queue, pick_up_request)
        heapq.heappush(self.passenger_up_queue, request)

    def add_down_request(self, request):
        if request.get_origin() == RequestOrigin.OUTSIDE:
            pick_up_request = Request(request.get_origin(), request.get_origin_floor, request.get_origin_floor())
            heapq.heappush(self.passenger_down_queue, pick_up_request)
        heapq.heappush(self.passenger_down_queue, request)

    def process_up_requests(self):
        while self.passenger_up_queue:
            up_request = heapq.heappop(self.passenger_up_queue)

            if self.get_current_floor() == up_request.get_destination_floor():
                print("Currently on floor", self.get_current_floor(),
                      ". No movement as destination is the same.")
                continue
            print("The current floor is", self.get_current_floor(),
                  ". Next stop:", up_request.get_destination_floor())
            
            try:
                print("Moving ", end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)  # Pause for half a second between dots.
                time.sleep(1)  # Assuming 1 second to move to the next floor.
                print()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)

            self.set_current_floor(up_request.get_destination_floor())
            print("Arrived at", self.get_current_floor())

            self.open_doors()
            # Simulating 3 seconds for people to enter/exit.
            self.wait_for_seconds(3)
            self.close_doors()

        print("Finished processing all the up requests.")

    def process_down_requests(self):
        while self.passenger_down_queue:
            down_request = heapq.heappop(self.passenger_down_queue)

            if self.get_current_floor() == down_request.get_destination_floor():
                print("Currently on floor", self.get_current_floor(),
                      ". No movement as destination is the same.")
                continue

            print("The current floor is", self.get_current_floor(),
                  ". Next stop:", down_request.get_destination_floor())

            try:
                print("Moving ", end="")
                for _ in range(3):
                    print(".", end="", flush=True)
                    time.sleep(0.5)  # Pause for half a second between dots.
                time.sleep(1)  # Assuming 1 second to move to the next floor.
                print()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)

            self.set_current_floor(down_request.get_destination_floor())
            print("Arrived at", self.get_current_floor())

            self.open_doors()
            # Simulating 3 seconds for people to enter/exit.
            self.wait_for_seconds(3)
            self.close_doors()

        print("Finished processing all the down requests.")

    def process_requests(self):
        if self.get_state() == State.UP or self.get_state() == State.IDLE:
            self.process_up_requests()
            if self.passenger_down_queue:
                print("Now processing down requests...")
                self.process_down_requests()
        else:
            self.process_down_requests()
            if self.process_up_requests:
                print("Now processing up requests...")
                self.process_up_requests()

                
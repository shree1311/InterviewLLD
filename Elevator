from enum import Enum
class Direction(Enum):
    UP = 1
    DOWN = 2

class Request:
    def __init__(self, source_floor, destination_floor):
        self.source_floor = source_floor
        self.destination_floor = destination_floor
    
import time
from threading import Lock, Condition
from request import Request
from direction import Direction


class Elevator:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.current_direction = Direction.UP
        self.requests = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_request(self, request: Request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(
                    f"Elevator {self.id} added request: {request.source_floor} to {request.destination_floor}"
                )
                self.condition.notify_all()

    def get_next_request(self) -> Request:
        with self.lock:
            while not self.requests:
                self.condition.wait()
            return self.requests.pop(0)

    def process_requests(self):
        while True:
            request = self.get_next_request()  # This will wait until there's a request
            self.process_request(request)

    def process_request(self, request: Request):
        start_floor = self.current_floor
        end_floor = request.destination_floor

        if start_floor < end_floor:
            self.current_direction = Direction.UP
            for i in range(start_floor, end_floor + 1):
                self.current_floor = i
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulating elevator movement
        elif start_floor > end_floor:
            self.current_direction = Direction.DOWN
            for i in range(start_floor, end_floor - 1, -1):
                self.current_floor = i
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulating elevator movement

    def run(self):
        self.process_requests()

from threading import Thread
from elevator import Elevator
from request import Request

class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int):
        self.elevators = []
        for i in range(num_elevators):
            elevator = Elevator(i + 1, capacity)
            self.elevators.append(elevator)
            Thread(target=elevator.run).start()

    def request_elevator(self, source_floor: int, destination_floor: int):
        optimal_elevator = self.find_optimal_elevator(source_floor, destination_floor)
        optimal_elevator.add_request(Request(source_floor, destination_floor))

    def find_optimal_elevator(self, source_floor: int, destination_floor: int) -> Elevator:
        optimal_elevator = None
        min_distance = float('inf')

        for elevator in self.elevators:
            distance = abs(source_floor - elevator.current_floor)
            if distance < min_distance:
                min_distance = distance
                optimal_elevator = elevator

        return optimal_elevator
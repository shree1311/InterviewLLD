from datetime import datetime

class Vehicle:
    """Represents a vehicle in the rental system."""
    def __init__(self, vehicle_id, make, model, year, daily_rate):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True

class User:
    """Represents a user of the rental system."""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Store:
    """Represents a rental store location."""
    def __init__(self, store_id, location):
        self.store_id = store_id
        self.location = location
        self.vehicles = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def get_available_vehicles(self):
        return [v for v in self.vehicles if v.is_available]

class Reservation:
    """Represents a vehicle reservation."""
    def __init__(self, reservation_id, user: User, vehicle: Vehicle, start_date, end_date):
        self.reservation_id = reservation_id
        self.user = user
        self.vehicle = vehicle
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = (end_date - start_date).days * vehicle.daily_rate

class CarRentalSystem:
    """The main class to manage the car rental operations."""
    def __init__(self):
        self.users = []
        self.stores = []
        self.reservations = []
        self._next_reservation_id = 1

    def add_user(self, user: User):
        self.users.append(user)

    def add_store(self, store: Store):
        self.stores.append(store)

    def search_vehicle(self, store_location):
        for store in self.stores:
            if store.location.lower() == store_location.lower():
                return store.get_available_vehicles()
        return []

    def make_reservation(self, user: User, vehicle: Vehicle, start_date, end_date):
        if not vehicle.is_available:
            print("Vehicle is not available for the selected dates.")
            return None

        vehicle.is_available = False
        reservation = Reservation(self._next_reservation_id, user, vehicle, start_date, end_date)
        self.reservations.append(reservation)
        self._next_reservation_id += 1
        return reservation

    def return_vehicle(self, reservation: Reservation):
        reservation.vehicle.is_available = True
        print(f"Vehicle {reservation.vehicle.vehicle_id} has been returned.")


if __name__ == "__main__":
    system = CarRentalSystem()

    # Setup
    user1 = User(1, "Alice")
    system.add_user(user1)

    store1 = Store(101, "Columbus Airport")
    system.add_store(store1)

    vehicle1 = Vehicle("V001", "Toyota", "Camry", 2023, 50)
    vehicle2 = Vehicle("V002", "Honda", "CRV", 2024, 70)
    store1.add_vehicle(vehicle1)
    store1.add_vehicle(vehicle2)

    # User searches for a car
    print("Searching for available vehicles at Columbus Airport...")
    available = system.search_vehicle("Columbus Airport")
    for v in available:
        print(f"  - {v.make} {v.model} (${v.daily_rate}/day)")

    # User makes a reservation
    if available:
        start = datetime(2025, 7, 10)
        end = datetime(2025, 7, 15)
        reservation = system.make_reservation(user1, available[0], start, end)
        if reservation:
            print(f"\nReservation successful for {user1.name}!")
            print(f"Vehicle: {reservation.vehicle.make} {reservation.vehicle.model}")
            print(f"Total Cost: ${reservation.total_cost:.2f}")

            # Later, user returns the vehicle
            print("\nReturning vehicle...")
            system.return_vehicle(reservation)
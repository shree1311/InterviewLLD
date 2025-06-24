from enum import Enum
from datetime import datetime
class OrderStatus(Enum):
    PENDING = 1
    PREPARING = 2
    READY = 3
    COMPLETED = 4
    CANCELLED = 5

class Order:
    def __init__(self, id, items, total_amount, status, timestamp):
        self.id = id
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.timestamp = timestamp

    def set_status(self, status):
        self.status = status

    def get_id(self):
        return self.id

    def get_items(self):
        return self.items

    def get_total_amount(self):
        return self.total_amount

    def get_status(self):
        return self.status

    def get_timestamp(self):
        return self.timestamp

class MenuItem:
    def __init__(self, id, name, description, price, available):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.available = available

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def is_available(self):
        return self.available

class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2
    MOBILE_PAYMENT = 3

class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3

class Payment:
    def __init__(self, id, amount, method, status):
        self.id = id
        self.amount = amount
        self.method = method
        self.status = status

    def get_id(self):
        return self.id

    def get_amount(self):
        return self.amount

    def get_method(self):
        return self.method

    def get_status(self):
        return self.status
    
class Staff:
    def __init__(self, id, name, role, contact_number):
        self.id = id
        self.name = name
        self.role = role
        self.contact_number = contact_number

from concurrent.futures import ThreadPoolExecutor
class Restaurant:
    _instance = None
    _lock = ThreadPoolExecutor(max_workers=1)

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.menu = []
        self.orders = {}
        self.reservations = []
        self.payments = {}
        self.staff = []

    def add_menu_item(self, item):
        self.menu.append(item)

    def remove_menu_item(self, item):
        self.menu.remove(item)

    def get_menu(self):
        return self.menu[:]

    def place_order(self, order):
        self.orders[order.get_id()] = order
        self._notify_kitchen(order)

    def update_order_status(self, order_id, status):
        order = self.orders.get(order_id)
        if order:
            order.set_status(status)
            self._notify_staff(order)

    def make_reservation(self, reservation):
        self.reservations.append(reservation)

    def cancel_reservation(self, reservation):
        self.reservations.remove(reservation)

    def process_payment(self, payment):
        self.payments[payment.get_id()] = payment

    def add_staff(self, staff):
        self.staff.append(staff)

    def remove_staff(self, staff):
        self.staff.remove(staff)

    def _notify_kitchen(self, order):
        pass

    def _notify_staff(self, order):
        pass
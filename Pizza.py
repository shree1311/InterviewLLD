# main_pizzashop.py

from enum import Enum
from typing import List, Set

# Step 1: Define Enums for fixed choices to make the code robust and readable.
# Each enum member holds its base price.

class Size(Enum):
    SMALL = (8.00, "Small")
    MEDIUM = (10.00, "Medium")
    LARGE = (12.00, "Large")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

class Crust(Enum):
    THIN = (2.00, "Thin Crust")
    HAND_TOSSED = (2.50, "Hand-Tossed")
    DEEP_DISH = (3.50, "Deep Dish")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

class Topping(Enum):
    PEPPERONI = (1.50, "Pepperoni")
    MUSHROOMS = (1.00, "Mushrooms")
    ONIONS = (0.75, "Onions")
    EXTRA_CHEESE = (2.00, "Extra Cheese")
    TOMATO_SAUCE = (0.50, "Tomato Sauce")
    BASIL = (0.75, "Basil")
    
    def __init__(self, price, description):
        self.price = price
        self.description = description

# Step 2: Define the Pizza class, which will be constructed by our Builder.
class Pizza:
    """Represents the final, complex Pizza object."""
    def __init__(self, builder):
        self.size: Size = builder.size
        self.crust: Crust = builder.crust
        self.toppings: Set[Topping] = builder.toppings

    def calculate_price(self) -> float:
        """Calculates the total price based on size, crust, and toppings."""
        price = self.size.price + self.crust.price
        price += sum(topping.price for topping in self.toppings)
        return round(price, 2)

    def __str__(self) -> str:
        """Provides a human-readable description of the pizza."""
        description = f"- {self.size.description} {self.crust.description} Pizza (${self.calculate_price():.2f})\n"
        if self.toppings:
            description += "  Toppings: " + ", ".join(t.description for t in sorted(list(self.toppings), key=lambda t: t.name))
        return description

    # Step 3: Implement the Builder as a nested class.
    class Builder:
        """A fluent builder for constructing Pizza objects step-by-step."""
        def __init__(self):
            self.size: Size = None
            self.crust: Crust = None
            self.toppings: Set[Topping] = set()

        def with_size(self, size: Size):
            self.size = size
            return self # Return self to allow for method chaining

        def with_crust(self, crust: Crust):
            self.crust = crust
            return self

        def add_topping(self, topping: Topping):
            self.toppings.add(topping)
            return self

        def build(self) -> 'Pizza':
            """Validates and creates the final Pizza object."""
            if not self.size or not self.crust:
                raise ValueError("A pizza must have a size and a crust.")
            return Pizza(self)

# Step 4: Define an Order class to hold items and calculate totals.
class Order:
    """Represents a customer's order, containing multiple items."""
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.items: List[Pizza] = []

    def add_item(self, item: Pizza):
        """Adds a configured pizza to the order."""
        self.items.append(item)

    def calculate_total(self) -> float:
        """Calculates the grand total for the order."""
        total = sum(item.calculate_price() for item in self.items)
        return round(total, 2)

    def print_receipt(self):
        """Prints a detailed receipt for the order."""
        print(f"--- Order #{self.order_id} ---")
        if not self.items:
            print("Order is empty.")
        else:
            for item in self.items:
                print(str(item))
        print("--------------------")
        print(f"Total: ${self.calculate_total():.2f}")
        print("--------------------")

# Step 6: The main application ties everything together.
# This demonstrates how a client would use your classes.
def main():
    """Main function to simulate placing an order at the pizza shop."""
    # Create a new order
    order = Order(order_id=101)
    
    # --- Add a custom-built pizza ---
    print("\nBuilding a custom pizza...")
    custom_pizza = Pizza.Builder()\
                        .with_size(Size.LARGE)\
                        .with_crust(Crust.DEEP_DISH)\
                        .add_topping(Topping.PEPPERONI)\
                        .add_topping(Topping.MUSHROOMS)\
                        .add_topping(Topping.ONIONS)\
                        .build()
    order.add_item(custom_pizza)
    
    # Print the final receipt
    print("\nFinal Order Details:")
    order.print_receipt()


if __name__ == "__main__":
    main()
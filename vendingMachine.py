class Item:
    """Represents an item available in the vending machine."""
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Inventory:
    """Manages the stock of a particular item."""
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
        else:
            raise ValueError("Item is out of stock.")

# State Pattern Implementation
class VendingMachineState(ABC):
    """Abstract base class for all machine states."""
    @abstractmethod
    def select_item(self, machine, item_name: str):
        pass

    @abstractmethod
    def insert_money(self, machine, amount: float):
        pass

    @abstractmethod
    def dispense_item(self, machine):
        pass

class NoMoneyState(VendingMachineState):
    """State when no money has been inserted."""
    def select_item(self, machine, item_name: str):
        print(f"Selected {item_name}. Please insert money.")
        machine.selected_item_name = item_name
        machine.set_state(HasMoneyState())

    def insert_money(self, machine, amount: float):
        print("Please select an item first.")

    def dispense_item(self, machine):
        print("Please select an item and insert money first.")

class HasMoneyState(VendingMachineState):
    """State when an item is selected and waiting for money."""
    def select_item(self, machine, item_name: str):
        print(f"Already processing a selection. Please insert money for {machine.selected_item_name}.")

    def insert_money(self, machine, amount: float):
        machine.inserted_money += amount
        print(f"Inserted ${amount:.2f}. Total: ${machine.inserted_money:.2f}")

        selected_inventory = machine.inventory.get(machine.selected_item_name)
        if not selected_inventory:
            print("Error: Item not found.")
            machine.eject_money()
            return
            
        if machine.inserted_money >= selected_inventory.item.price:
            self.dispense_item(machine)
        else:
            needed = selected_inventory.item.price - machine.inserted_money
            print(f"Please insert ${needed:.2f} more.")


    def dispense_item(self, machine):
        selected_inventory = machine.inventory.get(machine.selected_item_name)
        
        try:
            selected_inventory.decrease_quantity()
            change = machine.inserted_money - selected_inventory.item.price
            print(f"Dispensing {machine.selected_item_name}.")
            if change > 0:
                print(f"Returning change: ${change:.2f}")
            machine.reset()
        except ValueError as e:
            print(e)
            machine.eject_money()

class VendingMachine:
    """The main class representing the vending machine."""
    def __init__(self):
        self.inventory = {}
        self.state = NoMoneyState()
        self.inserted_money = 0.0
        self.selected_item_name = None

    def load_inventory(self, item: Item, quantity: int):
        self.inventory[item.name] = Inventory(item, quantity)
        print(f"Loaded {quantity} of {item.name}.")

    def set_state(self, state: VendingMachineState):
        self.state = state

    def select_item(self, item_name: str):
        self.state.select_item(self, item_name)
    
    def insert_money(self, amount: float):
        self.state.insert_money(self, amount)

    def eject_money(self):
        print(f"Ejecting ${self.inserted_money:.2f}.")
        self.reset()
    
    def reset(self):
        self.inserted_money = 0.0
        self.selected_item_name = None
        self.set_state(NoMoneyState())
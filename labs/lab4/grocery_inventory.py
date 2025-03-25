import os
from abc import ABC, abstractmethod

# Singleton Record class for file handling
class Record:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Record, cls).__new__(cls)
        return cls._instance

    def __init__(self, filename="record.txt"):
        # Initialize only once
        if not hasattr(self, "_initialized"):
            self.filename = filename
            # Ensure the file exists; open in append mode
            with open(self.filename, "a") as f:
                pass
            self._initialized = True

    def read(self):
        """Reads and prints the contents of the file."""
        try:
            with open(self.filename, "r") as f:
                content = f.read()
                print(content, end="")  # Avoid extra newline
        except IOError as e:
            print("An error occurred while reading the file:", e)

    def write(self, msg: str):
        """Appends the specified message to the file."""
        try:
            with open(self.filename, "a") as f:
                f.write(msg)
        except IOError as e:
            print("An error occurred while writing to the file:", e)


# Abstract base class for the Composite pattern
class FoodComponent(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def display(self, level: int) -> None:
        pass


# Leaf component representing a food item.
class FoodItem(FoodComponent):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def get_price(self) -> float:
        return self.price

    def display(self, level: int) -> None:
        indent = "  " * level
        print(f"{indent}FoodItem: {self.name}, {self.price}")


# Composite component representing a food category.
class FoodCategory(FoodComponent):
    def __init__(self, name: str):
        self.name = name
        self.components = []  # List of FoodComponent objects

    def add(self, component: FoodComponent) -> None:
        self.components.append(component)

    def get_price(self) -> float:
        total = 0.0
        for component in self.components:
            total += component.get_price()
        return total

    def display(self, level: int) -> None:
        indent = "  " * level
        cumulative_price = self.get_price()
        print(f"{indent}FoodCategory ({self.name}, {cumulative_price}) contains:")
        for component in self.components:
            component.display(level + 2)


# Test functions to demonstrate functionality
def test_record():
    # Obtain the singleton instance of Record.
    record_instance = Record()
    record_instance.write("Hello-1\n")
    record_instance.write("Hello-2\n")
    print("Currently the file record.txt contains the following lines:")
    record_instance.read()


def test_composite():
    # Create food items.
    fi1 = FoodItem("blueberries", 2.5)
    fi2 = FoodItem("strawberries", 3.5)
    fi3 = FoodItem("egg", 4.5)
    fi4 = FoodItem("chicken", 5.0)
    fi5 = FoodItem("peas", 6.0)
    fi6 = FoodItem("icecream", 7.0)

    # Create food categories.
    fc1 = FoodCategory("frozen")
    fc2 = FoodCategory("meat")
    fc3 = FoodCategory("vegetables")

    # Build the composite structure.
    fc1.add(fc2)
    fc1.add(fc3)
    fc1.add(fi6)

    fc2.add(fi3)
    fc2.add(fi4)

    fc3.add(fi1)
    fc3.add(fi2)
    fc3.add(fi5)

    # Display the complete structure.
    fc1.display(0)


if __name__ == "__main__":
    print("=== Testing Record Singleton ===")
    test_record()
    print("\n=== Testing Food Composite Structure ===")
    test_composite()
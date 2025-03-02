from abc import ABC, abstractmethod

class Flight:
    def __init__(self, flight_number: int, origin: str, destination: str, departure_time: str, capacity: int, original_price: float):
        if origin == destination:
            raise ValueError("Origin and destination cannot be the same.")
        self._flight_number = flight_number
        self._origin = origin
        self._destination = destination
        self._departure_time = departure_time
        self._capacity = capacity
        self._number_of_seats_left = capacity
        self._original_price = original_price

    @property
    def flight_number(self):
        return self._flight_number

    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._destination

    @property
    def departure_time(self):
        return self._departure_time

    @property
    def capacity(self):
        return self._capacity

    @property
    def number_of_seats_left(self):
        return self._number_of_seats_left

    @property
    def original_price(self):
        return self._original_price

    def book_a_seat(self) -> bool:
        if self._number_of_seats_left > 0:
            self._number_of_seats_left -= 1
            return True
        return False

    def __str__(self):
        return f"Flight {self._flight_number}, {self._origin} to {self._destination}, {self._departure_time}, original price: {self._original_price}$"

class Passenger(ABC):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

class Member(Passenger):
    def __init__(self, name: str, age: int, years_of_membership: int):
        super().__init__(name, age)
        self._years_of_membership = years_of_membership

    def apply_discount(self, price: float) -> float:
        if self._years_of_membership > 5:
            return price * 0.5
        elif self._years_of_membership > 1:
            return price * 0.9
        return price

class NonMember(Passenger):
    def apply_discount(self, price: float) -> float:
        return price * 0.9 if self._age > 65 else price

class Ticket:
    _ticket_counter = 1
    
    def __init__(self, passenger: Passenger, flight: Flight, price: float):
        self._passenger = passenger
        self._flight = flight
        self._price = price
        self._ticket_number = Ticket._ticket_counter
        Ticket._ticket_counter += 1
    
    def __str__(self):
        return f"{self._passenger.name}, {self._flight}, ticket price: ${self._price:.2f}"

class Manager:
    def __init__(self):
        self._flights = []
        self._tickets = []
    
    def create_flights(self):
        self._flights.append(Flight(101, "New York", "London", "10:00 AM", 200, 800))
        self._flights.append(Flight(102, "Paris", "Tokyo", "4:30 PM", 150, 1200))
    
    def display_available_flights(self, origin: str, destination: str):
        for flight in self._flights:
            if flight.origin == origin and flight.destination == destination and flight.number_of_seats_left > 0:
                print(flight)
    
    def get_flight(self, flight_number: int):
        for flight in self._flights:
            if flight.flight_number == flight_number:
                return flight
        return None
    
    def book_seat(self, flight_number: int, passenger: Passenger):
        flight = self.get_flight(flight_number)
        if flight and flight.book_a_seat():
            discounted_price = passenger.apply_discount(flight.original_price)
            ticket = Ticket(passenger, flight, discounted_price)
            self._tickets.append(ticket)
            print("Ticket issued:", ticket)
        else:
            print("Booking failed. No seats available.")
    
if __name__ == "__main__":
    manager = Manager()
    manager.create_flights()
    
    passenger1 = Member("Alice", 30, 6)
    passenger2 = NonMember("Bob", 70)
    
    manager.book_seat(101, passenger1)
    manager.book_seat(102, passenger2)
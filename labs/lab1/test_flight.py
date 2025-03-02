import unittest
from flight_management import Flight, Member, NonMember, Manager, Ticket

class TestFlight(unittest.TestCase):
    
    def test_constructor(self):
        # Test valid flight creation
        flight = Flight(101, "New York", "London", "10:00 AM", 200, 800.0)
        self.assertEqual(flight.flight_number, 101)
        self.assertEqual(flight.origin, "New York")
        self.assertEqual(flight.destination, "London")
        self.assertEqual(flight.departure_time, "10:00 AM")
        self.assertEqual(flight.capacity, 200)
        self.assertEqual(flight.number_of_seats_left, 200)
        self.assertEqual(flight.original_price, 800.0)
    
    def test_invalid_constructor(self):
        # Test invalid flight creation (same origin and destination)
        with self.assertRaises(ValueError):
            Flight(102, "Paris", "Paris", "2:00 PM", 150, 1200.0)
    
    def test_book_a_seat(self):
        # Test booking a seat
        flight = Flight(103, "Berlin", "Tokyo", "5:00 PM", 2, 900.0)
        self.assertTrue(flight.book_a_seat())
        self.assertEqual(flight.number_of_seats_left, 1)
        self.assertTrue(flight.book_a_seat())
        self.assertEqual(flight.number_of_seats_left, 0)
        self.assertFalse(flight.book_a_seat())
    
    def test_str_method(self):
        # Test string representation
        flight = Flight(104, "Sydney", "Dubai", "8:30 AM", 100, 700.0)
        self.assertEqual(str(flight), "Flight 104, Sydney to Dubai, 8:30 AM, original price: 700.0$")
    
class TestPassenger(unittest.TestCase):
    
    def test_member_discount(self):
        member1 = Member("Alice", 30, 6)  # More than 5 years -> 50% discount
        self.assertEqual(member1.apply_discount(1000), 500.0)
        
        member2 = Member("Bob", 40, 3)  # 1-5 years -> 10% discount
        self.assertEqual(member2.apply_discount(1000), 900.0)
        
        member3 = Member("Charlie", 25, 1)  # Less than 1 year -> No discount
        self.assertEqual(member3.apply_discount(1000), 1000.0)
    
    def test_non_member_discount(self):
        non_member1 = NonMember("David", 70)  # Age > 65 -> 10% discount
        self.assertEqual(non_member1.apply_discount(1000), 900.0)
        
        non_member2 = NonMember("Eve", 50)  # Age <= 65 -> No discount
        self.assertEqual(non_member2.apply_discount(1000), 1000.0)

class TestManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = Manager()
        self.manager.create_flights()
    
    def test_get_flight(self):
        flight = self.manager.get_flight(101)
        self.assertIsNotNone(flight)
        self.assertEqual(flight.flight_number, 101)
        
        no_flight = self.manager.get_flight(999)
        self.assertIsNone(no_flight)
    
    def test_book_seat(self):
        passenger = Member("Frank", 35, 2)
        self.manager.book_seat(101, passenger)
        flight = self.manager.get_flight(101)
        self.assertEqual(flight.number_of_seats_left, 199)
    
class TestTicket(unittest.TestCase):
    
    def test_ticket_creation(self):
        passenger = NonMember("Grace", 60)
        flight = Flight(105, "Rome", "Athens", "9:00 AM", 50, 500.0)
        ticket = Ticket(passenger, flight, passenger.apply_discount(flight.original_price))
        self.assertEqual(ticket._passenger.name, "Grace")
        self.assertEqual(ticket._flight.flight_number, 105)
        self.assertEqual(ticket._price, 500.0)
    
if __name__ == "__main__":
    unittest.main()
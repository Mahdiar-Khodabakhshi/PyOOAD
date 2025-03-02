import unittest
from flight_management import Manager, Flight, Member, NonMember

class TestManager(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        self.manager.create_flights()
        self.member = Member("Alice", 30, 6)
        self.non_member = NonMember("Bob", 70)

    def test_create_flights(self):
        self.assertEqual(len(self.manager._flights), 2)
        
    def test_get_flight(self):
        flight = self.manager.get_flight(101)
        self.assertIsNotNone(flight)
        self.assertEqual(flight.flight_number, 101)

    def test_get_flight_invalid(self):
        flight = self.manager.get_flight(999)
        self.assertIsNone(flight)

    def test_book_seat_success_member(self):
        self.manager.book_seat(101, self.member)
        self.assertEqual(self.manager._flights[0].number_of_seats_left, 199)

    def test_book_seat_success_non_member(self):
        self.manager.book_seat(102, self.non_member)
        self.assertEqual(self.manager._flights[1].number_of_seats_left, 149)

    def test_book_seat_no_availability(self):
        flight = self.manager.get_flight(101)
        flight._number_of_seats_left = 0  # Manually setting to 0 for test
        self.manager.book_seat(101, self.member)
        self.assertEqual(flight.number_of_seats_left, 0)

if __name__ == "__main__":
    unittest.main()

    # python -m unittest discover: This will automatically discover and run all test_*.py files.
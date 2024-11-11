from django.core.exceptions import ValidationError
from django.test import TestCase
from Airport.models import User, Airport, Route, AirplaneType, Flight, Crew, Order, Ticket


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='password123'
        )

        self.airport1 = Airport.objects.create(
            name='Airport1',
            closest_big_city='BigCity1'
        )
        self.airport2 = Airport.objects.create(
            name='Airport2',
            closest_big_city='BigCity2'
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=500
        )

        self.airplane_type = AirplaneType.objects.create(
            name='Boeing 747'
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane_type,
            flight_number='A123',
            total_rows=30,
            seats_in_row=6
        )

        self.crew = Crew.objects.create(
            first_name='John',
            last_name='Doe'
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number='ORD12345'
        )

    def test_user_creation(self):
        """Test creating a User instance."""
        user = User.objects.create(
            username='newuser',
            first_name='New',
            last_name='User',
            email='newuser@example.com',
            password='newpassword123'
        )
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(str(user), 'newuser')

    def test_airport_creation(self):
        """Test creating an Airport instance."""
        airport = Airport.objects.create(
            name='Airport3',
            closest_big_city='BigCity3'
        )
        self.assertEqual(airport.name, 'Airport3')
        self.assertEqual(str(airport), 'Airport3 (Closest big city: BigCity3)')

    def test_route_creation(self):
        """Test creating a Route instance."""
        route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=400
        )
        self.assertEqual(route.source, self.airport1)
        self.assertEqual(route.destination, self.airport2)
        self.assertEqual(route.distance, 400)
        self.assertEqual(str(route), f"{self.airport1} -> {self.airport2}, 400 km")

    def test_airplane_type_creation(self):
        """Test creating an AirplaneType instance."""
        airplane_type = AirplaneType.objects.create(
            name='Airbus A320'
        )
        self.assertEqual(airplane_type.name, 'Airbus A320')
        self.assertEqual(str(airplane_type), 'name')

    def test_flight_creation(self):
        """Test creating a Flight instance."""
        flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane_type,
            flight_number='B456',
            total_rows=40,
            seats_in_row=8
        )
        self.assertEqual(flight.flight_number, 'B456')
        self.assertEqual(flight.total_rows, 40)
        self.assertEqual(flight.seats_in_row, 8)
        self.assertEqual(str(flight), f"Flight B456 on {self.airplane_type} {self.route}")

    def test_crew_creation(self):
        """Test creating a Crew instance."""
        crew = Crew.objects.create(
            first_name='Jane',
            last_name='Doe'
        )
        self.assertEqual(crew.first_name, 'Jane')
        self.assertEqual(crew.last_name, 'Doe')
        self.assertEqual(str(crew), 'Jane Doe')

    def test_order_creation(self):
        """Test creating an Order instance."""
        order = Order.objects.create(
            user=self.user,
            order_number='ORD67890'
        )
        self.assertEqual(order.order_number, 'ORD67890')
        self.assertEqual(str(order), str(order.created_at))

    def test_ticket_creation_and_validation(self):
        """Test creating a Ticket instance and validation."""
        ticket = Ticket.objects.create(
            flight=self.flight,
            order=self.order,
            row=5,
            seat='2'
        )
        self.assertEqual(ticket.flight, self.flight)
        self.assertEqual(ticket.row, 5)
        self.assertEqual(ticket.seat, '2')
        self.assertEqual(str(ticket), f"{self.flight} (row: 5, seat: 2)")

    def test_ticket_unique_constraint(self):
        """Test that a Ticket is unique per flight, row, and seat."""
        Ticket.objects.create(
            flight=self.flight,
            order=self.order,
            row=5,
            seat='3'
        )

        with self.assertRaises(ValidationError):
            ticket = Ticket(
                flight=self.flight,
                order=self.order,
                row=5,
                seat='3'
            )
            ticket.full_clean()

    def test_ticket_invalid_row(self):
        """Test that Ticket raises a validation error if row is out of bounds."""
        with self.assertRaises(ValidationError):
            ticket = Ticket(
                flight=self.flight,
                order=self.order,
                row=31,
                seat='2'
            )
            ticket.full_clean()

    def test_ticket_invalid_seat(self):
        """Test that Ticket raises a validation error if seat is out of bounds."""
        with self.assertRaises(ValidationError):
            ticket = Ticket(
                flight=self.flight,
                order=self.order,
                row=5,
                seat='7'
            )
            ticket.full_clean()

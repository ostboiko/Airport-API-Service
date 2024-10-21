from django.contrib.admin.sites import site
from django.test import TestCase
from Airport.models import User, Airport, Route, AirplaneType, Flight, Crew, Order, Ticket
from Airport.admin import UserAdmin, AirportAdmin, RouteAdmin, AirplaneTypeAdmin, FlightAdmin, CrewAdmin, OrderAdmin, TicketAdmin

class AdminSiteTest(TestCase):

    def test_user_admin_registration(self):
        """Test that User model is registered with the correct configuration in the admin site."""
        self.assertIn(User, site._registry)  # Check if the model is registered
        admin_class = site._registry[User]
        self.assertIsInstance(admin_class, UserAdmin)
        self.assertEqual(admin_class.list_display, ('username', 'first_name', 'last_name', 'email'))
        self.assertEqual(admin_class.search_fields, ('username', 'email'))
        self.assertEqual(admin_class.list_filter, ('first_name', 'last_name'))

    def test_airport_admin_registration(self):
        """Test that Airport model is registered with the correct configuration in the admin site."""
        self.assertIn(Airport, site._registry)
        admin_class = site._registry[Airport]
        self.assertIsInstance(admin_class, AirportAdmin)
        self.assertEqual(admin_class.list_display, ('name', 'closest_big_city'))
        self.assertEqual(admin_class.search_fields, ('name', 'closest_big_city'))
        self.assertEqual(admin_class.list_filter, ('closest_big_city',))

    def test_route_admin_registration(self):
        """Test that Route model is registered with the correct configuration in the admin site."""
        self.assertIn(Route, site._registry)
        admin_class = site._registry[Route]
        self.assertIsInstance(admin_class, RouteAdmin)
        self.assertEqual(admin_class.list_display, ('source', 'destination', 'distance'))
        self.assertEqual(admin_class.search_fields, ('source__name', 'destination__name'))
        self.assertEqual(admin_class.list_filter, ('source', 'destination'))

    def test_airplane_type_admin_registration(self):
        """Test that AirplaneType model is registered with the correct configuration in the admin site."""
        self.assertIn(AirplaneType, site._registry)
        admin_class = site._registry[AirplaneType]
        self.assertIsInstance(admin_class, AirplaneTypeAdmin)
        self.assertEqual(admin_class.list_display, ('name',))
        self.assertEqual(admin_class.search_fields, ('name',))

    def test_flight_admin_registration(self):
        """Test that Flight model is registered with the correct configuration in the admin site."""
        self.assertIn(Flight, site._registry)
        admin_class = site._registry[Flight]
        self.assertIsInstance(admin_class, FlightAdmin)
        self.assertEqual(admin_class.list_display, ('flight_number', 'route', 'airplane', 'total_rows', 'seats_in_row'))
        self.assertEqual(admin_class.search_fields, ('flight_number', 'route__source__name', 'route__destination__name'))
        self.assertEqual(admin_class.list_filter, ('route', 'airplane'))

    def test_crew_admin_registration(self):
        """Test that Crew model is registered with the correct configuration in the admin site."""
        self.assertIn(Crew, site._registry)
        admin_class = site._registry[Crew]
        self.assertIsInstance(admin_class, CrewAdmin)
        self.assertEqual(admin_class.list_display, ('first_name', 'last_name'))
        self.assertEqual(admin_class.search_fields, ('first_name', 'last_name'))
        self.assertEqual(admin_class.list_filter, ('last_name',))

    def test_order_admin_registration(self):
        """Test that Order model is registered with the correct configuration in the admin site."""
        self.assertIn(Order, site._registry)
        admin_class = site._registry[Order]
        self.assertIsInstance(admin_class, OrderAdmin)
        self.assertEqual(admin_class.list_display, ('user', 'created_at', 'order_number'))
        self.assertEqual(admin_class.search_fields, ('user__username', 'order_number'))
        self.assertEqual(admin_class.list_filter, ('created_at', 'user'))

    def test_ticket_admin_registration(self):
        """Test that Ticket model is registered with the correct configuration in the admin site."""
        self.assertIn(Ticket, site._registry)
        admin_class = site._registry[Ticket]
        self.assertIsInstance(admin_class, TicketAdmin)
        self.assertEqual(admin_class.list_display, ('flight', 'row', 'seat', 'order'))
        self.assertEqual(admin_class.search_fields, ('flight__flight_number', 'row', 'seat', 'order__order_number'))
        self.assertEqual(admin_class.list_filter, ('flight', 'row', 'seat'))

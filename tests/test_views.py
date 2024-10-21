from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from Airport.models import Airport, Route
from Airport.serializers import AirportSerializer, RouteSerializer


class AirportViewSetTest(APITestCase):

    def setUp(self):
        self.airport = Airport.objects.create(name="Test Airport", closest_big_city="Test City")
        self.url = reverse('airport-list')  # URL for AirportViewSet (list)

    def test_airport_list(self):
        """Test retrieving list of airports."""
        response = self.client.get(self.url)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_airport_detail(self):
        """Test retrieving a single airport."""
        url = reverse('airport-detail', args=[self.airport.id])  # URL for AirportViewSet (detail)
        response = self.client.get(url)
        serializer = AirportSerializer(self.airport)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_airport_create(self):
        """Test creating a new airport."""
        data = {'name': 'New Airport', 'closest_big_city': 'New City'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 2)
        self.assertEqual(Airport.objects.get(id=response.data['id']).name, 'New Airport')

    def test_airport_update(self):
        """Test updating an existing airport."""
        url = reverse('airport-detail', args=[self.airport.id])
        data = {'name': 'Updated Airport', 'closest_big_city': 'Updated City'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.airport.refresh_from_db()
        self.assertEqual(self.airport.name, 'Updated Airport')

    def test_airport_delete(self):
        """Test deleting an airport."""
        url = reverse('airport-detail', args=[self.airport.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Airport.objects.count(), 0)


class RouteViewSetTest(APITestCase):

    def setUp(self):
        self.airport1 = Airport.objects.create(name="Source Airport", closest_big_city="City1")
        self.airport2 = Airport.objects.create(name="Destination Airport", closest_big_city="City2")
        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=500)
        self.url = reverse('route-list')  # URL for RouteViewSet (list)

    def test_route_list(self):
        """Test retrieving list of routes."""
        response = self.client.get(self.url)
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_route_detail(self):
        """Test retrieving a single route."""
        url = reverse('route-detail', args=[self.route.id])  # URL for RouteViewSet (detail)
        response = self.client.get(url)
        serializer = RouteSerializer(self.route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class FlightViewSetTest(APITestCase):

    def setUp(self):
        self.airport1 = Airport.objects.create(name="Source Airport", closest_big_city="City1")
        self.airport2 = Airport.objects.create(name="Destination Airport", closest_big_city="City2")
        self.route = Route.objects.cr

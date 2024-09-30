import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class User(models.Model):
    username = models.CharField(max_length=60)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)

    def __str__(self):
        return self.username


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (Closest big city: {self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, related_name="routes_from", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="routes_to", on_delete=models.CASCADE)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}, {self.distance} km"


# def movie_image_file_path(instance, filename):
#     _, extension = os.path.splitext(filename)
#     filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
#
#     return os.path.join("uploads/movies/", filename)


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)
    # image = models.ImageField(null=True,)

    def __str__(self):
        return f"name"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Flight {self.flight_number} on {self.airplane} {self.route}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.CharField(max_length=3)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

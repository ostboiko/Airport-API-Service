import os
import pathlib
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

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Closest big city: {self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, related_name="routes_from", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="routes_to", on_delete=models.CASCADE)
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}, {self.distance} km"


def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "upload/airplanes/",
        f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
    )


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to="???") # TODO refactore!!

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"name"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=10)
    total_rows = models.IntegerField(default=30)
    seats_in_row = models.IntegerField(default=6)

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
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.CharField(max_length=3)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    @staticmethod
    def validate_ticket(row, seat, flight, error_to_raise):
        try:
            row = int(row)  # Перетворюємо рядок на ціле число
        except ValueError:
            raise error_to_raise({"row": "Row number must be an integer."})

        try:
            seat = int(seat)  # Перетворюємо місце на ціле число (якщо це число)
        except ValueError:
            raise error_to_raise({"seat": "Seat number must be an integer."})

        for ticket_attr_value, ticket_attr_name, flight_attr_name in [
            (row, "row", "total_rows"),  # Перевірка для кількості рядів
            (seat, "seat", "seats_in_row"),  # Перевірка для кількості місць у ряду
        ]:
            count_attrs = getattr(flight, flight_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} number must be in available range: "
                                          f"(1, {flight_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight,  # Використовуємо flight для перевірки
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()  # Викликаємо перевірку перед збереженням
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

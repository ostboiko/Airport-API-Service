from django.contrib import admin
from .models import User, Airport, Route, AirplaneType, Flight, Crew, Order, Ticket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'last_name')


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'closest_big_city')
    search_fields = ('name', 'closest_big_city')
    list_filter = ('closest_big_city',)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'distance')
    search_fields = ('source__name', 'destination__name')
    list_filter = ('source', 'destination')


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'route', 'airplane', 'total_rows', 'seats_in_row')
    search_fields = ('flight_number', 'route__source__name', 'route__destination__name')
    list_filter = ('route', 'airplane')


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('last_name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'order_number')
    search_fields = ('user__username', 'order_number')
    list_filter = ('created_at', 'user')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('flight', 'row', 'seat', 'order')
    search_fields = ('flight__flight_number', 'row', 'seat', 'order__order_number')
    list_filter = ('flight', 'row', 'seat')

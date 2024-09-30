from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, RouteViewSet, FlightViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'airports', AirportViewSet, basename='airport')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = router.urls

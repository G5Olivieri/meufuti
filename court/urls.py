from django.urls import path
from court.views import CourtsView, CourtByIdView, CourtCreateView, CourtDeleteView, CourtUpdateView, \
    CourtReserveView, CourtReservationsView, CourtMyView

urlpatterns = [
    path("", CourtsView.as_view(), name="court.index"),
    path("create", CourtCreateView.as_view(), name="court.create"),
    path("my", CourtMyView.as_view(), name="court.my"),
    path("<uuid:id>", CourtByIdView.as_view(), name="court.get_by_id"),
    path("<uuid:id>/delete", CourtDeleteView.as_view(), name="court.delete"),
    path("<uuid:id>/update", CourtUpdateView.as_view(), name="court.update"),
    path("<uuid:id>/reserve", CourtReserveView.as_view(), name="court.reserve"),
    path("<uuid:id>/reservation", CourtReservationsView.as_view(), name="court.reservation.index"),
]

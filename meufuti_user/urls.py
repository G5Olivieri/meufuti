from django.urls import path

from meufuti_user.views import UserReservationsView

urlpatterns = [
    path('reservations', UserReservationsView.as_view(), name='user.reservation.index'),
]

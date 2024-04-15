from django.contrib import admin

from court.models import Court, CourtImage, Reservation

# Register your models here.
admin.site.register([Court, CourtImage, Reservation])

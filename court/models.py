import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Court(TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    street = models.CharField(max_length=256)
    neighborhood = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=32)
    number = models.CharField(max_length=32)
    reference_point = models.CharField(max_length=256, null=True, blank=True)

    facilities = ArrayField(models.TextField(null=True, blank=True))
    availability_weeks = ArrayField(models.TextField(null=True, blank=True), size=7)
    availability_times = ArrayField(models.TextField(null=True, blank=True), size=24)

    single_price = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)


class CourtImage(TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_TYPES = (
        ("Thumbnail", "thumbnail"),
        ("Banner", "banner"),
        ("Other", "other")
    )
    type = models.CharField(max_length=256)
    image = models.ImageField(upload_to="upload/")
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="images")


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()

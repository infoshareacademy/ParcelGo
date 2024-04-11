from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from datetime import datetime

User = get_user_model()


class ParcelLocker(models.Model):
    locker_number = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)  # Pojemność paczkomatu (ilość paczek, którą może pomieścić)

    def __str__(self):
        return f"{self.locker_number} - {self.city} {self.street} {self.street_number}"


class Parcel(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('In delivery', 'In delivery'),
        ('Delivered', 'Delivered'),
        ('Received', 'Received')
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_parcel_locker = models.ForeignKey(ParcelLocker, on_delete=models.CASCADE)
    tracking_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient_first_name = models.CharField(max_length=100)
    recipient_last_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)

    shipping_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=DELIVERY_STATUS_CHOICES, default='In delivery')
    is_approved = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    pickup_code = models.CharField(max_length=100, default="", blank=True)
    received_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.pickup_code}"

    def mark_as_received(self):
        self.status = 'Received'
        self.received_date = timezone.make_aware(datetime.now(), timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M')
        self.save()

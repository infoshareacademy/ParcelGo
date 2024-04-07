from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class ParcelLocker(models.Model):
    locker_number = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)  # Pojemność paczkomatu (ilość paczek, którą może pomieścić)

    def __str__(self):
        return self.locker_number


class Parcel(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('In delivery', 'In delivery'),
        ('Delivered', 'Delivered'),
        ('Failed delivery', 'Failed delivery'),
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

    def __str__(self):
        return str(self.tracking_number)

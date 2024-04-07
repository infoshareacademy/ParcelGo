from django.db import models

class ParcelLocker(models.Model):
    locker_number = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)  # Pojemność paczkomatu (ilość paczek, którą może pomieścić)

    def __str__(self):
        return self.locker_number



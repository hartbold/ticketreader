import datetime
from time import timezone
from django.db import models
from django.utils.timezone import now


# Create your models here.


class Storage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):

    UNIT_KILO   = "KL"
    UNIT_GRAM   = "GR"
    UNIT_UNIT   = "UN"
    UNIT_PACK   = "PK"
    UNIT_LITRE  = "LI"
    UNIT_OTHER  = "OT"

    UNIT_CHOICES = [
        (UNIT_KILO, 'Kilos'),
        (UNIT_GRAM, 'Grams'),
        (UNIT_UNIT, 'Unitats'),
        (UNIT_PACK, 'Paquets'),
        (UNIT_LITRE, 'Litres'),
        (UNIT_OTHER, 'Altres'),
    ]

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default=UNIT_OTHER)

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total = models.BinaryField()
    processedText = models.CharField(max_length=5000)
    uploaded_at = models.DateTimeField(default=now)


    def __str__(self) -> str:
        return self.storage + self.uploaded_at

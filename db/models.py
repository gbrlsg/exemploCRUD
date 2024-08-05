from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=14)
    creationDate =  models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self): return self.name

class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        UTILITY = "UTL", _("Utilitário")
        LIGHT_DUTY_TRUCK = "LDT", _("VUC")
        SINGLE_UNITY_TRUCK = "SUT", _("Toco")
        TRUCK = "TRK", _("Truck")
        TWIN_STEER_TRUCK = "TST", _("Bitruck")
        TRACTOR = "TCR", _("Cavalo mecânico simples")
        SEMITRAILER = "STR", _("Carreta")

    client = models.ForeignKey(Client,models.CASCADE,blank=True,null=True)
    plate = models.CharField(max_length=7)
    serialNumber = models.CharField(max_length=10)
    vehicleType = models.CharField(max_length=3,choices=VehicleType)
    creationDate =  models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self): return self.plate

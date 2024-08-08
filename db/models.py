from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Onixsat(models.Model):
    mid = models.BigIntegerField(blank=True, null=True)
    veiid = models.CharField(max_length=11, blank=True, null=True)
    lat = models.CharField(max_length=30, blank=True, null=True)
    lon = models.CharField(max_length=30, blank=True, null=True)
    dt = models.DateTimeField(blank=True, null=True)
    vel = models.BigIntegerField(blank=True, null=True)
    odm = models.BigIntegerField(blank=True, null=True)
    rua = models.CharField(max_length=150, blank=True, null=True)
    mun = models.CharField(max_length=150, blank=True, null=True)
    uf = models.CharField(max_length=5, blank=True, null=True)
    evt4 = models.CharField(max_length=50, blank=True, null=True)
    evt5 = models.CharField(max_length=45, blank=True, null=True)
    evt14 = models.CharField(max_length=50, blank=True, null=True)
    evt16 = models.CharField(max_length=45, blank=True, null=True)
    evt17 = models.CharField(max_length=45, blank=True, null=True)
    evt28 = models.CharField(max_length=45, blank=True, null=True)
    evt29 = models.CharField(max_length=45, blank=True, null=True)
    evt30 = models.CharField(max_length=45, blank=True, null=True)
    evt31 = models.CharField(max_length=45, blank=True, null=True)
    evt84 = models.CharField(max_length=45, blank=True, null=True)
    evt98 = models.CharField(max_length=45, blank=True, null=True)
    evtg = models.CharField(max_length=45, blank=True, null=True)
    dmac = models.TextField(blank=True, null=True)
    st1 = models.IntegerField(blank=True, null=True)
    pr = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    ativo_ocorrencia = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'onixsat'
        app_label =  'db'

class MockPosition(models.Model):
    veiid = models.CharField(max_length=11, blank=True, null=True)
    lat = models.CharField(max_length=30, blank=True, null=True)
    lon = models.CharField(max_length=30, blank=True, null=True)

class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        UTILITY = "UTL", _("Utilitário")
        LIGHT_DUTY_TRUCK = "LDT", _("VUC")
        SINGLE_UNITY_TRUCK = "SUT", _("Toco")
        TRUCK = "TRK", _("Truck")
        TWIN_STEER_TRUCK = "TST", _("Bitruck")
        TRACTOR = "TCR", _("Cavalo mecânico simples")
        SEMITRAILER = "STR", _("Carreta")

    client = models.ForeignKey('Client',null=True,on_delete=models.SET_NULL)
    position = models.ForeignKey('MockPosition',null=True,on_delete=models.SET_NULL)
    plate = models.CharField(max_length=7)
    serialNumber = models.CharField(max_length=10)
    vehicleType = models.CharField(max_length=3,choices=VehicleType)
    creationDate =  models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now=True)

    def __str__(self): return self.plate

class Area(models.Model):
    
    name = models.CharField(max_length=150)
    perimeter = models.CharField(max_length=100)
    vehicles_within = models.ManyToManyField('Vehicle')

    def __str__(self) -> str:
        return f"Name:{self.name}\n{self.perimeter}"

class Client(models.Model):

    name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=14)
    associated_areas = models.ManyToManyField('Area') 
    created_at =  models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("{}\n"*4).format(
            f"Name: {self.name}",
            f"CNPJ: {self.cnpj}",
            f"Creation: {self.created_at}",    
            f"Modification: {self.modified_at}",
        )

    def area_structure(self) -> str:
        struct_for_print: List[str] = [f"{self.name} (Client):"]

        for area in self.associated_areas.all():
            struct_for_print.append(f" {area.name} (Area):")
        
        return '\n'.join(struct_for_print)
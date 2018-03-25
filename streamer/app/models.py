from __future__ import unicode_literals

from django.db import models


# Transponders table
class Transponders(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    config = models.TextField(default="hello")

    def __str__(self):
        return self.name


class Satellites(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    config = models.TextField(default="hello")

    def __str__(self):
        return self.name


class InterfaceConfiguration(models.Model):
    #interface_id        =  models.ForeignKey(InterfaceProperties)
    sat_name            = models.CharField(max_length=200, null=False,)
    delivery_system     = models.CharField(max_length=5, null=False,)
    frequency           = models.PositiveIntegerField()
    symbole_rate        = models.PositiveIntegerField()
    polarisation        = models.CharField(max_length=10)
    modulation          = models.CharField(max_length=10)
    fec                 = models.CharField(max_length=10)
    rolloff             = models.CharField(max_length=10)
    pilot               = models.CharField(max_length=10)
    lnb_type            = models.CharField(max_length=10)
    lnb_lof_standard    = models.PositiveIntegerField()
    lnb_slof            = models.PositiveIntegerField()
    lnb_lof_low         = models.PositiveIntegerField()
    lnb_lof_high        = models.PositiveIntegerField()

    def __str__(self):
        return self.sat_name


class InterfaceProperties(models.Model):

    interface_id = models.DecimalField(max_digits=10,decimal_places=2, null=False)
    interface_name = models.CharField(max_length=100)

    def __str__(self):
        return self.interface_name


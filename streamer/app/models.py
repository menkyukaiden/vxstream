from __future__ import unicode_literals

from django.db import models


class Satellites(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    config = models.TextField(default="from_user")
    delivery_system     = models.CharField(max_length=5, null=True)
    frequency           = models.PositiveIntegerField(null=True, unique=True)
    symbole_rate        = models.PositiveIntegerField(null=True)
    polarisation        = models.CharField(max_length=10, null=True)
    modulation          = models.CharField(max_length=10, null=True)
    fec                 = models.CharField(max_length=10, null=True)
    rolloff             = models.CharField(max_length=10, null=True)
    pilot               = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = 'Satellites'

    def __str__(self):
        return self.name


class InterfaceConfiguration(models.Model):
    #id = models.ForeignKey(Satellites)
    sat_name            = models.CharField(max_length=200, null=False,unique=True)
    lnb_type            = models.CharField(max_length=10)
    lnb_lof_standard    = models.PositiveIntegerField()
    lnb_slof            = models.PositiveIntegerField()
    lnb_lof_low         = models.PositiveIntegerField()
    lnb_lof_high        = models.PositiveIntegerField()

    def __str__(self):
        return self.sat_name

    class Meta:
        verbose_name_plural = 'InterfaceConfigurations'


class InterfaceProprieties(models.Model):

    interface_name = models.CharField(max_length=100)

    #configuration = models.ForeignKey(InterfaceConfiguration)

    class Meta:
        verbose_name_plural = 'InterfaceProprieties'

    def __str__(self):
        return self.interface_name


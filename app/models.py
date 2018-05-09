# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.
class LocalTime(models.Model):
    time = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.time = timezone.now()
        self.save()

    def __str__(self):
        return self.time.date().__str__() + " - " + self.time.time().__str__()

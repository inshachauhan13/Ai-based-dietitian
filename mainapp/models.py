from django.db import models

# Create your models here.

class records_users(models.Model):
        name = models.CharField(max_length=200)
        age = models.IntegerField(default=0)
        weight = models.FloatField(default=0.0)
        height = models.FloatField(default=0.0)
        gender = models.CharField(max_length=1)
        a_l = models.IntegerField(default=1)
        bmi = models.FloatField(default=0.0)
        bmr = models.FloatField(default=0.0)
        ctmw = models.FloatField(default=0.0)
        
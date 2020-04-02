from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class ShockList(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=200)
    def __str__(self):
        return self.name


class shock_trade(models.Model):
    code=models.CharField(max_length=200,default=0)
    shock_name=models.CharField(max_length=200,default=0)
    num=models.IntegerField(default=0)
    cost=models.FloatField(default=0)
    code_str=models.CharField(max_length=200,default=0)
    now_price=models.FloatField(default=0)
    profit=models.FloatField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

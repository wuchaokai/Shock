from django.contrib import admin
from .models import ShockList
from .models import shock_trade
# Register your models here.

admin.site.register(ShockList)
admin.site.register(shock_trade)
from django.contrib import admin
from django.contrib.auth.admin import Group

from . import models


admin.site.unregister(Group)
admin.site.register(models.DeliveryBatch)
admin.site.register(models.ExcelDocument)
admin.site.register(models.Product)

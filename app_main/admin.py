from django.contrib import admin
from django.contrib.auth.admin import Group

from . import models

admin.site.site_header = "Cargo Star | Админ панель"  # Title in the admin home page
admin.site.site_title = "Админка Cargo Start"  # Title in the browser tab
admin.site.index_title = "Добро пожаловать в административную панель Cargo Star"  # Subtitle on the admin home page

admin.site.unregister(Group)
admin.site.register(models.DeliveryBatch)
admin.site.register(models.ExcelDocument)
admin.site.register(models.Product)

from django.contrib import admin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin, TabularInline

from .models import (
    DeliveryBatch,
    Product,
    ExcelDocument,
    SupplierExcelDocument,
    Supplier,
)

from . import models

admin.site.site_header = "Cargo Star | Админ панель"
admin.site.site_title = "Админка Cargo Start"
admin.site.index_title = "Добро пожаловать в административную панель Cargo Star"

admin.site.unregister(Group)


class SupplierExcelDocumentTabularAdmin(TabularInline):
    model = models.SupplierExcelDocument
    extra = 1


class ExcelDocumentTabularAdmin(TabularInline):
    model = models.ExcelDocument
    extra = 1


@admin.register(models.SupplierExcelDocumentsParent)
class SupplierExcelDocumentsParentAdmin(admin.ModelAdmin):
    inlines = [SupplierExcelDocumentTabularAdmin]


@admin.register(models.ProductExcelDocumentsParent)
class ProductExcelDocumentsParentAdmin(admin.ModelAdmin):
    inlines = [ExcelDocumentTabularAdmin]


@admin.register(DeliveryBatch)
class DeliveryBatchAdmin(ModelAdmin):
    list_display = (
        "manifest_register_number",
        "title",
        "sender_name",
        "send_date",
        "total_products",
        "total_recipients",
        "total_weight",
        "total_price",
    )
    search_fields = ("title", "manifest_register_number", "sender_name")
    list_filter = ("send_date",)
    ordering = ("-send_date",)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "product_id",
        "product_name",
        "recipient_fullname",
        "delivery_batch",
        "quantity",
        "price",
        "currency",
    )
    search_fields = (
        "product_id",
        "product_name",
        "recipient_fullname",
        "recipient_phonenumber",
        "recipient_pinfl",
    )
    list_filter = ("delivery_batch", "currency")
    fieldsets = (
        ("Basic Info", {
            "fields": ("product_id", "product_name", "invoice", "awb", "sticker", "delivery_batch")
        }),
        ("Pricing", {
            "fields": ("price", "quantity", "currency")
        }),
        ("Weight & Quantity", {
            "fields": ("netto", "brutto", "box_number")
        }),
        ("Recipient Info", {
            "fields": (
                "recipient_fullname",
                "recipient_passport",
                "recipient_pinfl",
                "recipient_birthdate",
                "recipient_country_code",
                "recipient_city_name",
                "recipient_address",
                "recipient_phonenumber"
            )
        }),
        ("Other", {
            "fields": ("tn_ved", "shk")
        })
    )


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = (
        "sender",
        "date",
        "country",
        "zone",
        "what_is_inside",
        "weight",
        "price",
        "final_price",
    )
    search_fields = ("sender", "number", "country")
    list_filter = ("date", "country", "zone", "payment_type")
    ordering = ("-date",)

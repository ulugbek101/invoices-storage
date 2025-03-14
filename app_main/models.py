from uuid import uuid4

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class DeliveryBatch(models.Model):
    title = models.CharField(max_length=255)
    manifest_register_number = models.IntegerField()
    sender_name = models.CharField(max_length=255)
    send_date = models.DateField()
    total_products = models.IntegerField()
    total_recipients = models.IntegerField()
    total_weight = models.IntegerField()
    total_price = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"
        ordering = ["-send_date", "sender_name"]

    def __str__(self):
        return f"{self.manifest_register_number} - {self.sender_name} {self.send_date}"


class Product(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    delivery_batch = models.ForeignKey(to=DeliveryBatch, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255)
    invoice = models.CharField(max_length=255)
    awb = models.CharField(max_length=255)
    sticker = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    netto = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    brutto = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    tn_ved = models.CharField(max_length=255)
    shk = models.CharField(max_length=255)
    recipient_fullname = models.CharField(max_length=255)
    recipient_passport = models.CharField(max_length=7)
    recipient_pinfl = models.CharField(max_length=14)
    recipient_birthdate = models.CharField(max_length=10)
    recipient_country_code = models.CharField(max_length=2)
    recipient_city_name = models.CharField(max_length=255)
    recipient_address = models.CharField(max_length=255)
    recipient_phonenumber = PhoneNumberField()
    box_number = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.product_id

    @property
    def total_price(self):
        return self.price * self.quantity


class ExcelDocument(models.Model):
    document = models.FileField(upload_to="documents/")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Excel документ"
        verbose_name_plural = "Excel документы"

    def __str__(self):
        return f"{self.created}"

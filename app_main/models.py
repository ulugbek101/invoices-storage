from uuid import uuid4

from django.db import models


class SupplierExcelDocumentsParent(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Документы поставщиков"
        verbose_name_plural = "Доукументы поставщиков"
        ordering = ["created"]

    def __str__(self):
        return self.created


class ProductExcelDocumentsParent(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Документы товаров"
        verbose_name_plural = "Документы товаров"
        ordering = ["created"]

    def __str__(self):
        return self.created


class SupplierExcelDocument(models.Model):
    """
    Документ содержащий список поставщиков FedEx, ...
    """
    parent = models.ForeignKey(to=SupplierExcelDocumentsParent, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to="documents/suppliers/", null=True, verbose_name="Документ поставщиков")
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Excel документ поставщика"
        verbose_name_plural = "Excel документы поставщиков"
        ordering = ["created"]

    def __str__(self):
        return self.document


class ExcelDocument(models.Model):
    """
    Документ содержащий список продуктов
    """
    parent = models.ForeignKey(to=ProductExcelDocumentsParent, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to="documents/products/", null=True, verbose_name="Документ товаров")
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Excel документ для товара"
        verbose_name_plural = "Excel документы для товаров"
        ordering = ["created"]

    def __str__(self):
        return f"{self.created}"


class DeliveryBatch(models.Model):
    title = models.CharField(max_length=255, null=True)
    manifest_register_number = models.CharField(max_length=255, null=True)
    sender_name = models.CharField(max_length=255, null=True)
    send_date = models.CharField(max_length=255, null=True)
    total_products = models.CharField(max_length=255, null=True)
    total_recipients = models.CharField(max_length=255, null=True)
    total_weight = models.CharField(max_length=255, null=True)
    total_price = models.CharField(max_length=255, null=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Поставка товара"
        verbose_name_plural = "Поставки товаров"
        ordering = ["created"]

    def __str__(self):
        return f"{self.manifest_register_number} - {self.sender_name} {self.send_date}"


class Product(models.Model):
    delivery_batch = models.ForeignKey(to=DeliveryBatch, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255, null=True)
    invoice = models.CharField(max_length=255, null=True)
    awb = models.CharField(max_length=255, null=True)
    sticker = models.CharField(max_length=255, null=True)
    product_name = models.CharField(max_length=255, null=True)
    netto = models.CharField(max_length=255, null=True)
    brutto = models.CharField(max_length=255, null=True)
    quantity = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255, null=True)
    tn_ved = models.CharField(max_length=255, null=True)
    shk = models.CharField(max_length=255, null=True)
    recipient_fullname = models.CharField(max_length=255, null=True)
    recipient_passport = models.CharField(max_length=255, null=True)
    recipient_pinfl = models.CharField(max_length=255, null=True)
    recipient_birthdate = models.CharField(max_length=255, null=True)
    recipient_country_code = models.CharField(max_length=255, null=True)
    recipient_city_name = models.CharField(max_length=255, null=True)
    recipient_address = models.CharField(max_length=255, null=True)
    recipient_phonenumber = models.CharField(max_length=255, null=True)
    box_number = models.CharField(max_length=255, null=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["created"]

    def __str__(self):
        return self.product_id

    @property
    def total_price(self):
        try:
            total_price = self.price * int(self.quantity)
        except:
            total_price = "Calc. Error"
        return total_price


class Supplier(models.Model):
    date = models.CharField(max_length=255, null=True)
    sender = models.CharField(max_length=255, null=True)
    number = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=50, null=True)
    zone = models.CharField(max_length=255, null=True)
    what_is_inside = models.CharField(max_length=255, null=True)
    weight = models.CharField(max_length=255, null=True)
    payment_type = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=255, null=True)
    additional_percent = models.CharField(max_length=255, null=True)
    final_price = models.CharField(max_length=255, null=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return f"{self.sender} - {self.date}"

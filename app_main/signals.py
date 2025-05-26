from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from django.dispatch import receiver
from django.db.models.signals import post_save

from openpyxl import load_workbook

from .models import ExcelDocument, DeliveryBatch, Product, SupplierExcelDocument, Supplier


@receiver(post_save, sender=ExcelDocument)
def save_and_populate_document(sender, instance, created, **kwargs):
    # if created:
    file = instance.document
    wb = load_workbook(file)
    sheet = wb.active

    title = sheet.cell(row=1, column=1)
    manifest_register_number = sheet.cell(row=2, column=1).value.split("№")[-1]
    total_products = sheet.cell(row=1, column=2).value.split()[-1]
    total_recipients = sheet.cell(row=2, column=2).value.split()[-1]
    sender_name = sheet.cell(row=3, column=1).value.lower().split("отправитель")[-1].strip().upper()
    total_weight = sheet.cell(row=3, column=2).value
    total_price = sheet.cell(row=4, column=2).value
    send_date = datetime.strptime(sheet.cell(row=4, column=1).value.split()[-1], "%d.%m.%Y").date()

    delivery_batch, delivery_batch_created = DeliveryBatch.objects.get_or_create(
        title=title,
        manifest_register_number=manifest_register_number,
        total_products=total_products,
        total_recipients=total_recipients,
        sender_name=sender_name,
        total_weight=total_weight,
        total_price=total_price,
        send_date=send_date,
    )

    for row in sheet.iter_rows(min_row=6, values_only=True):
        if row[0] is None:
            break

        product, product_created = Product.objects.get_or_create(
            delivery_batch=delivery_batch,
            product_id=row[0],
            invoice=row[1],
            awb=row[2],
            sticker=row[3],
            product_name=row[4],
            netto=row[6],
            brutto=row[7],
            quantity=row[8],
            price=row[9],
            currency=row[10],
            tn_ved=row[12],
            shk=row[13],
            recipient_fullname=row[14].title(),
            recipient_passport=row[15],
            recipient_pinfl=row[16],
            recipient_birthdate=str(row[17])[:11],
            recipient_country_code=row[18],
            recipient_city_name=row[19],
            recipient_address=row[20],
            recipient_phonenumber=row[21],
            box_number=row[22]
        )


@receiver(post_save, sender=SupplierExcelDocument)
def save_and_populate_suppliers(sender, instance, created, **kwargs):
    file = instance.document
    wb = load_workbook(file)

    # Ensure "FedEx" sheet is selected
    sheet_name = "FedEx"
    if sheet_name not in wb.sheetnames:
        return  # Exit if the sheet doesn't exist

    sheet = wb[sheet_name]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row[1]:  # Stop if no more valid data
            break

        Supplier.objects.create(
            date=row[1] if row[1] else None,
            sender=row[2].strip().title() if isinstance(row[2], str) else None,
            number=row[3] if row[3] else None,
            country=row[4].strip().title() if isinstance(row[4], str) else None,
            zone=row[5].strip().upper() if isinstance(row[5], str) else None,
            what_is_inside=row[6].strip().upper() if isinstance(row[6], str) else None,
            weight=Decimal(row[7]) if row[7] else None,
            payment_type=row[8].strip().upper() if isinstance(row[8], str) else None,
            price=row[9] if row[9] else "",
            additional_percent=row[10].replace("%", "") if isinstance(row[10], str) else "",
            # final_price=str(round(
            #     (Decimal(row[10]) + Decimal(row[10]) * Decimal(0.12)) * Decimal(row[10]) + Decimal(row[10]) + Decimal(
            #         row[10]) * Decimal(0.12), 2)) if row[10] else None  # (J31+J31*12%)*K31+J31+J31*12%
        )

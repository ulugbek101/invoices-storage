import os
import logging
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from openpyxl import load_workbook
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_main.models import (
    ProductExcelDocumentsParent,
    Product,
    Supplier,
    DeliveryBatch
)

logger = logging.getLogger(__name__)

def save_and_populate_products(sheet, document):
    for row in sheet.iter_rows(min_row=9, values_only=True):
        title = str(row[2]).strip() if row[2] else None
        supplier_name = str(row[6]).strip() if row[6] else None
        weight = None
        try:
            weight = Decimal(row[7]) if row[7] else None
        except (InvalidOperation, TypeError) as e:
            logger.warning(f"Invalid weight value '{row[7]}': {e}")

        if title and supplier_name:
            supplier, _ = Supplier.objects.get_or_create(name=supplier_name)
            try:
                Product.objects.get_or_create(
                    title=title,
                    supplier=supplier,
                    weight=weight,
                    document=document
                )
            except Exception as e:
                logger.error(f"Failed to create Product '{title}': {e}")

def save_and_populate_suppliers(sheet):
    for row in sheet.iter_rows(min_row=9, values_only=True):
        name = str(row[6]).strip() if row[6] else None
        if name:
            try:
                Supplier.objects.get_or_create(name=name)
            except Exception as e:
                logger.error(f"Failed to create Supplier '{name}': {e}")

@receiver(post_save, sender=ProductExcelDocumentsParent)
def save_and_populate_document(sender, instance, created, **kwargs):
    if not created:
        return

    file_path = instance.file.path
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
    except Exception as e:
        logger.error(f"Failed to load Excel file: {e}")
        return

    # Parse values from Excel
    try:
        raw_value = str(sheet.cell(row=2, column=1).value)
        manifest_register_number = raw_value.split("№")[-1].strip()
    except Exception as e:
        logger.warning(f"Failed to parse manifest_register_number: {e}")
        manifest_register_number = ""

    try:
        total_products = int(sheet.cell(row=3, column=1).value)
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to parse total_products: {e}")
        total_products = 0

    try:
        send_date_raw = sheet.cell(row=4, column=1).value
        send_date_str = str(send_date_raw).split()[-1]
        send_date = datetime.strptime(send_date_str, "%d.%m.%Y").date()
    except Exception as e:
        logger.warning(f"Failed to parse send_date: {e}")
        send_date = date.today()

    try:
        delivery_batch, _ = DeliveryBatch.objects.get_or_create(
            title=f"Batch {manifest_register_number}",
            manifest_register_number=manifest_register_number,
            total_products=total_products,
            send_date=send_date
        )
        instance.delivery_batch = delivery_batch
        instance.save(update_fields=["delivery_batch"])
    except Exception as e:
        logger.error(f"Failed to create DeliveryBatch: {e}")
        return

    try:
        with transaction.atomic():
            save_and_populate_suppliers(sheet)
            save_and_populate_products(sheet, instance)
    except Exception as e:
        logger.error(f"Failed to populate data from Excel: {e}")

from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

from openpyxl import load_workbook

from .models import ExcelDocument, DeliveryBatch, Document


@receiver(signal=post_save, sender=ExcelDocument)
def save_and_populate_document(sender, instance, created, **kwargs):
    if created:
        file = instance.document
        wb = load_workbook(file)
        sheet = wb.active

        title = sheet.cell(row=1, column=1).value.strip().capitalize()
        manifest_register_number = sheet.cell(row=2, column=1).value.split("№")[-1].strip()
        total_products = int(sheet.cell(row=1, column=2).value.split()[-1])
        total_recipients = int(sheet.cell(row=2, column=2).value.split()[-1])
        sender_name = sheet.cell(row=3, column=1).value.lower().split("отправитель")[-1].strip().upper()
        total_weight = float(sheet.cell(row=3, column=2).value.lower().replace("кг", "").replace("kg", "").replace(",", ".").split()[-1])
        total_price = float(sheet.cell(row=4, column=2).value.lower().replace("руб", "").split("стоимость")[-1].strip().replace(",", ".").replace(" ", ""))
        send_date = datetime.strptime(sheet.cell(row=4, column=1).value.split()[-1], "%d.%m.%Y").date()

        print(sheet.cell(row=4, column=2).value.lower().replace(",", ".").replace("руб", "").split()[-1].strip())

        delivery_batch = DeliveryBatch.objects.create(
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

            Document.objects.create(
                tracking_number=row[0],
                invoice_number=row[1],
                awb=row[2],
                shipment_id=row[3],
                product_name=row[4],
                net_weight=row[5],
                gross_weight=row[6],
                quantity=int(row[7]),
                unit_price=float(row[8]),
                total_price=float(row[9]),
                customs_code=row[10],
                barcode=row[11],
                recipient_name=row[12],
                passport_number=row[13],
                pinfl=row[14],
                recipient_address=row[15],
                phone_number=row[16],
                box_number=row[17],
                birth_date=datetime.strptime(row[18], "%d.%m.%Y").date(),
            )

            # TODO: for cycle is not checked to work properly, i just copied and pasted


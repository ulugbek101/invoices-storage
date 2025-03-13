from datetime import datetime, date
from django.dispatch import receiver
from django.db.models.signals import post_save

from openpyxl import load_workbook

from .models import ExcelDocument, DeliveryBatch, Product


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

        # print(sheet.cell(row=4, column=2).value.lower().replace(",", ".").replace("руб", "").split()[-1].strip())

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

            Product.objects.create(
                delivery_batch=delivery_batch,
                product_id=row[0],
                invoice=row[1],
                awb=row[2],
                sticker=row[3],
                product_name=row[4],
                netto=float(row[6]),
                brutto=float(row[7]),
                quantity=int(row[8]),
                price=float(row[9]),
                currency=row[10],
                tn_ved=row[12],
                shk=row[13],
                recipient_fullname=row[14].title(),
                recipient_passport=row[15],
                recipient_pinfl=row[16],
                recipient_birthdate=str(row[17])[:11],
                recipient_country_code=row[18],
                recipient_city_name=row[19],
                recipient_address=[20],
                recipient_phonenumber=row[21],
                box_number=row[22]
            )

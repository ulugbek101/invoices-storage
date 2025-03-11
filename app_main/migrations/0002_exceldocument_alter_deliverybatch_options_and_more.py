# Generated by Django 5.1.7 on 2025-03-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='deliverybatch',
            options={'ordering': ['-send_date', 'sender_name'], 'verbose_name': 'Поставка', 'verbose_name_plural': 'Поставки'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]

# Generated by Django 5.1.7 on 2025-03-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0004_alter_exceldocument_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='additional_percent',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='final_price',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='payment_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='price',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='sender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='what_is_inside',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='zone',
            field=models.CharField(max_length=1, null=True),
        ),
    ]

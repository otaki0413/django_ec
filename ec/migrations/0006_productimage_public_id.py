# Generated by Django 4.2.5 on 2024-09-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ec", "0005_alter_productimage_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="productimage",
            name="public_id",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

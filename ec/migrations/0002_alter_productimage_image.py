# Generated by Django 4.2.5 on 2024-09-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ec", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(blank=True, upload_to="image/"),
        ),
    ]

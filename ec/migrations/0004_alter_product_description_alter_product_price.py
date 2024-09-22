# Generated by Django 4.2.5 on 2024-09-14 05:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ec", "0003_alter_productimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, default="", verbose_name="説明"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(default=0, verbose_name="値段"),
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0003_translatedmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="translatedmodel",
            name="not_translated",
            field=models.TextField(default="A Default Value"),
        ),
    ]

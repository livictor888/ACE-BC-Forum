# Generated by Django 4.1.2 on 2023-03-23 21:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0005_subscription"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Subscription",
        ),
    ]

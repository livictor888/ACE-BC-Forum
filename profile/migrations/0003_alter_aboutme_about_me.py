# Generated by Django 4.1.2 on 2022-11-24 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_alter_aboutme_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutme',
            name='about_me',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
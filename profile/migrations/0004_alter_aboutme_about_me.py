# Generated by Django 4.1.2 on 2022-11-24 22:42

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_alter_aboutme_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutme',
            name='about_me',
            field=tinymce.models.HTMLField(blank=True, default=''),
        ),
    ]
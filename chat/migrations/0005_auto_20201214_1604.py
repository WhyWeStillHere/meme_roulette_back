# Generated by Django 3.1.3 on 2020-12-14 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201213_0900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='image',
            new_name='image_url',
        ),
    ]

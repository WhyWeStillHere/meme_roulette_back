# Generated by Django 3.1.3 on 2020-12-13 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('messeger_1_id', models.IntegerField()),
                ('messeger_2_id', models.IntegerField()),
            ],
        ),
    ]

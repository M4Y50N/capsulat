# Generated by Django 4.0.6 on 2022-07-30 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_room_date_control'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='date_control',
        ),
    ]

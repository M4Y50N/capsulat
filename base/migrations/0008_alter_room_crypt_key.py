# Generated by Django 4.0.4 on 2022-07-23 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_room_crypt_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='crypt_key',
            field=models.CharField(default='capsulat', max_length=23),
        ),
    ]

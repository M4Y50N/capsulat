# Generated by Django 4.0.6 on 2022-07-26 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_room_created_in_alter_room_crypt_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_join',
            field=models.CharField(default='room', max_length=20),
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_room_created_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_in',
            field=models.TextField(blank=True, null=True),
        ),
    ]
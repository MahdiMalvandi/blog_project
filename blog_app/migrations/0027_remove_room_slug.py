# Generated by Django 4.2.7 on 2023-12-27 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0026_message_room_delete_ticket_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='slug',
        ),
    ]

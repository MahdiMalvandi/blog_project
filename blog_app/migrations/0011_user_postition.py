# Generated by Django 4.2.7 on 2023-11-24 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0010_comment_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='postition',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user')], default='user', max_length=10),
        ),
    ]
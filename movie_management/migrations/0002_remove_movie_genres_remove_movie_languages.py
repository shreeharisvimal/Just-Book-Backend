# Generated by Django 5.0.6 on 2024-06-07 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='languages',
        ),
    ]

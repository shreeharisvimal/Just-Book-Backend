# Generated by Django 5.0.6 on 2024-06-07 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_management', '0002_remove_movie_genres_remove_movie_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.CharField(default='00/00/0000', max_length=255),
        ),
    ]

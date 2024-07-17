# Generated by Django 5.0.6 on 2024-06-15 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movie_management', '0003_movie_language_movie_release_date'),
        ('theater_management', '0006_theater_theater_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_date', models.DateField()),
                ('show_time', models.TimeField()),
                ('price', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_management.movie')),
                ('screen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theater_management.screen')),
                ('theater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theater_management.theater')),
            ],
        ),
    ]

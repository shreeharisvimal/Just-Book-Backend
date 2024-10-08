# Generated by Django 5.0.6 on 2024-06-04 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('tmdb_id', models.IntegerField()),
                ('poster_path', models.CharField(max_length=225)),
                ('background_path', models.CharField(max_length=225)),
                ('video_key', models.CharField(max_length=225)),
                ('genres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='movie_management.genre')),
                ('languages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='movie_management.language')),
            ],
        ),
    ]

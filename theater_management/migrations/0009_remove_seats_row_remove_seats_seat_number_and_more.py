# Generated by Django 5.0.6 on 2024-07-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_management', '0008_remove_theater_latitude_remove_theater_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seats',
            name='row',
        ),
        migrations.RemoveField(
            model_name='seats',
            name='seat_number',
        ),
        migrations.RemoveField(
            model_name='seats',
            name='seat_type',
        ),
        migrations.AddField(
            model_name='seats',
            name='seat_allocation',
            field=models.JSONField(default='{}'),
        ),
        migrations.AlterField(
            model_name='theater',
            name='address',
            field=models.TextField(blank=True, default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='theater',
            name='city',
            field=models.TextField(blank=True, default=' ', null=True),
        ),
        migrations.AlterField(
            model_name='theater',
            name='no_of_screens',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='theater',
            name='state',
            field=models.TextField(blank=True, default=' ', null=True),
        ),
    ]

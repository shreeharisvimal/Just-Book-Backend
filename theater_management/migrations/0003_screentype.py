# Generated by Django 5.0.6 on 2024-06-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater_management', '0002_alter_theater_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price_multi', models.CharField(max_length=50)),
            ],
        ),
    ]
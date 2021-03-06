# Generated by Django 2.1.7 on 2019-03-13 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='date_born',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='home',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='distance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='lap_distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='laps_run',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='length',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='scheduled_distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='scheduled_laps',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='race',
            name='surface',
            field=models.CharField(blank=True, choices=[('P', 'Paved'), ('R', 'Road'), ('D', 'Dirt')], max_length=2, null=True),
        ),
    ]

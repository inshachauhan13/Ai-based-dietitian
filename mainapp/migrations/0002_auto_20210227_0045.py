# Generated by Django 3.1.1 on 2021-02-26 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='records_users',
            name='bmi',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='records_users',
            name='bmr',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='records_users',
            name='ctmw',
            field=models.FloatField(default=0.0),
        ),
    ]

# Generated by Django 3.1.7 on 2021-07-21 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20210721_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenotazione',
            name='tavolo',
            field=models.ForeignKey(default='Z0', on_delete=django.db.models.deletion.CASCADE, to='booking.tavolo'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.1.7 on 2021-07-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tavolo',
            name='stato',
            field=models.CharField(choices=[('L', 'Libero'), ('P', 'Prenotato'), ('D', 'Disabilitato')], max_length=1),
        ),
    ]

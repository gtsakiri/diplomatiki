# Generated by Django 2.1 on 2018-08-27 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eklogestbl',
            name='dateofelection',
            field=models.DateField(blank=True, db_column='dateOfElection', null=True),
        ),
    ]
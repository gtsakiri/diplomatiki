# Generated by Django 2.1 on 2018-08-25 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0003_auto_20180820_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edres',
            name='descr',
            field=models.CharField(max_length=45, verbose_name='Περιγραφή'),
        ),
        migrations.AlterField(
            model_name='edres',
            name='edresprwtou',
            field=models.IntegerField(db_column='edresPrwtou', verbose_name='Έδρες Πρώτου'),
        ),
        migrations.AlterField(
            model_name='edres',
            name='edresypoloipwn',
            field=models.IntegerField(db_column='edresYpoloipwn', verbose_name='Έδρες Υπολοίπων'),
        ),
        migrations.AlterField(
            model_name='edres',
            name='sinoloedrwn',
            field=models.IntegerField(db_column='sinoloEdrwn', verbose_name='Σύνολο εδρών'),
        ),
    ]

# Generated by Django 2.1 on 2018-09-10 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0014_auto_20180909_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psifoi',
            name='kenid',
            field=models.ForeignKey(db_column='kenID', on_delete=django.db.models.deletion.CASCADE, to='Elections.Kentra'),
        ),
        migrations.AlterField(
            model_name='psifoi',
            name='simbid',
            field=models.ForeignKey(db_column='simbID', on_delete=django.db.models.deletion.CASCADE, to='Elections.Simbouloi'),
        ),
    ]
# Generated by Django 2.1 on 2018-09-07 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0011_auto_20180907_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psifodeltia',
            name='kenid',
            field=models.ForeignKey(db_column='kenID', on_delete=django.db.models.deletion.CASCADE, to='Elections.Kentra'),
        ),
        migrations.AlterField(
            model_name='psifodeltia',
            name='sindid',
            field=models.ForeignKey(db_column='sindID', on_delete=django.db.models.deletion.CASCADE, to='Elections.Sindiasmoi'),
        ),
    ]

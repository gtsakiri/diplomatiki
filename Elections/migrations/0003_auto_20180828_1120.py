# Generated by Django 2.1 on 2018-08-28 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0002_auto_20180827_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sindiasmoi',
            name='sindid',
            field=models.AutoField(db_column='sindID', primary_key=True, serialize=False),
        ),
    ]
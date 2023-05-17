# Generated by Django 2.1 on 2019-05-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Elections', '0005_eklkatametrimenapsifoikoinotitesonlyvw'),
    ]

    operations = [
        migrations.CreateModel(
            name='EklSumpsifoiKoinVw',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('eklid', models.IntegerField(db_column='eklID')),
                ('kentro', models.CharField(max_length=45)),
                ('kenid', models.IntegerField(db_column='kenID')),
                ('sumvotes', models.DecimalField(blank=True, db_column='sumVotes', decimal_places=0, max_digits=32, null=True)),
            ],
            options={
                'db_table': 'EKL_SUMPSIFOI_KOIN_VW',
                'managed': False,
            },
        ),
    ]
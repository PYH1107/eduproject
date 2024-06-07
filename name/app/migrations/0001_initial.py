# Generated by Django 5.0.6 on 2024-06-02 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareRequirements',
            fields=[
                ('diet_type', models.TextField(blank=True, null=True)),
                ('characteristic', models.TextField(blank=True, null=True)),
                ('special_requirements', models.TextField(blank=True, null=True)),
                ('care_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'care_requirements',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sex', models.TextField(blank=True, null=True)),
                ('price', models.TextField(blank=True, null=True)),
                ('birth_year', models.IntegerField(blank=True, null=True)),
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SnakeSpecies',
            fields=[
                ('scientific_name', models.TextField(blank=True, db_column='scientific name', null=True)),
                ('chinese_name', models.TextField(blank=True, db_column='Chinese name', null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('species_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'snake_species',
                'managed': False,
            },
        ),
    ]
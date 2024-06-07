# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CareRequirements(models.Model):
    diet_type = models.TextField(blank=True, null=True)
    characteristic = models.TextField(blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    species = models.ForeignKey('SnakeSpecies', models.DO_NOTHING, blank=True, null=True)
    care_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'care_requirements'


class Product(models.Model):
    sex = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    species = models.ForeignKey('SnakeSpecies', models.DO_NOTHING, blank=True, null=True)
    product_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'product'


class SnakeSpecies(models.Model):
    scientific_name = models.TextField(db_column='scientific name', blank=True, null=True, unique=True)  # Field renamed to remove unsuitable characters.
    chinese_name = models.TextField(db_column='Chinese name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    amount = models.IntegerField(blank=True, null=True)
    species_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'snake_species'

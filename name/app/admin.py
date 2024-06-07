from django.contrib import admin

# Register your models here.
from app.models import *


class CareRequirementsAdmin(admin.ModelAdmin):
    list_display = ('care_id', 'diet_type', 'characteristic', 'special_requirements', 'species')

admin.site.register(CareRequirements, CareRequirementsAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'sex', 'price', 'birth_year', 'species')

admin.site.register(Product, ProductAdmin)

class SnakeSpeciesAdmin(admin.ModelAdmin):
    list_display = ('species_id', 'scientific_name', 'chinese_name', 'amount')

admin.site.register(SnakeSpecies, SnakeSpeciesAdmin)
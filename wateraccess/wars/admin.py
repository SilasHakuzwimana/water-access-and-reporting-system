from django.contrib import admin
from .models import Province, District, Sector, Cell, Village

# Register your models here.


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')

@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sector')

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cell')
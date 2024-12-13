from django import forms
from .models import Province, District, Sector, Cell, Village

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = '__all__'

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = '__all__'

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = '__all__'

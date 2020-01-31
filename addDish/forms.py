from django import forms

from home.models import Dish, Categori

class CategoriForm(forms.ModelForm):
    class Meta:
        model = Categori
        fields = ['name']

class DishForm(forms.ModelForm):
    categori = forms.ModelChoiceField(queryset=Categori.objects.all(), to_field_name='name')
    class Meta:
        model = Dish
        fields = ['name', 'image', 'price', 'categori', 'enabled']
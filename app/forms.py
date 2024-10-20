from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Produse, ProprietatiProduse, Furnizori, Categorie

class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class ProductCreationForm(forms.ModelForm):
    # Use ModelChoiceField for ForeignKey fields
    furnizor = forms.ModelChoiceField(
        queryset=Furnizori.objects.all(),
        empty_label="Select Furnizor"
    )

    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        empty_label="Select Categorie"
    )

    class Meta:
        model = Produse
        fields = '__all__'

class PropertiesProductForm(ModelForm):

    DOMENIU_OPTIONS = [
        ("Medicina Dentara", "Medicina Dentara"),
        ("Medicina", "Medicina"),
        ("Drept", "Drept"),
        ("Informatica", "Informatica"),
        ("Inginerie", "Inginerie")
    ]

    DIMENIUNE_OPTIONS = [
        ("A4", "A4"),
        ("A5", "A5"),
        ("B5", "B5"),
        ("Letter", "Letter"),
        ("Pocket", "Pocket"),
        ("Executive", "Executive")
    ]

    FOAIE_OPTIONS = [
        ("80g/mp", "80g/mp"),
        ("70g/mp", "70g/mp"),
        ("90g/mp", "90g/mp"),
        ("100g/mp", "100g/mp")
    ]

    PAGINA_OPTIONS = [
        ("Velina", "Velina"),
        ("Dictando", "Dictando"),
        ("Matematica", "Matematica")
    ]

    CULORI_OPTIONS = [
        ("Rosu", "Rosu"),
        ("Albastru", "Albastru"),
        ("Verde", "Verde"),
        ("Galben", "Galben"),
        ("Portocaliu", "Portocaliu"),
        ("Mov", "Mov"),
        ("Roz", "Roz"),
        ("Alb", "Alb"),
        ("Negru", "Negru")
    ]

    domeniu = forms.ChoiceField(choices = DOMENIU_OPTIONS)
    Dimensiune = forms.ChoiceField(choices = DIMENIUNE_OPTIONS)
    Foaie = forms.ChoiceField(choices = FOAIE_OPTIONS)
    Pagina = forms.ChoiceField(choices= PAGINA_OPTIONS)
    Culori = forms.MultipleChoiceField(choices = CULORI_OPTIONS, widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = ProprietatiProduse
        fields = '__all__'
        exclude = ["produs"]


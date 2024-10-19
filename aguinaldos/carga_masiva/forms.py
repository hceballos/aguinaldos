from django.db import models



from django import forms

class CargaMasivaForm(forms.Form):
    archivo_excel = forms.FileField(label="Seleccione el archivo Excel")

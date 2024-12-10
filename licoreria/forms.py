from django import forms
from .models import Detalle, Venta

class DetalleForm(forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['razon', 'detalle', 'producto', 'cantidad', 'monto_total']
        widgets = {
            'razon': forms.TextInput(attrs={'class': 'form-control'}),
            'detalle': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha', 'detalle']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'detalle': forms.Select(attrs={'class': 'form-control'}),
           
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['detalle'].queryset = Detalle.objects.filter(id_det__in=[7, 5])
    
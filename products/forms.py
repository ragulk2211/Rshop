from django import forms
from .models import ProductImage

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['img', 'video', 'caption']

    def clean(self):
        cleaned_date = super().clean()
        img = cleaned_date.get('img')
        
        if not img:
            raise forms.ValidationError("please upload an image")
        
        return cleaned_date
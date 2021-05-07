from django import forms
from images.models import Images
class CreateImages(forms.ModelForm):
    class Meta:
        model=Images
        fields=['image']
    def save(commit=True):
        if commit:
            Images.save()

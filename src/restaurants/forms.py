from django import forms

from .models import RestaurantLocation
from .validators import validate_category


class RestaurantCreateForm(forms.Form):
    name = forms.CharField()
    location = forms.CharField(required=False)
    category = forms.CharField(required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name == 'Johann':
            raise forms.ValidationError("That's an invalid name.")

        return name


class RestaurantLocationCreateForm(forms.ModelForm):
    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category'
        ]

    # category = forms.CharField(validators=[validate_category], required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name == 'Johann':
            raise forms.ValidationError("That's an invalid name.")

        return name



from django import forms
from .models import Parcel


# Globalne zmienne dla maksymalnych wymiarów paczki
MAX_WEIGHT = 50  # Maximum weight in kilograms
MAX_WIDTH = 100  # Maximum width in centimeters
MAX_HEIGHT = 200  # Maximum height in centimeters
MAX_DEPTH = 50  # Maximum depth in centimeters


class ParcelLockerSearchForm(forms.Form):
    search_query = forms.CharField(label='Wpisz miasto lub nr. urzadzenia które chcesz sprawdzić', max_length=100, required=False)


class ParcelForm(forms.ModelForm):
    weight = forms.FloatField(label='Weight (kg)')
    width = forms.FloatField(label='Width (cm)')
    height = forms.FloatField(label='Height (cm)')
    depth = forms.FloatField(label='Depth (cm)')

    class Meta:
        model = Parcel
        fields = ['destination_parcel_locker', 'recipient_first_name', 'recipient_last_name', 'recipient_phone',
                  'description', 'weight', 'width', 'height', 'depth']

    def clean(self):
        cleaned_data = super().clean()
        dimensions = [
            ('weight', cleaned_data.get('weight'), MAX_WEIGHT),
            ('width', cleaned_data.get('width'), MAX_WIDTH),
            ('height', cleaned_data.get('height'), MAX_HEIGHT),
            ('depth', cleaned_data.get('depth'), MAX_DEPTH)
        ]

        for dimension, value, max_value in dimensions:
            if value and value > max_value:
                self.add_error(dimension, f'Exceeded maximum value for {dimension} ({max_value}).')

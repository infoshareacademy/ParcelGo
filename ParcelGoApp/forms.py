from django import forms
from .models import Parcel, ParcelLocker


# Globalne zmienne dla maksymalnych wymiarów paczki
MAX_WEIGHT = 25  # Maximum weight in kilograms
MAX_WIDTH = 40  # Maximum width in centimeters
MAX_HEIGHT = 40  # Maximum height in centimeters
MAX_DEPTH = 60  # Maximum depth in centimeters


class ParcelLockerSearchForm(forms.Form):
    search_query = forms.CharField(label='Wpisz miasto lub nr. urzadzenia które chcesz sprawdzić', max_length=100, required=False)


class ParcelForm(forms.ModelForm):
    weight = forms.FloatField(label=f'Weight (max {MAX_WEIGHT} kg)')
    width = forms.FloatField(label=f'Width (max {MAX_WIDTH} cm)')
    height = forms.FloatField(label=f'Height (max {MAX_HEIGHT} cm)')
    depth = forms.FloatField(label=f'Depth (max {MAX_DEPTH} cm)')
    destination_parcel_locker = forms.ModelChoiceField(queryset=ParcelLocker.objects.all(),
                                                       label='Parcel Locker',
                                                       to_field_name='id',
                                                       empty_label=None)
    recipient_email = forms.EmailField(label='Recipient Email')

    class Meta:
        model = Parcel
        fields = ['destination_parcel_locker', 'recipient_first_name', 'recipient_last_name', 'recipient_phone',
                  'recipient_email', 'description', 'weight', 'width', 'height', 'depth']

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

    def clean_width(self):
        width = self.cleaned_data.get('width')
        if width <= 0:
            raise forms.ValidationError("Width cannot be negative or zero.")
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height cannot be negative or zero.")
        return height

    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        if depth <= 0:
            raise forms.ValidationError("Depth cannot be negative or zero.")
        return depth

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight cannot be negative or zero.")
        return weight


from django import forms

class ParcelLockerSearchForm(forms.Form):
    search_query = forms.CharField(label='Wpisz miasto lub nr. urzadzenia które chcesz sprawdzić', max_length=100, required=False)


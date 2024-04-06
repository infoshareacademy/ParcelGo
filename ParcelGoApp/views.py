from django.shortcuts import render
from .models import ParcelLocker
from .forms import ParcelLockerSearchForm


def parcel_locker_search(request):
    parcel_lockers = None  # Początkowo ustawiamy na None, aby nie wyświetlać listy na początku
    form = ParcelLockerSearchForm(request.GET or None)  # Pobierz dane z formularza lub utwórz nowy formularz

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            # wyszukiwanie paczkomatów po mieście lub numerze paczkomatu
            parcel_lockers = ParcelLocker.objects.filter(
                city__icontains=search_query) | ParcelLocker.objects.filter(locker_number__icontains=search_query)

    return render(request, 'ParcelGoApp/parcel_locker_search.html', {'form': form, 'parcel_lockers': parcel_lockers})


from django.shortcuts import render
from .models import ParcelLocker
from .forms import ParcelLockerSearchForm
from django.db.models import Q


def parcel_locker_search(request):
    parcel_lockers = None
    no_results_message = None

    if request.method == 'GET':
        form = ParcelLockerSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            if search_query:
                # Wyszukaj paczkomaty po mieście lub numerze urządzenia
                parcel_lockers = ParcelLocker.objects.filter(
                    Q(city__icontains=search_query) | Q(locker_number__icontains=search_query)
                )

                if not parcel_lockers.exists():
                    no_results_message = f"Brak wyników dla zapytania: '{search_query}'"
    else:
        form = ParcelLockerSearchForm()

    return render(request, 'ParcelGoApp/parcel_locker_search.html', {
        'form': form,
        'parcel_lockers': parcel_lockers,
        'no_results_message': no_results_message
    })



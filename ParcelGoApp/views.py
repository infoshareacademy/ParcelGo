from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ParcelLocker, Parcel
from .forms import ParcelLockerSearchForm, ParcelForm
from django.db.models import Q
import random
from django.views.generic import TemplateView

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


def create_parcel(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.sender = request.user
            parcel.save()
            # Convert the tracking number to a string before saving it to the session
            tracking_number_str = str(parcel.tracking_number)
            request.session['tracking_number'] = tracking_number_str
            return redirect('parcel_created')
    else:
        form = ParcelForm()
    return render(request, 'ParcelGoApp/create_parcel.html', {'form': form})


def parcel_created(request):
    # Get the tracking number from the session
    tracking_number_str = request.session.get('tracking_number', None)
    # Remove the tracking number from the session
    request.session.pop('tracking_number', None)
    return render(request, 'ParcelGoApp/parcel_created.html', {'tracking_number': tracking_number_str})

@staff_member_required
def approve_delivery(request):
    if request.method == 'POST':
        approved_parcel_ids = request.POST.getlist('approved_parcels')

        for parcel_id in approved_parcel_ids:
            parcel = Parcel.objects.get(id=parcel_id)
            parcel_locker = parcel.destination_parcel_locker
            if parcel_locker.capacity <= 0:
                messages.error(request,
                               f"The Parcel Locker {parcel_locker.locker_number} is full. Cannot deliver more parcels.")
                return redirect('approve_delivery')
            else:
                parcel_locker.capacity -= 1
                parcel_locker.save()

            pickup_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
            parcel.pickup_code = pickup_code
            parcel.save()

        Parcel.objects.filter(id__in=approved_parcel_ids).update(is_delivered=True, status='Delivered')

        return redirect('delivery_approval_success')

    else:
        pending_parcels = Parcel.objects.filter(is_approved=False).exclude(status__in=['Delivered', 'Received'])
        return render(request, 'ParcelGoApp/approve_delivery.html', {'pending_parcels': pending_parcels})


def delivery_approval_success(request):
    return render(request, 'ParcelGoApp/delivery_approval_success.html')


def parcel_pickup(request):
    if request.method == 'POST':
        recipient_phone = request.POST.get('recipient_phone')
        pickup_code = request.POST.get('pickup_code')

        try:
            parcel = Parcel.objects.get(recipient_phone=recipient_phone, pickup_code=pickup_code)

            # Weryfikacja aktualnego statusu paczki
            if parcel.status == 'Received':
                # Wyświetlenie wiadomości z datą odbioru
                success_message = f'Parcel has already been received on {parcel.received_date}.'
                return render(request, 'ParcelGoApp/parcel_pickup.html', {'success_message': success_message})


            # Wywołanie metody mark_as_received
            parcel.mark_as_received()

            # Zwiększenie pojemności paczkomatu
            parcel_locker = parcel.destination_parcel_locker
            parcel_locker.capacity += 1
            parcel_locker.save()

            messages.success(request, 'Parcel has been successfully picked up.')

        except Parcel.DoesNotExist:
            messages.error(request, 'Invalid recipient phone or pickup code.')

    return render(request, 'ParcelGoApp/parcel_pickup.html')


class HomePageView(TemplateView):
    template_name = 'ParcelGoApp/home.html'

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import ParcelLocker, Parcel
from .forms import ParcelLockerSearchForm, ParcelForm
from django.db.models import Q
import random
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


def parcel_locker_search(request):

    parcel_lockers = None
    no_results_message = None

    user = request.user

    # Przekazanie imienia użytkownika do kontekstu, jeśli użytkownik jest zalogowany
    fname = None
    if user.is_authenticated:
        fname = user.first_name
    
    if request.method == "GET":
        form = ParcelLockerSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get("search_query")
            if search_query:
                # Wyszukaj paczkomaty po mieście lub numerze urządzenia
                parcel_lockers = ParcelLocker.objects.filter(
                    Q(city__icontains=search_query)
                    | Q(locker_number__icontains=search_query)
                )

                if not parcel_lockers.exists():
                    no_results_message = (
                        f"No results found for your query: '{search_query}'"
                    )
    else:
        form = ParcelLockerSearchForm()

    return render(
        request,
        "ParcelGoApp/parcel_locker_search.html",
        {
            "form": form,
            "parcel_lockers": parcel_lockers,
            "no_results_message": no_results_message,
            "fname": fname,
        },
    )


def create_parcel(request):
    if request.method == "POST":
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.sender = request.user
            parcel.status = "Payment_Pending"
            parcel.save()
            return redirect(reverse("payment_page", kwargs={"parcel_id": parcel.id}))
    else:
        form = ParcelForm()

    # Przekazanie informacji o zalogowanym użytkowniku do kontekstu renderowania
    user = request.user
    fname = None
    if user.is_authenticated:
        fname = user.first_name        

    return render(
        request,
        "ParcelGoApp/create_parcel.html",
        {
            "form": form,
            "fname": fname,  # Dodaj to do kontekstu
        },
    )


def parcel_created(request, tracking_number):
    return render(
        request, "ParcelGoApp/parcel_created.html", {"tracking_number": tracking_number}
    )


def payment_page(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)

    if parcel.status != "Payment_Pending":
        return HttpResponse("Błąd: Niepoprawny status paczki.")

    # Obliczanie kwoty na podstawie gabarytu paczki
    if parcel.width <= 8 or parcel.height <= 8 or parcel.depth <= 8:
        fee = 10
    elif parcel.width <= 19 or parcel.height <= 19 or parcel.depth <= 19:
        fee = 13
    elif parcel.width <= 40 and parcel.height <= 40 and parcel.depth <= 60:
        fee = 16
    else:
        return HttpResponse("Błąd: Niepoprawne wymiary paczki.")

    return render(
        request, "ParcelGoApp/payment_page.html", {"parcel": parcel, "fee": fee}
    )


def confirm_payment(request, parcel_id):
    parcel = get_object_or_404(Parcel, id=parcel_id)

    if request.method == "POST":
        # Sprawdź, czy paczka jest w stanie oczekiwania na płatność
        if parcel.status != "Payment_Pending":
            return HttpResponse("Błąd: Niepoprawny status paczki.")

        # Oznacz płatność jako zatwierdzoną i zmień status paczki na "In delivery"
        parcel.whether_paid = True
        parcel.status = "In delivery"
        parcel.save()

        # stwórz adres URL do strony  z numerem śledzenia  + Tworzenie linku
        tracking_number = parcel.tracking_number
        link_package_status_url = request.build_absolute_uri(
            reverse("link_package_status", args=[tracking_number])
        )

        # Tworzenie wiadomości e-mail
        subject = "Potwierdzenie utworzenia paczki"
        message = f"Paczka została potwierdzona i opłacona. Możesz sprawdzić jej status pod adresem: {link_package_status_url}"
        sender_email = "Parcel.Go.No.Reply@gmail.com"
        recipient_email = parcel.recipient_email

        send_mail(subject, message, sender_email, [recipient_email])

        # Przekieruj użytkownika na stronę parcel_created
        return redirect(reverse("parcel_created", args=[tracking_number]))


def cancel_payment(request, parcel_id):
    # Pobierz paczkę do anulowania płatności
    parcel = get_object_or_404(Parcel, id=parcel_id)

    # Usuń paczkę
    parcel.delete()

    # Przekieruj użytkownika na stronę główną
    return redirect("/users/account/")


@staff_member_required
def approve_delivery(request):
    if request.method == "POST":
        approved_parcel_ids = request.POST.getlist("approved_parcels")

        for parcel_id in approved_parcel_ids:
            parcel = Parcel.objects.get(id=parcel_id)
            parcel_locker = parcel.destination_parcel_locker
            if parcel_locker.capacity <= 0:
                messages.error(
                    request,
                    f"The Parcel Locker {parcel_locker.locker_number} is full. Cannot deliver more parcels.",
                )
                return redirect("approve_delivery")
            else:
                parcel_locker.capacity -= 1
                parcel_locker.save()

            pickup_code = "".join(str(random.randint(0, 9)) for _ in range(6))
            parcel.pickup_code = pickup_code
            parcel.save()

            subject = "Potwierdzenie dostarczenia paczki do paczkomatu"
            paczkomat_address = f"{parcel_locker.city}, {parcel_locker.street} {parcel_locker.street_number}"
            message = (
                f"Paczka została dostarczona do paczkomatu.\n\n"
                f"Adres paczkomatu: {paczkomat_address}\n"
                f"Kod odbioru: {parcel.pickup_code}\n"
                f"Numer telefonu odbiorcy: {parcel.recipient_phone}\n\n"
            )
            sender_email = "Parcel.Go.No.Reply@gmail.com"
            recipient_email = parcel.recipient_email

            send_mail(subject, message, sender_email, [recipient_email])

        Parcel.objects.filter(id__in=approved_parcel_ids).update(
            is_delivered=True, status="Delivered"
        )

        return redirect("delivery_approval_success")

    else:
        pending_parcels = Parcel.objects.filter(is_approved=False).exclude(
            status__in=["Delivered", "Received", "Payment_Pending"]
        )
        return render(
            request,
            "ParcelGoApp/approve_delivery.html",
            {"pending_parcels": pending_parcels},
        )


def delivery_approval_success(request):
    return render(request, "ParcelGoApp/delivery_approval_success.html")


def parcel_pickup(request):
    user = request.user
    fname = None
    if user.is_authenticated:
        fname = user.first_name

    if request.method == "POST":
        recipient_phone = request.POST.get("recipient_phone")
        pickup_code = request.POST.get("pickup_code")

        try:
            parcel = Parcel.objects.get(
                recipient_phone=recipient_phone, pickup_code=pickup_code
            )

            # Weryfikacja aktualnego statusu paczki
            if parcel.status == "Received":
                # Wyświetlenie wiadomości z datą odbioru
                success_message = (
                    f"Parcel has already been received on {parcel.received_date}."
                )
                return render(
                    request,
                    "ParcelGoApp/parcel_pickup.html",
                    {"success_message": success_message},
                )

            # Wywołanie metody mark_as_received
            parcel.mark_as_received()

            # Zwiększenie pojemności paczkomatu
            parcel_locker = parcel.destination_parcel_locker
            parcel_locker.capacity += 1
            parcel_locker.save()

            messages.success(request, "Parcel has been successfully picked up.")

        except Parcel.DoesNotExist:
            messages.error(request, "Invalid recipient phone or pickup code.")

    return render(request, "ParcelGoApp/parcel_pickup.html", {"fname": fname})


class HomePageView(TemplateView):
    template_name = "ParcelGoApp/home.html"

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated:
            user = self.request.user
            authenticated_user_name = user.first_name
            context["fname"] = authenticated_user_name
        return context


def track_package(request):
    if request.method == "POST":
        tracking_number = request.POST.get("tracking_number")
        return link_package_status(request, tracking_number)

    user = request.user
    fname = None
    if user.is_authenticated:
        fname = user.first_name

    return render(
        request,
        "ParcelGoApp/track_package.html",
        {
            "fname": fname,
        },
    )


def link_package_status(request, tracking_number):
    try:
        parcel = Parcel.objects.get(tracking_number=tracking_number)
        return render(
            request, "ParcelGoApp/link_package_status.html", {"parcel": parcel}
        )
    except Parcel.DoesNotExist:
        message = "Brak paczki o podanym numerze śledzenia."
        return render(
            request, "ParcelGoApp/link_package_status.html", {"message": message}
        )
    except ValidationError:
        message = f'"{tracking_number}" nie jest prawidłowym formatem numeru śledzenia.'
        return render(
            request, "ParcelGoApp/link_package_status.html", {"message": message}
        )

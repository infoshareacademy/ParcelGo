from django.test import TestCase
from .models import ParcelLocker
from django.urls import reverse
from user.models import User
from .forms import ParcelForm


class ParcelLockerSearchTestCase(TestCase):
    def setUp(self):
        ParcelLocker.objects.get_or_create(locker_number='1A', city='Warszawa', street='Testowa', street_number='1', capacity=10)
        ParcelLocker.objects.get_or_create(locker_number='2B', city='Kraków', street='Inna', street_number='2', capacity=5)
        ParcelLocker.objects.get_or_create(locker_number='3B', city='Warszawa', street='Inna3', street_number='33', capacity=5)

    def test_search_by_city(self):
        """Test wyszukiwania paczkomatów po mieście."""
        request = self.client.get('/parcel-lockers/search/?search_query=Warszawa')
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Warszawa')
        self.assertContains(request, '1A')
        self.assertEqual(len(request.context['parcel_lockers']), 2)


    def test_search_by_locker_number(self):
        """Test wyszukiwania paczkomatów po numerze urządzenia."""
        request = self.client.get('/parcel-lockers/search/?search_query=2B')
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Kraków')
        self.assertContains(request, '2B')

    def test_no_results(self):
        """Test wyszukiwania, gdy brak wyników."""
        request = self.client.get('/parcel-lockers/search/?search_query=AAA')
        self.assertEqual(request.status_code, 200)
        self.assertTrue('no_results_message' in request.context)
        self.assertEqual(request.context['no_results_message'], "No results found for your query: 'AAA'")

    def test_invalid_search(self):
        """Test wyszukiwania z nieprawidłowymi danymi."""
        request = self.client.get('/parcel-lockers/search/?search_query=')
        self.assertEqual(request.status_code, 200)
        self.assertNotContains(request, 'Warszawa')
        self.assertNotContains(request, 'Kraków')


class ParcelCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.parcel_locker = ParcelLocker.objects.create(locker_number='A1', city='Warszawa', street='Testowa', street_number='1', capacity=10)

    def test_create_parcel_valid_form(self):
        form_data = {
            'destination_parcel_locker': self.parcel_locker.id,
            'recipient_first_name': 'John',
            'recipient_last_name': 'Doe',
            'recipient_phone': '123456789',
            'recipient_email': 'john@example.com',
            'description': 'Test parcel',
            'weight': 2.5,
            'width': 20,
            'height': 30,
            'depth': 15
        }
        form = ParcelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_parcel_invalid_form(self):
        form_data = {
            'destination_parcel_locker': self.parcel_locker.id,
            'recipient_first_name': 'John',
            'recipient_last_name': 'Doe',
            'recipient_phone': '123456789',
            'recipient_email': 'john@example.com',
            'description': 'Test parcel',
            'weight': -2.5,  # Invalid weight
            'width': 20,
            'height': 30,
            'depth': 15
        }
        form = ParcelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_parcel_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_parcel'), {
            'destination_parcel_locker': self.parcel_locker.id,
            'recipient_first_name': 'John',
            'recipient_last_name': 'Doe',
            'recipient_phone': '123456789',
            'recipient_email': 'john@example.com',
            'description': 'Test parcel',
            'weight': 2.5,
            'width': 20,
            'height': 30,
            'depth': 15
        })
        self.assertEqual(response.status_code, 302)  # Check if redirection happens

    def test_create_parcel_view_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_parcel'), {
            'destination_parcel_locker': self.parcel_locker.id,
            'recipient_first_name': 'John',
            'recipient_last_name': 'Doe',
            'recipient_phone': '123456789',
            'recipient_email': 'john@example.com',
            'description': 'Test parcel',
            'weight': -2.5,  # Invalid weight
            'width': 20,
            'height': 30,
            'depth': 15
        })
        self.assertEqual(response.status_code, 200)  # Check if form re-rendered with errors
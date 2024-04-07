from django.test import TestCase
from .models import ParcelLocker
from .views import parcel_locker_search

class ParcelLockerSearchTestCase(TestCase):
    def setUp(self):
        ParcelLocker.objects.create(locker_number='1A', city='Warszawa', street='Testowa', street_number='1', capacity=10)
        ParcelLocker.objects.create(locker_number='2B', city='Kraków', street='Inna', street_number='2', capacity=5)

    def test_search_by_city(self):
        """Test wyszukiwania paczkomatów po mieście."""
        request = self.client.get('/parcel-lockers/search/?search_query=Warszawa')
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, 'Warszawa')
        self.assertContains(request, '1A')

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
        self.assertContains(request, 'Brak wyników')

    def test_invalid_search(self):
        """Test wyszukiwania z nieprawidłowymi danymi."""
        request = self.client.get('/parcel-lockers/search/?search_query=')
        self.assertEqual(request.status_code, 200)
        self.assertNotContains(request, 'Warszawa')
        self.assertNotContains(request, 'Kraków')

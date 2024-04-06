from django.urls import path
from . import views

urlpatterns = [
    path('parcel-lockers/search/', views.parcel_locker_search, name='parcel_locker_search'),
]

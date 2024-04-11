from django.urls import path
from . import views

urlpatterns = [
    path('parcel-lockers/search/', views.parcel_locker_search, name='parcel_locker_search'),
    path('create/', views.create_parcel, name='create_parcel'),
    path('parcel_created/', views.parcel_created, name='parcel_created'),
    path('approve_delivery/', views.approve_delivery, name='approve_delivery'),
    path('delivery_approval_success/', views.delivery_approval_success, name='delivery_approval_success'),
    path('parcel/pickup/', views.parcel_pickup, name='parcel_pickup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('track/', views.track_package, name='track_package'),

]



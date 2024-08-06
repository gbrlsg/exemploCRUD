from django.urls import path
from db import views

urlpatterns = {
    path('clear/', views.clear_db),
    path("clients/", views.clients_list),
    path("onix/<int:pk>/", views.onix_test),
    path("clients/<int:pk>/", views.client_detail),
    path("vehicles/<int:pk>/", views.vehicle_detail)

}
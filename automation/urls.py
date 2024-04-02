from django.urls import path
from .views import virtual_machine_detail, virtual_machine_view

urlpatterns = [
    path('vms/<str:public_ip>/', virtual_machine_detail),
        path('vms/', virtual_machine_view),
]

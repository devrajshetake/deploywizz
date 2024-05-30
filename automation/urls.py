from django.urls import path
from .views import virtual_machine_detail, virtual_machine_view, test_view, deploy_site

urlpatterns = [
    path('vms/<str:public_ip>/', virtual_machine_detail),
    path('vms/', virtual_machine_view),
    path('test/', test_view),
    path('deploy_site/', deploy_site, name='deploy_view')
]

"""
{
    "git_url": "https://github.com/devrajshetake/DVBS2-toolkit",
    "public_ip": "4.227.182.7"
}

{
    "user": 1,
    "public_ip": "4.227.182.7",
    "provider": "AWS",
    "region": "us-west-1"
}
"""
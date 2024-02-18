"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from automation.views import test_view
from sites.views import DeploySiteView, SiteListView, DeploymentListView, DeploymentDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', view=test_view),
    path('sites/<int:pk>/deploy/', DeploySiteView.as_view(), name='deploy_site'),
    path('sites/', SiteListView.as_view(), name='site_list'),
    path('deployments/', DeploymentListView.as_view(), name='deployment_list'),
    path('deployments/<int:pk>/', DeploymentDetailView.as_view(), name='deployment_detail'),
]

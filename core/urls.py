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
from django.urls import path, include
from automation.views import test_view
from sites.views import DeployRepositoryView, SiteListView, DeploymentListView
from users.views import UserReposView, RepoStructureView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('test/', view=test_view),
    path('github-user/<str:username>/repos/', UserReposView.as_view(), name='user_repos'),
    path('github-repo/<str:username>/<str:repo_name>/', RepoStructureView.as_view(), name='repo_structure'),
    path('sites/', SiteListView.as_view(), name='site_list'),
    path('deployments/', DeploymentListView.as_view(), name='deployment_list'),
    path('deploy/', DeployRepositoryView.as_view(), name='deploy_repository'),
    path('automation/', include('automation.urls')),

]

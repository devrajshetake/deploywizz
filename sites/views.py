from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from github import Github
from django.http import JsonResponse
from .models import Site, Deployment
from .serializers import SiteSerializer, DeploymentSerializer
from django.contrib.auth.models import User

class GitHubAPI:
    def __init__(self, token):
        self.github = Github(token)

    def get_repo_structure(self, username, repo_name):
        user = self.github.get_user(username)
        repo = user.get_repo(repo_name)
        structure = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                structure.append({
                    'name': file_content.name,
                    'path': file_content.path,
                    'download_url': file_content.download_url,
                    'type': file_content.type
                })
        return structure

class DeployRepositoryView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        repo_name = request.data.get('repo_name')
        
        try:
            owner = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': f"User with username '{username}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            github_api = GitHubAPI(token='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')  
            repo_structure = github_api.get_repo_structure(username, repo_name)

            # user, created = User.objects.get_or_create(username=username)

            site = Site.objects.create(name=repo_name) 
            deployment = Deployment.objects.create(site=site)
            
            return JsonResponse({'message': f"Repository '{repo_name}' deployed successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SiteListView(generics.ListAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class DeploymentListView(generics.ListCreateAPIView):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer

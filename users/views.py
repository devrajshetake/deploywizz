from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import GitHub

class UserReposView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            username = kwargs.get('username')
            github = GitHub(token='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')
            repos = github.get_repos(username)
            return JsonResponse({'repos': repos}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class RepoStructureView(View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            username = kwargs.get('username')
            repo_name = kwargs.get('repo_name')
            github = GitHub(token='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')
            structure = github.get_repo_structure(username, repo_name)
            return JsonResponse({'structure': structure}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

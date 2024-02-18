from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from github import Github

# class CustomUser(AbstractUser):
    # pass


class GitHub:
    def __init__(self, token=None):
        if token:
            self.github = Github(token)
        else:
            self.github = Github()

    def get_repos(self, username):
        user = self.github.get_user(username)
        repos = []
        for repo in user.get_repos():
            repos.append({
                'name': repo.name,
                'url': repo.html_url,
                'description': repo.description,
                'created_at': repo.created_at,
                'updated_at': repo.updated_at,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count
            })
        return repos

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
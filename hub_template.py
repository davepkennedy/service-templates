from github import Github
import json

class GitTemplates(object):
    __slots__ = ['client', 'user']

    def __init__(self, user):
        self.client = Github()
        self.user = user

    def find_templates(self, repo='service-templates'):
        user_data = self.client.get_user(self.user)
        repos = user_data.get_repos()
        l = list(filter(lambda x: x.name == repo, repos))
        if len(l): 
            return Templates(l[0])
        return Templates(False)

class Templates(object):
    __slots__ = ['repo']

    def __init__ (self, repo):
        self.repo = repo

    def list_templates(self):
        if self.repo:
            return json.loads(self.repo.get_contents('manifest.json').decoded_content)
        return []

    def load_template(self, template):
        if self.repo:
            return Template(self.repo, 
            json.loads(self.repo.get_contents(template + '/manifest.json').decoded_content))
        return Template(False,False)

class Template(object):
    __slots__ = ['repo', 'manifest']

    def __init__ (self, repo, manifest):
        self.repo = repo            
        self.manifest = manifest

    def dependencies(self):
        return self.manifest['dependencies']

    def fetch(self):
        pass

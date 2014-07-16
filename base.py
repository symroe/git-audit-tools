import os
import glob

from github3 import login
import git
from git.exc import GitCommandError

class GitRepoException(Exception): pass

class BaseGitTool(object):

    github_token = "d542f971125c143fb8fd4b59745d70cd0cdc2de3"
    github_org = "ministryofjustice"
    
    def __init__(self, base_path=".", login=True):
        if login:
            self.login()
        self.base_repo_path = "repos"
    
    def login(self):
        self.github = login(token=self.github_token)
        self.org = self.github.organization(self.github_org)
    
    def repo_list(self):
        self.repos = []
        for r in self.org.iter_repos():
            self.repos.append(r)
        return self.repos

    def parse_branches(self, repo):
        pass
    
    def iter_paths(self):
        for path in glob.glob("%s/*" % self.base_repo_path):
            yield path
    
    def iter_projects(self):
        for path in self.iter_paths():
            yield Project(git.Repo(path))
    
    
class RepoSync(BaseGitTool):
    def sync(self):
        for repo in self.repo_list():
            print repo.name
            repo_path = os.path.join(self.base_repo_path, repo.name)
            if not os.path.exists(repo_path):
                # Need to clone
                print "\tCloning"
                try:
                    git.Git().clone(repo.clone_url, repo_path)
                except GitCommandError:
                    print "\tError cloning %s" % repo.clone_url
            # import ipdb; ipdb.set_trace()

class ProjectList(BaseGitTool):
    pass

class Project(object):
    def __init__(self, repo):
        self.repo = repo
        self.name = os.path.split(repo.working_tree_dir)[-1]
        self.data = {}
    
    def add_data(self, gatherer, data):
        self.data.update({gatherer: data})

class Gatherer(object):
    def __init__(self, project):
        self.project = project


if __name__ == "__main__":
    r = RepoSync()
    r.sync()
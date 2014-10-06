import os
import glob
import datetime
import StringIO
import subprocess

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

    @property
    def has_mr(self):
        from distutils import spawn
        return spawn.find_executable("mr")

    def _create_mr_config(self):
        config_file = StringIO.StringIO()
        for project in self.iter_projects():
            if not project.repo.remotes.origin.url.startswith('https'):
                config = """[%s]\ncheckout = git clone '%s' '%s'\nskip = !  hours_since "$1" 1\n\n""" \
                         % (project.name, project.repo.remotes.origin.url, project.name)
                config_file.write(config)
        with open('repos/.mrconfig', 'w') as mrconfig:
         mrconfig.write(config_file.getvalue())


    def _sync_with_mr(self):
        p = subprocess.Popen(['mr', '-t','-j10', 'update'], cwd="repos")
        p.wait()


    def sync(self):
        for github_repo in self.repo_list():
            print github_repo.name
            repo_path = os.path.join(self.base_repo_path, github_repo.name)

            if not os.path.exists(repo_path):
                # Need to clone
                print "\tCloning"
                try:
                    git.Git().clone(github_repo.ssh_url, repo_path)
                except GitCommandError:
                    print "\tError cloning %s" % github_repo.clone_url
            else:
                repo = git.Repo(repo_path)
                repo.git.reset('--hard')
                if not self.has_mr:
                    origin = repo.remotes.origin
                    print "\tPulling"
                    try:
                        origin.pull(github_repo.default_branch)
                    except GitCommandError:
                        print "\tError updating %s (could be empty)" % \
                              github_repo.clone_url
        if self.has_mr:
            self._create_mr_config()
            self._sync_with_mr()

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
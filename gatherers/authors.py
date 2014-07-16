import os
import glob
from datetime import datetime

from base import Project, Gatherer, GitRepoException
    
class Authors(Gatherer):
    name = 'authors'
    
    def run(self):
        authors = {}
        try:
            for commit in self.project.repo.iter_commits():
                # import ipdb; ipdb.set_trace()
                email = commit.author.email
                authors[email] = {
                    'name': commit.author.name
                }
            return authors
    
        except ValueError:
            raise GitRepoException('Error with %s' % self.project.name)
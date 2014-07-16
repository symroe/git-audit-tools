import os
import glob
from datetime import datetime

from base import Project, Gatherer, GitRepoException
    
class CommitsByDay(Gatherer):
    name = 'commits_by_day'
    
    def run(self):
        commits = {}
        try:
            for commit in self.project.repo.iter_commits():
                # import ipdb; ipdb.set_trace()
                date = datetime.fromtimestamp(commit.committed_date)
                date_str = date.strftime('%Y-%m-%d')
                if date_str in commits:
                    commits[date_str] += 1
                else:
                    commits[date_str] = 1
            dates = commits.keys()
            dates.sort()
            sorted_commits = []
            for date in dates:
                sorted_commits.append((date, commits[date]))
            return sorted_commits
        except ValueError:
            raise GitRepoException('Error with %s' % self.project.name)
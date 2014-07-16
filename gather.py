import json

from base import ProjectList, GitRepoException
from gatherers.parse_libs import GemfileParser
from gatherers.commits import CommitsByDay
from gatherers.authors import Authors
from gatherers.languages import Languages

gatherers = [
    GemfileParser,
    CommitsByDay,
    Authors,
    Languages,
]

if __name__ == "__main__":
    p = ProjectList(login=False)
    for project in p.iter_projects():
        for gather in gatherers:
            g = gather(project)
            try:
                project.add_data(g.name, g.run())
            except GitRepoException:
                pass
        print 
        print json.dumps(project.data)
        print 
        
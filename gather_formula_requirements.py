import json
from collections import defaultdict

from base import ProjectList, GitRepoException
from gatherers.formula_requirements import FormulaRequirementsParser

if __name__ == "__main__":
    p = ProjectList(login=False)
    formula_data = defaultdict(dict)
    for project in p.iter_projects():
        fr = FormulaRequirementsParser(project)
        try:
            project.add_data(fr.name, fr.run())
        except GitRepoException:
            pass
        if project.data['formula_requirements']:
            for requirement in project.data['formula_requirements']:
                version = requirement['revision']
                name = requirement['name']
                project_name = project.name
                try:
                    formula_data[name][version].append(project.name)
                except KeyError:
                    formula_data[name][version] = [project.name, ]
    for name, values in formula_data.items():
        if values:
            print name
            print "=" * len(name)
            for k, v in values.items():
                print "    * %s" % k
                print "        * %s" % ",".join(v)
                # print v
            print
        
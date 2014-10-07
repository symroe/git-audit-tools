import os

from base import ProjectList, GitRepoException
from gatherers.formula_requirements import FormulaRequirementsParser

if __name__ == "__main__":
    p = ProjectList(login=False)
    suspect_deploy_repos = set()
    for project in p.iter_projects():
        fr = FormulaRequirementsParser(project)
        try:
            project.add_data(fr.name, fr.run())
        except GitRepoException:
            pass
        if not project.data['formula_requirements']:
            if project.name.endswith(('-ops', '_ops', '-deploy', '_ops')):
                suspect_deploy_repos.add(project.name)

            fab_file_path = os.path.join(project.repo.working_tree_dir,
                                         'fabfile.py')
            
            if os.path.exists(fab_file_path):
                suspect_deploy_repos.add(project.name)
    print "\n".join(suspect_deploy_repos)
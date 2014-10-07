from base import ProjectList, GitRepoException
from gatherers.formula_requirements import FormulaRequirementsParser

if __name__ == "__main__":
    p = ProjectList(login=False)
    all_used_formulas = set()
    for project in p.iter_projects():
        fr = FormulaRequirementsParser(project)
        try:
            project.add_data(fr.name, fr.run())
        except GitRepoException:
            pass
        if project.data['formula_requirements']:
            names = [requirement['name'] for requirement in
                      project.data['formula_requirements']]
            if 'hardening' not in names:
                if not project.name.endswith('-formula'):
                    print project.name
import os
import glob
import json

import git

from cotton.salt_shaker import Shaker

from base import Project, Gatherer

class BaseLibParser(Gatherer):
        def run(self):
            return self.parse()

class FormulaRequirementsParser(BaseLibParser):
    name = 'formula_requirements'
    def parse(self):
        requirements_location = "%s/formula-requirements.txt" % self.project.repo.working_tree_dir
        requirements = []
        if os.path.exists(requirements_location):
            shaker = Shaker(self.project.repo.working_tree_dir)
            parsed_file = shaker.parse_requirements_file(requirements_location)
            if parsed_file:
                for requirement in parsed_file:
                    requirements.append({
                        'name': requirement['name'],
                        'revision': requirement['revision']
                    })
        return requirements

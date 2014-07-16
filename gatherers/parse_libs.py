import os
import glob

import git

from base import Project, Gatherer

class BaseLibParser(Gatherer):
        def run(self):
            return self.parse()
    
class GemfileParser(BaseLibParser):
    name = 'gems'

    # def parse(self):
    #     parsed_file = {'project': self.project.name}
    #     parsed_file['gems'] = self.parse_gemfile(self.project)
    #     return parsed_file
    
    def parse(self):
        gemfile_location = "%s/Gemfile" % self.project.repo.working_tree_dir
        gems = []
        if os.path.exists(gemfile_location):
            gemfile = open(gemfile_location)
            for line in gemfile.readlines():
                line = line.strip()
                if line.startswith('gem '):
                    gem_line = line.replace("'", "").strip('gem ').split(',')
                    gem = {}
                    name = gem_line.pop(0)
                    gem['name'] = name
                    if gem_line:
                        gem['version'] = gem_line.pop(0)
                    if gem_line:
                        gem['remainder'] = gem_line
                    gems.append(gem)
        return gems

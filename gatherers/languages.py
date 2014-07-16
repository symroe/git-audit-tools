import os
import glob

from base import Project, Gatherer, GitRepoException
    
class Languages(Gatherer):
    name = 'language'
    
    def run(self):
        extentions = {}
        for file in glob.glob("%s/**/**" % self.project.repo.working_tree_dir):
            if os.path.isfile(file):
                ext = file.split('.')[-1].strip('~ ')
                if ext in extentions:
                    extentions[ext] += 1
                else:
                    extentions[ext] = 1
        
        keys = extentions.keys()
        keys.sort(key=extentions.__getitem__, reverse=True)
        if not keys:
            return "Unknown"
        main_ext = keys.pop(0)
        if main_ext == 'rb':
            return 'Ruby'
        if main_ext == 'py':
            return 'Python'
        if main_ext == 'html':
            return 'HTML'
        if main_ext == 'js':
            return 'JavaScript'
        return main_ext
            
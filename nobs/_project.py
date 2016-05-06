from ._file import Directory
from ._target import _TargetUserBase


class Project(object):
    def __init__(self, name, build_result_dir,build_temp_dir,build_files_dir):
        if not isinstance(name,str): raise Exception("Project name must be a string!")
        self.name = name

        if not isinstance(build_result_dir,Directory): raise Exception("Build result directory must be an instance of \"nobs.Directory\"!")
        self.build_result_directory    = build_result_dir
        if not isinstance(build_temp_dir,Directory): raise Exception("Build temporary directory must be an instance of \"nobs.Directory\"!")
        self.build_temporary_directory = build_temp_dir
        if not isinstance(build_files_dir,Directory): raise Exception("Build files directory must be an instance of \"nobs.Directory\"!")
        self.build_files_directory     = build_files_dir

        self.targets = []

        self.generators = set()

    def add_target(self, target):
        if not isinstance(target,_TargetUserBase):
            raise Exception("Target must be an instance of one of { \"nobs.TargetStaticLibrary\", \"nobs.TargetDynamicLibrary\", \"nobs.TargetExecutable\" }!")
        self.targets.append(target)

    def _validate_basic(self):
        for gen in self.generators:
            gen._validate_basic()
        for target in self.targets:
            target._validate_basic()

    def generate(self):
        self._validate_basic()

        for generator in self.generators:
            generator.generate() 

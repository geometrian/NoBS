from ._file import Directory
from ._platform import Platform
from ._target import _TargetUserBase


class Project(object):
    def __init__(self, name, build_result_dir,build_temp_dir,build_files_dir):
        if not isinstance(name,str): raise Exception("Project name must be a string!")
        self.name = name

        self.build_result_directory    = build_result_dir
        self.build_temporary_directory = build_temp_dir
        self.build_files_directory     = build_files_dir
        if not isinstance(self.build_result_directory,Directory): raise Exception("Build result directory must be an instance of \"nobs.Directory\"!")
        if not isinstance(self.build_temporary_directory,Directory): raise Exception("Build temporary directory must be an instance of \"nobs.Directory\"!")
        if not isinstance(self.build_files_directory,Directory): raise Exception("Build files directory must be an instance of \"nobs.Directory\"!")

        self.platforms = []

        self.targets = []

    def add_platform(self, platform):
        if not isinstance(platform,Platform):
            raise Exception("Platform must be an instance of \"nobs.Platform\"!")
        self.platforms.append(platform)

    def add_target(self, target):
        if not isinstance(target,_TargetUserBase):
            raise Exception("Target must be an instance of one of { \"nobs.TargetStaticLibrary\", \"nobs.TargetDynamicLibrary\", \"nobs.TargetExecutable\" }!")
        self.targets.append(target)

    def _validate_basic(self):
        for platform in self.platforms:
            platform._validate_basic()
        for target in self.targets:
            target._validate_basic()

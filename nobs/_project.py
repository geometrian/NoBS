from ._file import Directory
from ._helpers import _errorinstance,_warning
from ._target import _TargetUserBase


class Project(object):
	def __init__(self,
		name,
		directory_project_root,
		directory_build_result,
		directory_build_temporary,
		directory_project_files
	):
		if not isinstance(name,str):
			_errorinstance("Project name",str)
		self.name = name

		if not isinstance(directory_project_root,   Directory):
			_errorinstance("Project root directory",     Directory)
		if not isinstance(directory_build_result,   Directory):
			_errorinstance("Build result directory",     Directory)
		if not isinstance(directory_build_temporary,Directory):
			_errorinstance("Build temporaries directory",Directory)
		if not isinstance(directory_project_files,  Directory):
			_errorinstance("Project files directory",    Directory)
		self.directory_project_root    = directory_project_root
		self.directory_build_result    = directory_build_result
		self.directory_build_temporary = directory_build_temporary
		self.directory_project_files   = directory_project_files

		self.targets = []

		self.generators = set()

	def generate(self):
		if len(self.generators) == 0:
			_warning("No generators added to project; no output will be made.")

		for generator in self.generators:
			generator.generate()

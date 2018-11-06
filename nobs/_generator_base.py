from . import _configuration
from . import _helpers
from . import _project


class _GeneratorBase(object):
	def __init__(self, project):
		if not isinstance(project,_project.Project):
			_helpers._errorinstance("Project",Project)
		self.project = project
		self.project.generators.add(self)

		self.configurations = []

	def isVisualStudioGenerator(self):
		return False

from . import _configuration
from . import _project


class _GeneratorBase(object):
    def __init__(self, project):
        if not isinstance(project,_project.Project):
            raise Exception("Project must be an instance of \"nobs.Project\"!")
        project.generators.add(self)
        self.project = project

        self.configurations = []

    def add_configuration(self, configuration):
        if not isinstance(configuration,_configuration.Configuration):
            raise Exception("Platform configuration must be an instance of \"nobs.Configuration\"!")
        self.configurations.append(configuration)

    def _validate_basic(self):
        for config in self.configurations:
            config._validate_basic()

from ._configuration import Configuration


class Platform(object):
    LINUX = 0
    WINDOWS = 1
    def __init__(self, search_name):
        self.configurations = []
        
        self.targets = None #Iff none, inherited from project
        
        if   search_name == "linux":
            self.type = Platform.LINUX
        elif search_name == "windows":
            self.type = Platform.WINDOWS
        else:
            raise Exception("Unrecognized platform \""+str(search_name)+"\"!  Supported platforms are { \"linux\", \"windows\" }.")

    def add_configuration(self, configuration):
        if not isinstance(configuration,Configuration):
            raise Exception("Platform configuration must be an instance of \"nobs.Configuration\"!")
        self.configurations.append(configuration)

    def _validate_basic(self):
        for config in self.configurations:
            config._validate_basic()

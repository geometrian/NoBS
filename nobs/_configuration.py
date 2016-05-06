from ._architecture import Architecture
from . import _generator_base
from ._build_options import BuildOptions
from ._toolchain import Toolchain


class Configuration(object):
    def __init__(self, generator, name, name_build, build_options, toolchain, architecture):
        if not isinstance(generator,_generator_base._GeneratorBase): raise Exception("Generator must be an instance of { \"nobs.GeneratorMSVC2015\" }!")
        generator.configurations.append(self)
        
        if not isinstance(name,str): raise Exception("Configuration name must be a string!")
        self.name = name

        if not isinstance(name_build,str): raise Exception("Configuration build name must be a string!")
        self.name_build = name_build

        if not isinstance(build_options,BuildOptions): raise Exception("Configuration build options must be an instance of \"nobs.BuildOptions\"!")
        self.build_options = build_options

        if not isinstance(toolchain,Toolchain): raise Exception("Configuration toolchain must be an instance of \"nobs.Toolchain\"!")
        self.toolchain = toolchain

        if not isinstance(architecture,Architecture): raise Exception("Configuration architecture must be an instance of \"nobs.Architecture\"!")
        self.architecture = architecture

    def _validate_basic(self):
        self.build_options._validate_basic()
        self.toolchain._validate_basic()
        self.architecture._validate_basic()

    def _get_msvc_configplat(self):
        #Return something like "debug|Win32"
        return "%s|%s" % (
            self.name,
            ["Win32","x64","ARM"][int(self.architecture.type)]
        )
    def _get_msvc_name(self):
        #Return something like "debug|x86".
        return "%s|%s" % (
            self.name,
            ["x86","x64","ARM"][int(self.architecture.type)]
        )
    def _get_msvc_arch(self):
        return ["Win32","x64","ARM"][int(self.architecture.type)]

from ._architecture import Architecture
from . import _generator_base
from . import _generator_vs
from ._build_options import BuildOptions
from ._helpers import _check_type
from ._toolchain import Toolchain


class Configuration(object):
	def __init__(self, generator, name, name_build, build_options, toolchain, architecture):
		_check_type(generator,"Generator",[_generator_vs.GeneratorVS2015,_generator_vs.GeneratorVS2017])
		self.generator = generator
		self.generator.configurations.append(self)

		_check_type(name,"Configuration name",str)
		self.name = name

		_check_type(name_build,"Configuration build name",str)
		self.name_build = name_build

		self.additional_include_directories = []

		_check_type(build_options,"Configuration build options",BuildOptions)
		self.build_options = build_options

		_check_type(toolchain,"Configuration toolchain",Toolchain)
		self.toolchain = toolchain

		_check_type(architecture,"Configuration architecture",Architecture)
		self.architecture = architecture

	def _getMSVCConfigPlat(self):
		#Return something like "debug|Win32"
		return "%s|%s" % (
			self.name,
			["Win32","x64","ARM"][int(self.architecture.type)]
		)
	def _getMSVCName    (self):
		#Return something like "debug|x86".
		return "%s|%s" % (
			self.name,
			["x86","x64","ARM"][int(self.architecture.type)]
		)
	def _getMSVCArch    (self):
		return ["Win32","x64","ARM"][int(self.architecture.type)]
	def _getMSVCArchName(self):
		return ["x86",  "x64","ARM"][int(self.architecture.type)]

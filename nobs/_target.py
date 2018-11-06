from ._define import Define
from ._file import Directory, File
from . import _project
from . import _helpers


class Export(object):
	def __init__(self, dirs_incl_list, headers_list, defs_list):
		if not isinstance(dirs_incl_list,list): raise Exception("Exported include directories must be a list!")
		for d in dirs_incl_list:
			if not isinstance(d,Directory): raise Exception("Exported includes directories must be instances of `nobs.Directory`!")
		self.dirs_incl_list = dirs_incl_list

		if not isinstance(headers_list,list): raise Exception("Headers list must be a list!")
		for header in headers_list:
			if not isinstance(header,File): raise Exception("Headers must be instances of `nobs.File`!")
		#This may be a subset of the headers in the project.
		self.headers_list = headers_list

		if not isinstance(defs_list,list): raise Exception("Exported defines must be a list!")
		for define in defs_list:
			if not isinstance(define,Define): raise Exception("Exported defines must be instances of `nobs.Define`!")
		self.defs_list = defs_list


class _TargetBase(object):
	STATIC_LIBRARY  = 0
	DYNAMIC_LIBRARY = 1
	EXECUTABLE      = 2

	def __init__(self, project, name, type, dependencies_list, pch):
		if not isinstance(project,_project.Project): raise Exception("Target's project must be an instance of `nobs.Project`!")
		self.project = project
		self.project.targets.append(self)

		if not isinstance(name,str): raise Exception("Target name must be a string!")
		self.name = name
		self.uuid = _helpers._get_uuid(self.name)

		self.type = type

		for dependency in dependencies_list:
			if not isinstance(dependency,_TargetBase):
				raise Exception("Target dependencies must also be targets!")
			if dependency.type not in [_TargetBase.STATIC_LIBRARY,_TargetBase.DYNAMIC_LIBRARY]:
				raise Exception("Target dependencies must be library targets!")
		def _get_flattened_dependencies_list(dependencies_list):
			result = []
			def recurse(dep):
				if dep not in result:
					result.append(dep)
					for dep2 in dep.dependencies_list:
						recurse(dep2)
			for dep in dependencies_list:
				recurse(dep)
			return result
		dependencies_list_flat = _get_flattened_dependencies_list(dependencies_list)
		if self in dependencies_list_flat:
			raise Exception("Cyclic dependency requested!")
		self.dependencies_list      = dependencies_list
		self.dependencies_list_flat = dependencies_list_flat

		#Override for configurations.  If user set to a list of configurations, then those will be
		#	used instead of those in the generators.
		self.configurations_override = None

		if pch != None:
			if not isinstance(pch,tuple) or len(pch) != 2:
				raise Exception("Precompiled header must be a tuple of two files: the first being the header, the second the source!")
			for i in [0,1]:
				if not isinstance(pch[i],File): raise Exception("Path in precompiled header must be an instance of `nobs.File`!")
		self.pch = pch

class _TargetLibraryBase(_TargetBase):
	def __init__(self, project, name, type, exported, dependencies_list, pch):
		_TargetBase.__init__(self, project, name, type, dependencies_list, pch)

		if not isinstance(exported,Export):
			raise Exception("Library export must be an instance of `nobs.Export`!")
		self.exported = exported
class _TargetUserBase(object):
	def __init__(self, headers_list,sources_list):
##        if isinstance(headers_list,tuple):
##            if len(headers_list)==2 and isinstance(headers_list[0],list) and isinstance(headers_list[1],list):
##                self.headers_list        = headers_list[0]
##                self.headers_list_public = headers_list[1]
##        elif isinstance(headers_list,list):
##            self.headers_list        = headers_list
##            self.headers_list_public = headers_list
##        else:
##            raise Exception("Headers list must be a list or tuple of two lists!")
##        for header in self.headers_list:
##            if not isinstance(header,File): raise Exception("Headers must be instances of `nobs.File`!")
		if not isinstance(headers_list,list): raise Exception("Headers list must be a list!")
		for header in headers_list:
			if not isinstance(header,File): raise Exception("Headers must be instances of `nobs.File`!")
		self.headers_list = headers_list

		if not isinstance(sources_list,list): raise Exception("Sources list must be a list!")
		for source in sources_list:
			if not isinstance(source,File): raise Exception("Sources must be instances of `nobs.File`!")
		self.sources_list = sources_list

class TargetStaticLibrary(_TargetLibraryBase,_TargetUserBase):
	def __init__(self, project, name, exported, headers_list,sources_list, dependencies_list, pch=None):
		_TargetLibraryBase.__init__(self, project, name, _TargetBase.STATIC_LIBRARY, exported, dependencies_list, pch)
		_TargetUserBase.   __init__(self, headers_list,sources_list)

	def _getMSVCType(self):
		return "StaticLibrary"
class TargetDynamicLibrary(_TargetLibraryBase,_TargetUserBase):
	def __init__(self, project, name, exported, headers_list,sources_list, dependencies_list, pch=None):
		_TargetLibraryBase.__init__(self, project, name, _TargetBase.DYNAMIC_LIBRARY, exported, dependencies_list, pch)
		_TargetUserBase.   __init__(self, headers_list,sources_list)

	def _getMSVCType(self):
		return "DynamicLibrary"
##class _TargetStaticLibraryBuiltin(TargetStaticLibrary):
##    def __init__(self, name, dirs_inc_provided,dir_lib_provided):
##        TargetStaticLibrary.__init__(self, name, dirs_inc_provided,dir_lib_provided, [],[], [], None)
##class _TargetDynamicLibraryBuiltin(TargetDynamicLibrary):
##    def __init__(self, name, dirs_inc_provided,dir_lib_provided):
##        TargetDynamicLibrary.__init__(self, name, dirs_inc_provided,dir_lib_provided, [],[], [], None)
class TargetExecutable(_TargetBase,_TargetUserBase):
	def __init__(self, project, name,           headers_list,sources_list, dependencies_list, pch=None):
		_TargetBase.    __init__(self, project, name, _TargetBase.EXECUTABLE, dependencies_list, pch)
		_TargetUserBase.__init__(self, headers_list,sources_list)

	def _getMSVCType(self):
		return "Application"


def find_target_system(name):
	...

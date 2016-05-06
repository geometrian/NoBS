from ._define import Define
from ._file import Directory, File
from . import _project
from . import _helpers


class Export(object):
    def __init__(self, dirs_incl_list, defs_list):
        if not isinstance(dirs_incl_list,list): raise Exception("Exported include directories must be a list!")
        for d in dirs_incl_list:
            if not isinstance(d,Directory): raise Exception("Exported includes directories must be instances of \"nobs.Directory\"!")
        self.dirs_incl_list = dirs_incl_list

        if not isinstance(defs_list,list): raise Exception("Exported defines must be a list!")
        for define in defs_list:
            if not isinstance(define,Define): raise Exception("Exported defines must be instances of \"nobs.Define\"!")
        self.defs_list = defs_list

class _TargetBase(object):
    STATIC_LIBRARY = 0
    DYNAMIC_LIBRARY = 1
    EXECUTABLE = 2
    def __init__(self, project, name, type, dependencies_list, pch):
        if not isinstance(project,_project.Project): raise Exception("Target's project must be an instance of \"nobs.Project\"!")
        self.project = project
        project.targets.append(self)
        
        if not isinstance(name,str): raise Exception("Target name must be a string!")
        self.name = name
        self.uuid = _helpers._get_uuid(self.name)

        self.type = type

        self.dependencies_list = dependencies_list
        for dependency in self.dependencies_list:
            if not isinstance(dependency,_TargetBase): raise Exception("Target dependencies must also be targets!")
            if dependency.type not in [_TargetBase.STATIC_LIBRARY,_TargetBase.DYNAMIC_LIBRARY]:
                raise Exception("Target dependencies must be library targets, not executables!")
        if self in self._get_flattened_dependencies_list():
            raise Exception("Cyclic dependency requested!")

        self.configurations = None #Iff none, inherited from platform

        self.pch = pch
        if self.pch != None:
            if not isinstance(self.pch,tuple) or len(self.pch) != 2:
                raise Exception("Precompiled header must be a tuple of two paths: the first to the header, the second to the source!")
            for i in [0,1]:
                if not isinstance(self.pch[i],str): raise Exception("Path in precompiled header must be either \"None\" or a string!")
                if not _helpers._validate_path(self.pch[i]): raise Exception("Could not find precompiled-headed path at \""+str(self.pch[i])+"\"!")

    def _validate_basic(self):
        pass

    def _get_flattened_dependencies_list(self):
        result = []
        def recurse(dep):
            if dep not in result:
                result.append(dep)
                for dep2 in dep.dependencies_list:
                    recurse(dep2)
        for dep in self.dependencies_list:
            recurse(dep)
        return result

class _TargetLibraryBase(_TargetBase):
    def __init__(self, project, name, type, exported, dependencies_list, pch):
        _TargetBase.__init__(self, project, name, type, dependencies_list, pch)

        if not isinstance(exported,Export):
            raise Exception("Library export must be an instance of \"nobs.Export\"!")
        self.exported = exported
class _TargetUserBase(object):
    def __init__(self, headers_list,sources_list):
        if not isinstance(headers_list,list): raise Exception("Headers list must be a list!")
        for header in headers_list:
            if not isinstance(header,File): raise Exception("Headers must be instances of \"nobs.File\"!")
        self.headers_list = headers_list

        if not isinstance(sources_list,list): raise Exception("Sources list must be a list!")
        for source in sources_list:
            if not isinstance(source,File): raise Exception("Sources must be instances of \"nobs.File\"!")
        self.sources_list = sources_list

class TargetStaticLibrary(_TargetLibraryBase,_TargetUserBase):
    def __init__(self, project, name, exported, headers_list,sources_list, dependencies_list, pch=None):
        _TargetLibraryBase.__init__(self, project, name, _TargetBase.STATIC_LIBRARY, exported, dependencies_list, pch)
        _TargetUserBase.__init__(self, headers_list,sources_list)

    def _get_msvc_type(self):
        return "StaticLibrary"
class TargetDynamicLibrary(_TargetLibraryBase,_TargetUserBase):
    def __init__(self, project, name, dirs_inc_provided,dir_lib_provided, headers_list,sources_list, dependencies_list, pch=None):
        _TargetLibraryBase.__init__(self, project, name, _TargetBase.DYNAMIC_LIBRARY, dirs_inc_provided,dir_lib_provided, dependencies_list, pch)
        _TargetUserBase.__init__(self, headers_list,sources_list)

    def _get_msvc_type(self):
        return "DynamicLibrary"
##class _TargetStaticLibraryBuiltin(TargetStaticLibrary):
##    def __init__(self, name, dirs_inc_provided,dir_lib_provided):
##        TargetStaticLibrary.__init__(self, name, dirs_inc_provided,dir_lib_provided, [],[], [], None)
##class _TargetDynamicLibraryBuiltin(TargetDynamicLibrary):
##    def __init__(self, name, dirs_inc_provided,dir_lib_provided):
##        TargetDynamicLibrary.__init__(self, name, dirs_inc_provided,dir_lib_provided, [],[], [], None)
class TargetExecutable(_TargetBase,_TargetUserBase):
    def __init__(self, project, name, headers_list,sources_list, dependencies_list, pch=None):
        _TargetBase.__init__(self, project, name, _TargetBase.EXECUTABLE, dependencies_list, pch)
        _TargetUserBase.__init__(self, headers_list,sources_list)

    def _get_msvc_type(self):
        return "Application"



















import glob
import os

try:
    from . import _helpers
except:
    import _helpers


class _FileBase(object):
    def __init__(self, rel_path):
        if not isinstance(rel_path,str): raise Exception("Relative path must be a string!")
        if not _helpers._inited: raise Exception("Must call \"nobs.init(...)\" before referencing files!")

        self.abspath = os.path.normpath(os.path.join(_helpers._script_absdir,rel_path))
        self.relpath = os.path.relpath(self.abspath,_helpers._script_absdir)
        self.absdir = os.path.dirname(self.abspath) + "/"

        self.ext = os.path.splitext(rel_path)[1].lower()
        self.is_header = self.ext in [".h",".hh",".hpp",".hxx",".h++"]
        self.is_source = self.ext in [".c",".cc",".cpp",".cxx",".c++"]

    def __str__(self):
        return "<File\n\tabspath: \"%s\"\n\trelpath: \"%s\"\n\tabsdir: \"%s\"\n\text:    \"%s\"\n>"%(self.abspath,self.relpath,self.absdir,self.ext)

class Directory(_FileBase):
    def __init__(self, rel_path):
        _FileBase.__init__(self, rel_path)

        if not os.path.exists(self.abspath):
            os.mkdir(self.abspath)

        
class File(_FileBase):
    def __init__(self, rel_path):
        _FileBase.__init__(self, rel_path)

        if not os.path.exists(self.abspath):
            raise Exception("Could not find referenced file \""+self.abspath+"\"!")

def get_files_list(rel_path_glob):
    if not isinstance(rel_path_glob,str): raise Exception("Relative path must be a string!")
    if not _helpers._inited: raise Exception("Must call \"nobs.init(...)\" before calling this function!")

    paths = glob.glob(os.path.join(_helpers._script_absdir,rel_path_glob))
    return [
        File(os.path.relpath(path)) for path in paths
    ]

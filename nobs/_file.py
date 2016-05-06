import glob
import os

try:
    from . import _helpers
except:
    import _helpers


class _FileBase(object):
    def __init__(self, relpath):
        if not isinstance(relpath,str): raise Exception("Relative path must be a string!")

        self.abspath = os.path.normpath(os.path.join(os.getcwd(),relpath))
        self.relpath = os.path.relpath(self.abspath)
        self.absdir = os.path.dirname(self.abspath) + "/"

        self.ext = os.path.splitext(relpath)[1].lower()
        self.is_header = self.ext in [".h",".hh",".hpp",".hxx",".h++"]
        self.is_source = self.ext in [".c",".cc",".cpp",".cxx",".c++"]

    def __str__(self):
        return "<File\n\tabspath: \"%s\"\n\trelpath: \"%s\"\n\tabsdir: \"%s\"\n\text:    \"%s\"\n>"%(self.abspath,self.relpath,self.absdir,self.ext)

class Directory(_FileBase):
    def __init__(self, relpath):
        _FileBase.__init__(self, relpath)

        self.abspath += "/"
        self.relpath += "/"

        if not os.path.exists(self.abspath):
            os.mkdir(self.abspath)

        
class File(_FileBase):
    def __init__(self, relpath):
        _FileBase.__init__(self, relpath)

        if not os.path.exists(self.abspath):
            raise Exception("Could not find referenced file \""+self.abspath+"\"!")

def get_files_list(path_glob):
    """Searches for files matching the given glob path.

    Note: path may be either relative or absolute."""

    if not isinstance(path_glob,str): raise Exception("Glob path must be a string!")

    paths = glob.glob(path_glob)
    return [
        File(os.path.relpath(path)) for path in paths
    ]

import glob
import os

try:
	from . import _helpers
except:
	import _helpers

from . import sys as nobs_sys


class _FileBase(object):
	def __init__(self, relpath):
		if not isinstance(relpath,str): raise Exception("Relative path must be a string!")

		cwd = os.getcwd()
		self.abspath = _helpers.reslash( os.path.normpath(os.path.join(cwd,relpath)) )
		self.relpath = _helpers.reslash( os.path.relpath(self.abspath)               )
		self.absdir  = _helpers.reslash( os.path.dirname(self.abspath) + "/"         )

		self.ext = os.path.splitext(relpath)[1].lower()
		self.is_header = self.ext in [".h",".hh",".hpp",".hxx",".h++"]
		self.is_source = self.ext in [".c",".cc",".cpp",".cxx",".c++"]

		self.is_in_nobs_sys_dir = _helpers.reslash(os.path.commonpath((nobs_sys.NOBS_SYS_DIR,self.abspath))+"/" ) == nobs_sys.NOBS_SYS_DIR

	def __repr__(self):
		return str(self)
	def __str__(self):
		return "<File: \""+self.abspath+"\"\n>"

class Directory(_FileBase):
	def __init__(self, relpath):
		_FileBase.__init__(self, relpath)

		self.abspath += "/"
		self.relpath += "/"

		def _make_as_necessary(d):
			if not os.path.exists(d):
				_make_as_necessary( os.path.normpath(os.path.join(d,"../")) )
				os.mkdir(d)
		_make_as_necessary(self.abspath)

class File(_FileBase):
	def __init__(self, relpath):
		_FileBase.__init__(self, relpath)

		if not os.path.exists(self.abspath):
			raise Exception("Could not find referenced file \""+self.abspath+"\"!")


def get_files_list(path_glob):
	"""
Searches for files matching the given glob path.

Note: path may be either relative or absolute.
	"""

	if not isinstance(path_glob,str): raise Exception("Glob path must be a string!")

	paths = glob.glob(path_glob, recursive=True)
	return [
		File(os.path.relpath(path)) for path in paths
	]

import re
import os, sys
import shutil

sys.path.append("../")
import nobs

from __helpers import *


def get_filename():
	dt, page = nobs.download_to_mem("http://www.libpng.org/pub/png/libpng.html")
	page = page.decode("utf-8")

	#E.g. """<FONT SIZE="+1"><B>1.6.35</B></FONT>"""
	match = re.search("(?<=(<FONT SIZE=\\\"\\+1\\\"><B>))\d+\.\d+\.\d+(?=(</B></FONT>))", page)
	if match==None: raise Exception("Could not automatically determine latest libpng version!  May need to update \"%s\"."%__file__)
	else:           verstr=match.group(0)

	return dt, "https://download.sourceforge.net/libpng/", "libpng", verstr, "libpng-"+verstr+".tar.xz"

def additional_project_setup_fromrootdir():
	shutil.copyfile("scripts/pnglibconf.h.prebuilt","pnglibconf.h")

def get_system_projecttargets_fromrootdir():
	prj = nobs.Project(
		"libpng",
		nobs.Directory("."), nobs.Directory(".nobs/.build/"), nobs.Directory(".nobs/.build/"), nobs.Directory(".nobs/.ides/")
	)

	gen_vs = make_standard_system_config(prj)

	target = nobs.TargetStaticLibrary(prj,
		"libpng",
		nobs.Export(
			[                                                 ], #Exported additional definitions
			[ nobs.Directory("../../../Include/user/libpng/") ], #Exported include directories
			[ nobs.File("png.h")                              ], #Exported headers
			[ nobs.Directory("../../../Lib/user/libpng/")     ]  #Exported libraries root directories
		),
		nobs.get_files_list("png*.h"),
		nobs.get_files_list("png*.c"),
		[ get_system_target("zlib") ], #Dependencies
		None #PCH (optional: tuple (header,source) or default None)
	)

	return prj, [target]

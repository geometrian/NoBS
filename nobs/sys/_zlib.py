import re
import os, sys

sys.path.append("../")
import nobs

from __helpers import *


def get_filename():
	dt, page = nobs.download_to_mem("http://zlib.net/")
	page = page.decode("utf-8")

	#E.g. """<FONT SIZE="+2"><B> zlib 1.2.11</B></FONT>"""
	match = re.search("(?<=(<FONT SIZE=\\\"\\+2\\\"><B> zlib ))\d+\.\d+\.\d+(?=(</B></FONT>))", page)
	if match==None: raise Exception("Could not automatically determine latest zlib version!  May need to update \"%s\"."%__file__)
	else:           verstr=match.group(0)

	return dt, "http://zlib.net/", "zlib", verstr, "zlib-"+verstr+".tar.gz"

def additional_project_setup_fromrootdir():
	print("  Cleaning up \"contrib/masmx86/bld_ml32.bat\".")
	os.chdir("contrib/masmx86/")
	replace_file_if_hashmatch_or_fail(
		"bld_ml32.bat",

		"b0b05b62715d4a81a7db5b7ca4a372d109ec95634c9d3bef9e0041ff52de22fc",

		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\ml.exe\" /coff /Zi /c /safeseh /Flmatch686.lst match686.asm\n"+
		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\ml.exe\" /coff /Zi /c /safeseh /Flinffas32.lst inffas32.asm\n"
	)
	nobs.run_subproc("bld_ml32.bat")
	os.chdir("../../")

	print("  Cleaning up \"contrib/masmx64/bld_ml64.bat\".")
	os.chdir("contrib/masmx64/")
	replace_file_if_hashmatch_or_fail(
		"bld_ml64.bat",

		"1c0561908a07ebdff271b12ed757241e1813d3db0f3551501b2595c23f0833aa",

		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\x86_amd64\\ml64.exe\" /Flinffasx64 /c /Zi inffasx64.asm\n"+
		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\x86_amd64\\ml64.exe\" /Flgvmat64   /c /Zi gvmat64.asm\n"
	)
	nobs.run_subproc("bld_ml64.bat")
	os.chdir("../../")

def get_system_projecttargets_fromrootdir():
	prj = nobs.Project(
		"zlib",
		nobs.Directory("."), nobs.Directory(".nobs/.build/"), nobs.Directory(".nobs/.build/"), nobs.Directory(".nobs/.ides/")
	)

	gen_vs = make_standard_system_config(prj)

	for config in gen_vs.configurations:
		config.additional_include_directories.append(nobs.Directory("."))
		config.additional_include_directories.append(nobs.Directory("contrib/masmx86/"))

	target = nobs.TargetStaticLibrary(prj,
		"zlib",
		nobs.Export(
			[                                               ], #Exported additional definitions
			[ nobs.Directory("../../../Include/user/zlib/") ], #Exported include directories
			[ nobs.File("zconf.h"), nobs.File("zlib.h" )    ], #Exported headers
			[ nobs.Directory("../../../Lib/user/zlib/")     ]  #Exported libraries root directories
		),
		nobs.get_files_list("*.h"),
		nobs.get_files_list("*.c") + [
			nobs.File("contrib/masmx64/inffas8664.c"),
			nobs.File("contrib/minizip/ioapi.c"     ),
			nobs.File("contrib/minizip/unzip.c"     ),
			nobs.File("contrib/minizip/zip.c"       ),
		],
		[], #Dependencies
		None #PCH (optional: tuple (header,source) or default None)
	)

	return prj, [target]

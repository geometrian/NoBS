import re
import os,sys; sys.path.append("../../")

import dependency
import nobs


def get_filename_zlib():
	dt, page = nobs.download_to_mem("http://zlib.net/")
	page = page.decode("utf-8")

	#E.g. """<FONT SIZE="+2"><B> zlib 1.2.11</B></FONT>"""
	match = re.search("(?<=(<FONT SIZE=\\\"\\+2\\\"><B> zlib ))\d+\.\d+\.\d+(?=(</B></FONT>))", page)
	if match == None:
		raise Exception(
			"Could not automatically determine latest zlib version!  May need to update \"%s\"." % __file__
		)
	else:
		verstr = match.group(0)
	return dt, "http://zlib.net/", "zlib", verstr, "zlib-"+verstr+".tar.gz"

def prepare_dep_zlib():
	print("  Cleaning up \"contrib/masmx86/bld_ml32.bat\".")
	os.chdir("contrib/masmx86/")
	dependency.replace_file_if_hashmatch_or_fail(
		"bld_ml32.bat",

		"b0b05b62715d4a81a7db5b7ca4a372d109ec95634c9d3bef9e0041ff52de22fc",

		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\ml.exe\" /coff /Zi /c /safeseh /Flmatch686.lst match686.asm\n"+
		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\ml.exe\" /coff /Zi /c /safeseh /Flinffas32.lst inffas32.asm\n"
	)
	nobs.run_subproc("bld_ml32.bat")
	os.chdir("../../")

	print("  Cleaning up \"contrib/masmx64/bld_ml64.bat\".")
	os.chdir("contrib/masmx64/")
	dependency.replace_file_if_hashmatch_or_fail(
		"bld_ml64.bat",

		"1c0561908a07ebdff271b12ed757241e1813d3db0f3551501b2595c23f0833aa",

		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\x86_amd64\\ml64.exe\" /Flinffasx64 /c /Zi inffasx64.asm\n"+
		b"\"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\x86_amd64\\ml64.exe\" /Flgvmat64   /c /Zi gvmat64.asm\n"
	)
	nobs.run_subproc("bld_ml64.bat")
	os.chdir("../../")

def nobs_generate_zlib(vername):
	prj = nobs.Project(
		vername,
		nobs.Directory("."            ),
		nobs.Directory(".nobs/.build/"),
		nobs.Directory(".nobs/.build/"),
		nobs.Directory(".nobs/.ides/" )
	)

	gen_vs = nobs.GeneratorVS(prj)

	opts_deb_s = nobs.BuildOptions("debug"               )
	opts_rel_s = nobs.BuildOptions("release-with-symbols")
	for opts in [opts_deb_s,opts_rel_s]:
		opts.setStdLibStatic();
		opts.simd = nobs.BuildOptions.SIMD_SSE4_2

	toolchain_intel = nobs.Toolchain("intel")
	toolchain_msvc  = nobs.Toolchain("msvc" )

	nobs.Configuration( gen_vs,    "debug-msvc-static",    "win-deb-x32-msvc-s",  opts_deb_s, toolchain_msvc,  nobs.Architecture("x86"   ) )
	nobs.Configuration( gen_vs,    "debug-msvc-static",    "win-deb-x64-msvc-s",  opts_deb_s, toolchain_msvc,  nobs.Architecture("x86-64") )
	nobs.Configuration( gen_vs,    "release-msvc-static",  "win-rel-x32-msvc-s",  opts_rel_s, toolchain_msvc,  nobs.Architecture("x86"   ) )
	nobs.Configuration( gen_vs,    "release-msvc-static",  "win-rel-x64-msvc-s",  opts_rel_s, toolchain_msvc,  nobs.Architecture("x86-64") )
	#nobs.Configuration( gen_vs,    "debug-intel-static",   "win-deb-x32-intel-s", opts_deb_s, toolchain_intel, nobs.Architecture("x86"   ) )
	#nobs.Configuration( gen_vs,    "debug-intel-static",   "win-deb-x64-intel-s", opts_deb_s, toolchain_intel, nobs.Architecture("x86-64") )
	#nobs.Configuration( gen_vs,    "release-intel-static", "win-rel-x32-intel-s", opts_rel_s, toolchain_intel, nobs.Architecture("x86"   ) )
	#nobs.Configuration( gen_vs,    "release-intel-static", "win-rel-x64-intel-s", opts_rel_s, toolchain_intel, nobs.Architecture("x86-64") )
	for config in gen_vs.configurations:
		config.additional_include_directories.append(nobs.Directory("."))
		config.additional_include_directories.append(nobs.Directory("contrib/masmx86/"))

	nobs.TargetStaticLibrary(prj,
		vername,
		nobs.Export(
			[nobs.Directory("../../../Include/user/")], #Include directories
			[
				nobs.File("zconf.h"),
				nobs.File("zlib.h" )
			],
			[] #Additional definitions
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

	prj.generate()

	return prj

dependency.setup_dependency(
	get_filename_zlib, prepare_dep_zlib, nobs_generate_zlib
)

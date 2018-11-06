import os, sys

sys.path.append("../")
import nobs


NOBS_SYS_DIR = "C:/dev/Python Projects/Prebuilt and Programming Utilities/NoBS/nobs-sys/"
##NOBS_SYS_DIR = "C:/Program Files (x86)/Windows Kits/10/"


#http://stackoverflow.com/a/28382515/688624
#if sys.platform == "win32":
#	def symlink_ms(source, link):
#		if not os.path.isabs(source): source=os.path.join(os.getcwd(),source)
#		if not os.path.isabs(link  ): link  =os.path.join(os.getcwd(),link  )
#		orig_cwd = os.getcwd() + "/"
#		if os.path.isdir(source):
#			os.chdir(link+"../")
#			link = os.path.basename(link[:-1])
#			source = source[:-1]
###            print("  CWD: \"%s\""%os.getcwd())
###            print("  link (dir): \"%s\""%link)
###            print("  src  (dir): \"%s\""%source)
#			nobs.run_subproc("mklink /D \"%s\" \"%s\""%(link.replace("/","\\"),source.replace("/","\\")),False)
#		else:
#			os.chdir(os.path.dirname(link))
#			link = os.path.basename(link)
###            print("  CWD: \"%s\""%os.getcwd())
###            print("  link (file): \"%s\""%link)
###            print("  src  (file): \"%s\""%source)
#			nobs.run_subproc("mklink \"%s\" \"%s\""%(link.replace("/","\\"),source.replace("/","\\")),False)
#		os.chdir(orig_cwd)
#	os.symlink = symlink_ms

def replace_file_if_hashmatch_or_fail(relpath, req_orig_hash, new_contents):
	if nobs.get_file_hash(relpath) == req_orig_hash:
		file = open(relpath,"wb")
		file.write(new_contents)
		file.close()
	else:
		raise Exception("Could not update file contents; file has changed!  Update \"%s\"."%__file__)

def safe_create_dir(path):
	if os.path.isdir(path) and not dir_is_empty(path):
		reply = nobs.strinput("Directory \"%s\" already exists!  Should I delete it (y/n)?  "%path)
		if reply == "y":
			shutil.rmtree(path)
		else:
			print("Abort."); sys.exit()
		nobs.Directory(path)
		print("  Recreated \"%s\""%path)
	else:
		nobs.Directory(path)
		print("  Created \"%s\""%path)

def dir_is_empty(path):
	return len(os.listdir(path)) == 0

def make_standard_system_config(prj):
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

	return gen_vs

def get_system_target(name):
	try:
		module = __import__("_"+name)
	except ModuleNotFoundError:
		raise Exception(
			"Unrecognized system target \""+name+"\"!"
		)

	orig_cwd = os.getcwd()
	path = NOBS_SYS_DIR+"Source/user/"+name+"/"
	if not os.path.exists(path):
		raise Exception("Unrecognized system target \""+name+"\"!")
	os.chdir(path)

	#cwd = os.getcwd()
	#cwd = path if not os.path.islink(cwd) else os.readlink(cwd) #Workaround for `os.path.realpath(...)` being broken
	#vername = os.path.split(cwd)[1]
	prj, targets = module.get_system_projecttargets_fromrootdir()

	os.chdir(orig_cwd)
	return targets[0]

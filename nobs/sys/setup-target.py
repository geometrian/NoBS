import os, sys
import shutil
import subprocess
import tarfile

sys.path.append("../")
import nobs

from __helpers import *


def setup_target(modulename):
	module = __import__("_"+modulename)

	orig_cwd = os.getcwd()

	#Parse dependency's website to get file
	print("Parsing the dependency's website to get file information.")
	try:
		dt, urlprefix, name, verstr, filename = module.get_filename()
		#dt, urlprefix, name, verstr, filename = 0.0, "http://zlib.net/", "zlib", "1.2.11", "zlib-1.2.11.tar.gz"
	except Exception as e:
		print("  Parse failed: \"%s\""%e)
		print("Abort."); sys.exit()
	print("  Downloaded and parsed in ~%dms."%( int(round(1000.0*dt)) ))
	print("  Current version appears to be \"%s\"."%verstr)
	vername = name+"-"+verstr

	#Create directories
	print("Creating directories.")
	nobs.Directory(NOBS_SYS_DIR)
	os.chdir(NOBS_SYS_DIR)
	safe_create_dir("Include/user/"+   vername+"/")
	safe_create_dir(    "Lib/user/"+   vername+"/")
	safe_create_dir( "Source/user/"+   vername+"/")
	nobs.Directory(  "Source/user/download-cache/")

	#Download dependency
	print("Attempting to download dependency.")
	os.chdir("Source/user/download-cache/")
	if os.path.isfile(filename):
		print("  Using cached download.")
	else:
		dt = nobs.download_to_file(urlprefix+filename,filename,nobs.download_progress_callback_simple)
		print("  Downloaded in %f seconds."%round(dt,3))
	os.chdir("../")

	#Extract dependency
	print("Extracting dependency.")
	tar = tarfile.open("download-cache/"+filename)
	tar.extractall() #Extracts to CWD, apparently.
	tar.close()

	#Prepare dependency for build
	print("Preparing dependency for build.")
	os.chdir(vername+"/")
	module.additional_project_setup_fromrootdir()

	#Generate build files with NoBS
	print("Generating build files.")
	prj, targets = module.get_system_projecttargets_fromrootdir()
	prj.generate()

	#Build dependency
	print("Building dependency.")
	os.chdir(".nobs/.ides/")
	msbuild = "\"C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/MSBuild.exe\""
	cmd1 = "%s %s.sln /nologo /verbosity:minimal /maxcpucount:8" % (msbuild,name)
	for gen in prj.generators:
		if gen.isVisualStudioGenerator():
			for config in gen.configurations:
				cmd2 = cmd1 + " /p:Configuration=%s /p:Platform=\"%s\""%(config.name,config._getMSVCArchName())
				nobs.run_subproc(cmd2)

	#Install
	print("Installing dependency.")
	os.chdir("../../../../../")
	#	"Include/"
	nobs.overwrite_symlink("Include/user/"+vername+"/","Include/user/"+name+"/",2)
	for target in prj.targets:
		for header in target.exported.headers_list:
			src = nobs.reslash(header.abspath)
			prefix = NOBS_SYS_DIR + "Source/user/"+vername+"/"
			assert src.startswith(prefix)
			subpath = src[len(prefix):]
			nobs.overwrite_symlink(
				src,
				"Include/user/"+vername+"/"+subpath,
				2
			)
	#	"Lib/"
	nobs.overwrite_symlink("Lib/user/"+vername+"/","Lib/user/"+name+"/",2)
	for gen in prj.generators:
		if gen.isVisualStudioGenerator():
			for config in gen.configurations:
				nobs.Directory("Lib/user/"+vername+"/"+config.name_build+"/")
				nobs.overwrite_symlink(
					"Source/user/"+vername+"/.nobs/.build/"+config.name_build+"/"+name+".lib",
					"Lib/user/"+vername+"/"+config.name_build+"/"+name+".lib",
					2
				)
	#	"Source/"
	nobs.overwrite_symlink("Source/user/"+vername+"/","Source/user/"+name+"/",2)

	#Cleanup
	print("Cleaning up.")
	os.chdir(orig_cwd)

	#Done
	print("Done!")

def setup_targets_all():
	selfdir = os.path.dirname(__file__)

	modules = []
	for filename in os.listdir(selfdir):
		if filename.startswith("_") and not filename.startswith("__"):
			modules.append(os.path.splitext(filename)[0][1:])

	for modulename in modules:
		setup_target(modulename)
def setup_targets_named():
	#setup_target("zlib")
	setup_target("libpng")

def main():
	#setup_targets_all()
	setup_targets_named()

if __name__ == "__main__": main()

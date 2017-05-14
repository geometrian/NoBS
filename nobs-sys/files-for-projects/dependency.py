import os,sys; sys.path.append("../../")
import shutil
import subprocess
import tarfile

import nobs


def replace_file_or_fail(relpath, req_orig_hash, new_contents):
    if nobs.get_file_hash(relpath) == req_orig_hash:
        file = open(relpath,"wb")
        file.write(new_contents)
        file.close()
    else:
        raise Exception("Could not update file contents; file has changed!  Update \"%s\"."%__file__)

def setup_dependency(temp_dir, get_filename_dep,prepare_dep,nobs_generate_dep):
    orig_cwd = os.getcwd()

    #Create the build directory
    print("Creating build directory.")
##    if os.path.isdir(temp_dir):
##        reply = nobs.strinput("Temporary build directory:\n  \"%s\"\nalready exists!  Should I delete it (y/n)?  "%temp_dir)
##        if reply == "y":
##            shutil.rmtree(temp_dir)
##            os.mkdir(temp_dir)
##        else:
##            print("Abort."); sys.exit()
##    else:
##        os.mkdir(temp_dir)
    os.chdir(temp_dir)

    #Parse dependency's website to get file
    print("Parsing the dependency's website to get file.")
##    try:
##        urlprefix, name, filename = get_filename_dep()
##    except Exception as e:
##        print(e)
##        print("Abort."); sys.exit()
    urlprefix, name, filename = "http://zlib.net/", "zlib-1.2.11", "zlib-1.2.11.tar.gz"

    #Download dependency
    print("Downloading dependency.")
##    dep = nobs.download_to_file(urlprefix+filename,filename,nobs.download_progress_callback_simple)

    #Extract dependency
##    shutil.rmtree(name)
    print("Extracting dependency.")
##    tar = tarfile.open(filename)
##    tar.extractall()
##    tar.close()

    #Prepare dependency for build
    print("Preparing dependency for build.")
    os.chdir(name)
##    prepare_dep()

    #Generate build files with NoBS
    print("Generating build files.")
##    prj = nobs_generate_dep(name)

    #Build dependency
    print("Building dependency.")
    os.chdir(".nobs/.ides/")
##    msbuild = "\"C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64/MSBuild.exe\""
##    cmd1 = "%s %s.sln /nologo /verbosity:minimal /maxcpucount:8" % (msbuild,name)
##    for gen in prj.generators:
##        if gen.is_vs_gen:
##            for config in gen.configurations:
##                cmd2 = cmd1 + " /p:Configuration=%s /p:Platform=\"%s\""%(config.name,config._get_msvc_archname())
##                nobs.run_subproc(cmd2)

    #Install
    print("Installing dependency.")
    

    #Cleanup
##    print("Cleaning up.")
##    os.chdir(orig_cwd)
##    shutil.rmtree(temp_dir)

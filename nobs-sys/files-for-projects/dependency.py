import os,sys; sys.path.append("../../")
import shutil
import subprocess
import tarfile

import nobs


system_dir = "C:/dev/Python Projects/Prebuilt and Programming Utilities/NoBS/nobs-sys/files-for-projects/TestSystemDir/"
##system_dir = "C:/Program Files (x86)/Windows Kits/10/"

#http://stackoverflow.com/a/28382515/688624
if sys.platform == "win32":
    def symlink_ms(source, link):
        if not os.path.isabs(source): source=os.path.join(os.getcwd(),source)
        if not os.path.isabs(link  ): link  =os.path.join(os.getcwd(),link  )
        orig_cwd = os.getcwd() + "/"
        if os.path.isdir(source):
            os.chdir(link+"../")
            link = os.path.basename(link[:-1])
            source = source[:-1]
##            print("  CWD: \"%s\""%os.getcwd())
##            print("  link (dir): \"%s\""%link)
##            print("  src  (dir): \"%s\""%source)
            nobs.run_subproc("mklink /D \"%s\" \"%s\""%(link.replace("/","\\"),source.replace("/","\\")),False)
        else:
            os.chdir(os.path.dirname(link))
            link = os.path.basename(link)
##            print("  CWD: \"%s\""%os.getcwd())
##            print("  link (file): \"%s\""%link)
##            print("  src  (file): \"%s\""%source)
            nobs.run_subproc("mklink \"%s\" \"%s\""%(link.replace("/","\\"),source.replace("/","\\")),False)
        os.chdir(orig_cwd)
    os.symlink = symlink_ms

def overwrite_symlink(source, link):
    print("  Making \""+link+"\" -> \""+source+"\"")
    if os.path.exists(link):
##        print("  (deleting old first)")
        if os.path.isdir(link): os. rmdir(link)
        else:                   os.unlink(link)
    os.symlink(source,link)

def replace_file_or_fail(relpath, req_orig_hash, new_contents):
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
    
def setup_dependency(get_filename_dep,prepare_dep,nobs_generate_dep):
    orig_cwd = os.getcwd()

    #Parse dependency's website to get file
    print("Parsing the dependency's website to get file information.")
    try:
        dt, urlprefix, name, verstr, filename = get_filename_dep()
    except Exception as e:
        print("  Parse failed: \"%s\""%e)
        print("Abort."); sys.exit()
    print("  Downloaded and parsed in ~%dms."%( int(round(1000.0*dt)) ))
    dt, urlprefix, name, verstr, filename = 0.0, "http://zlib.net/", "zlib", "1.2.11", "zlib-1.2.11.tar.gz"
    print("  Current version appears to be \"%s\"."%verstr)
    vername = name+"-"+verstr

    #Create directories
    print("Creating directories.")
    os.chdir(system_dir)
    safe_create_dir("Include/user/"+vername+"/")
    safe_create_dir("Lib/user/"+vername+"/")
    safe_create_dir("Source/user/"+vername+"/")
    nobs.Directory("Source/user/download-cache/")

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
    prepare_dep()

    #Generate build files with NoBS
    print("Generating build files.")
    prj = nobs_generate_dep(vername)

    #Build dependency
    print("Building dependency.")
    os.chdir(".nobs/.ides/")
    msbuild = "\"C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/amd64/MSBuild.exe\""
    cmd1 = "%s %s.sln /nologo /verbosity:minimal /maxcpucount:8" % (msbuild,vername)
    for gen in prj.generators:
        if gen.is_vs_gen:
            for config in gen.configurations:
                cmd2 = cmd1 + " /p:Configuration=%s /p:Platform=\"%s\""%(config.name,config._get_msvc_archname())
                nobs.run_subproc(cmd2)

    #Install
    print("Installing dependency.")
    os.chdir("../../../../../")
    #   "Include/"
    overwrite_symlink("Include/user/"+vername+"/","Include/user/"+name+"/")
    for target in prj.targets:
        for header in target.exported.headers_list:
            src = nobs.reslash(header.abspath)
            prefix = system_dir + "Source/user/"+vername+"/"
            assert src.startswith(prefix)
            subpath = src[len(prefix):]
            overwrite_symlink(
                src,
                "Include/user/"+vername+"/"+subpath
            )
    #   "Lib/"
    overwrite_symlink("Lib/user/"+vername+"/","Lib/user/"+name+"/")
    for gen in prj.generators:
        if gen.is_vs_gen:
            for config in gen.configurations:
                nobs.Directory("Lib/user/"+vername+"/"+config.name_build+"/")
                overwrite_symlink(
                    "Source/user/"+vername+"/.nobs/.build/"+config.name_build+"/"+vername+".lib",
                    "Lib/user/"+vername+"/"+config.name_build+"/"+name+".lib"
                )
    #   "Source/"
    overwrite_symlink("Source/user/"+vername+"/","Source/user/"+name+"/")

    #Cleanup
    print("Cleaning up.")
    os.chdir(orig_cwd)

    #Done
    print("Done!")










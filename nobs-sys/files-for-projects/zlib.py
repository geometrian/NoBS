#=======================================================================



#User configurable section

build_dir = "C:/dev/Python Projects/Prebuilt and Programming Utilities/NoBS/NoBS/nobs-sys/files-for-projects/zlib/"

###   User should set to downloaded source distribution of package
##source_dir = "C:/Users/Ian Mallett/Desktop/zlib-1.2.8/"
###   User can change as desired; may not be compatible, though.
##verstr = "1.2.8"
###   User can change
##simd = nobs.BuildOptions.SIMD_SSE4_2

#User should not need to change below this line.



#=======================================================================

import re
import os,sys; sys.path.append("../../")
import shutil
import tarfile

import nobs


def replace_file_or_fail(relpath, req_orig_hash, new_contents):
    if nobs.get_file_hash(relpath) == req_orig_hash:
        file = open(relpath,"wb")
        file.write(new_contents)
        file.close()
    else:
        raise Exception("Could not update file contents; file has changed!  Update \"%s\"."%__file__)

def get_filename_zlib():
    page = nobs.download_to_mem("http://zlib.net/", nobs.download_progress_callback_simple).decode("utf-8")

    #E.g. """<FONT SIZE="+2"><B> zlib 1.2.11</B></FONT>"""
    match = re.search("(?<=(<FONT SIZE=\\\"\\+2\\\"><B> zlib ))\d+\.\d+\.\d+(?=(</B></FONT>))", page)
    if match == None:
        raise Exception(
            "Could not automatically determine latest zlib version!  May need to update \"%s\"." % __file__
        )
    else:
        verstr = match.group(0)
    print("Dependency version appears to be \"%s\""%verstr)

    name = "zlib-"+verstr
    filename = name+".tar.gz"
    return "http://zlib.net/", name, filename
def prepare_dep_zlib():
    os.chdir("contrib/masmx86/")
    replace_file_or_fail(
        "bld_ml32.bat",
        "b0b05b62715d4a81a7db5b7ca4a372d109ec95634c9d3bef9e0041ff52de22fc",
        b""""C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x86\\ml.exe" /safeseh /coff /Zi /c /Flmatch686.lst match686.asm
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x86\\ml.exe" /safeseh /coff /Zi /c /Flinffas32.lst inffas32.asm
"""
    )
    nobs.run_bat("bld_ml32.bat")
    os.chdir("../../")

    os.chdir("contrib/masmx64/")
    replace_file_or_fail(
        "bld_ml64.bat",
        "1c0561908a07ebdff271b12ed757241e1813d3db0f3551501b2595c23f0833aa",
        b""""C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x64\\ml64.exe" /Flinffasx64 /c /Zi inffasx64.asm
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x64\\ml64.exe" /Flgvmat64   /c /Zi gvmat64.asm
"""
    )
    nobs.run_bat("bld_ml64.bat")
    os.chdir("../../")

def setup_dependency(temp_dir, get_filename_dep,prepare_dep):
    orig_cwd = os.getcwd()

##    #Create the build directory
##    print("Creating build directory.")
##    if os.path.isdir(temp_dir):
##        reply = nobs.strinput("Temporary build directory:\n  \"%s\"\nalready exists!  Should I delete it (y/n)?  ")
##        if reply == "y":
##            shutil.rmtree(temp_dir)
##            os.mkdir(temp_dir)
##        else:
##            print("Abort."); sys.exit()
##    else:
##        os.mkdir(temp_dir)
    os.chdir(temp_dir)

    #Parse dependency's website to get file
##    print("Parse the dependency's website to get file.")
##    try:
##        urlprefix, name, filename = get_filename_dep()
##    except Exception as e:
##        print(e)
##        print("Abort."); sys.exit()
    urlprefix, name, filename = "http://zlib.net/", "zlib-1.2.11", "zlib-1.2.11.tar.gz"

    #Download dependency
##    print("Downloading dependency.")
##    dep = nobs.download_to_file(urlprefix+filename,filename,nobs.download_progress_callback_simple)

    #Extracting dependency
    shutil.rmtree(name)
    print("Extracting dependency.")
    tar = tarfile.open(filename)
    tar.extractall()
    tar.close()

    #Preparing for build
    os.chdir(name)
    prepare_dep()

    #Building dependency

    #Cleanup
##    print("Cleaning up.")
##    os.chdir(orig_cwd)
##    shutil.rmtree(temp_dir)

setup_dependency(
    build_dir,
    get_filename_zlib, prepare_dep_zlib
)
input("Done")
sys.exit(0)




os.path.dirname(os.path.abspath(__file__))

import os,sys; sys.path.append("../../")
import nobs



prj = nobs.Project(
    "zlib",
    nobs.Directory("C:/Program Files (x86)/Windows Kits/8.1/user_libs2/zlib-"+verstr+"/lib/"),
    nobs.Directory("C:/Program Files (x86)/Windows Kits/8.1/user_libs2/zlib-"+verstr+"/lib-temp/"),
    nobs.Directory("C:/Program Files (x86)/Windows Kits/8.1/user_libs2/zlib-"+verstr+"/")
)

gen_msvc  = nobs.GeneratorMSVC2015(prj)

opts_deb_d = nobs.BuildOptions("debug");                opts_deb_d.set_dynamic_stdlib()
opts_rel_d = nobs.BuildOptions("release-with-symbols"); opts_rel_d.set_dynamic_stdlib()
opts_deb_s = nobs.BuildOptions("debug");                opts_deb_s.set_static_stdlib()
opts_rel_s = nobs.BuildOptions("release-with-symbols"); opts_rel_s.set_static_stdlib()
for opts in [opts_deb_d,opts_rel_d,opts_deb_s,opts_rel_s]:
    opts.simd = simd

toolchain_msvc  = nobs.Toolchain("msvc-2015")
toolchain_clang = nobs.Toolchain("clang-3.7")
toolchain_intel = nobs.Toolchain("intel-16.0")

arch_x86 = nobs.Architecture("x86"   )
arch_x64 = nobs.Architecture("x86-64")

for toolchain_name,toolchain in [("msvc",toolchain_msvc),("clang",toolchain_clang),("intel",toolchain_intel)]:
    for arch_name,arch in [("x86",arch_x86),("x64",arch_x64)]:
        for ds,drs,dr,opts in [
            ("d","deb","debug",opts_deb_d),
            ("d","rel","release",opts_rel_d),
            ("s","deb","debug",opts_deb_s),
            ("s","rel","release",opts_rel_s)
        ]:
            nobs.Configuration( gen_msvc, dr, toolchain_name+"-"+arch_name+"-"+ds+"-"+drs, opts, toolchain, arch )

target_mylib = nobs.TargetStaticLibrary(prj,
    "zlib",
    nobs.Export(
        [nobs.Directory(".")], #Include directories
        [] #Additional definitions
    ),
    nobs.get_files_list("mylib/*.h"),
    nobs.get_files_list("mylib/*.cpp"),
    [], #Dependencies
    None #PCH (optional: tuple (header,source) or default None)
)
#   Define an executable as a build target, depending on "target_mylib".  Note: because
#       "target_mylib" depends on "target_zlib", that will be added as a dependency
#       automatically.  However, if you specified it again, NoBS is smart enough not to
#       include it as a dependency twice.
target_myexec = nobs.TargetExecutable(prj,
    "My Executable",
    nobs.get_files_list("myexec/*.h"),
    nobs.get_files_list("myexec/*.cpp"),
    [target_mylib]
)

prj.generate()





















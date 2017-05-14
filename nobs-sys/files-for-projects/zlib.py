import re
import os,sys; sys.path.append("../../")

import dependency
import nobs


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
    dependency.replace_file_or_fail(
        "bld_ml32.bat",
        "b0b05b62715d4a81a7db5b7ca4a372d109ec95634c9d3bef9e0041ff52de22fc",
        b""""C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x86\\ml.exe" /safeseh /coff /Zi /c /Flmatch686.lst match686.asm
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x86\\ml.exe" /safeseh /coff /Zi /c /Flinffas32.lst inffas32.asm
"""
    )
    nobs.run_subproc("bld_ml32.bat")
    os.chdir("../../")

    os.chdir("contrib/masmx64/")
    dependency.replace_file_or_fail(
        "bld_ml64.bat",
        "1c0561908a07ebdff271b12ed757241e1813d3db0f3551501b2595c23f0833aa",
        b""""C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x64\\ml64.exe" /Flinffasx64 /c /Zi inffasx64.asm
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.10.25017\\bin\\HostX64\\x64\\ml64.exe" /Flgvmat64   /c /Zi gvmat64.asm
"""
    )
    nobs.run_subproc("bld_ml64.bat")
    os.chdir("../../")
def nobs_generate_zlib(versioned_name):
    prj = nobs.Project(
        versioned_name,
        nobs.Directory(".nobs/.build/"),      #Build result directory
        nobs.Directory(".nobs/.build-temp/"), #Build temp directory
        nobs.Directory(".nobs/.ides/")        #Build files directory
    )
    
    gen_vs = nobs.GeneratorVS(prj)

    opts_deb = nobs.BuildOptions("debug")
    opts_rel = nobs.BuildOptions("release-with-symbols")
    for opts in [opts_deb,opts_rel]:
        opts.set_static_stdlib();
        opts.simd = nobs.BuildOptions.SIMD_SSE4_2

    toolchain_msvc  = nobs.Toolchain("msvc")
    toolchain_intel = nobs.Toolchain("intel")

    nobs.Configuration( gen_vs, "msvc-s-deb", "win-deb-x32-msvc-s", opts_deb, toolchain_msvc, nobs.Architecture("x86"   ) )
    nobs.Configuration( gen_vs, "msvc-s-deb", "win-deb-x64-msvc-s", opts_deb, toolchain_msvc, nobs.Architecture("x86-64") )
    nobs.Configuration( gen_vs, "msvc-s-rel", "win-rel-x32-msvc-s", opts_rel, toolchain_msvc, nobs.Architecture("x86"   ) )
    nobs.Configuration( gen_vs, "msvc-s-rel", "win-rel-x64-msvc-s", opts_rel, toolchain_msvc, nobs.Architecture("x86-64") )
##    nobs.Configuration( gen_vs, "intel-s-deb", "win-deb-x32-intel-s", opts_deb, toolchain_intel, nobs.Architecture("x86"   ) )
##    nobs.Configuration( gen_vs, "intel-s-deb", "win-deb-x64-intel-s", opts_deb, toolchain_intel, nobs.Architecture("x86-64") )
##    nobs.Configuration( gen_vs, "intel-s-rel", "win-rel-x32-intel-s", opts_rel, toolchain_intel, nobs.Architecture("x86"   ) )
##    nobs.Configuration( gen_vs, "intel-s-rel", "win-rel-x64-intel-s", opts_rel, toolchain_intel, nobs.Architecture("x86-64") )
    for config in gen_vs.configurations:
        config.additional_include_directories.append(nobs.Directory("."))
        config.additional_include_directories.append(nobs.Directory("contrib/masmx86/"))

    nobs.TargetStaticLibrary(prj,
        "zlib",
        nobs.Export(
            [nobs.Directory(".")], #Include directories
            [] #Additional definitions
        ),
        #Global headers:
        #   ./zconf.h
        #   ./zlib.h
        nobs.get_files_list("*.h"),
        nobs.get_files_list("*.c") + [
            nobs.File("contrib/masmx64/inffas8664.c"),
            nobs.File("contrib/minizip/ioapi.c"),
            nobs.File("contrib/minizip/unzip.c"),
            nobs.File("contrib/minizip/zip.c"),
        ],
        [], #Dependencies
        None #PCH (optional: tuple (header,source) or default None)
    )

    prj.generate()

    return prj
    
dependency.setup_dependency(
    "zlib-temp/",
    get_filename_zlib, prepare_dep_zlib, nobs_generate_zlib
)













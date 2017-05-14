import os,sys; sys.path.append("../")
import nobs

#Mental model of hierarchy of a NoBS-managed project:
#    --Project
#        --Name
#        --Build result directory
#        --Build temporary directory
#        --Build files directory
#        --Set of generators, each with
#            --List of configurations (user-ordered), each with
#                --Name
#                --Additional include directories
#                --Standard build options
#                    --"debug", "release", "release-with-symbols"
#                    --Defines
#                    --SIMD instruction set
#                --Toolchain
#                    --Compiler/assembler/linker
#                    --Additional defines
#                    --Additional build options
#                --Architecture
#            --Optional exclusions/overrides of list of targets to appear
#        --List of targets (auto-sorted, accounting for dependencies), each with
#            --Type
#            --Name
#            --Exported incl/lib directories and defines (libraries only)
#            --Headers list
#            --Sources list
#            --Dependencies, each with
#                --Include directories list
#                --Libraries directories list
#                --Library targets list
#            --Optional exclusion of a given configuration
#            --Optional extensions/overrides for a given configuration
#                --Additional defines
#                --Additional build options
#                --Additional dependencies
#                --Exports

#The return-values of all the below functions are objects which have additional
#   properties, which you might enjoy customizing (see docs).

#Change current working directory to be that of this file, if it wasn't already.
os.chdir( os.path.dirname(os.path.abspath(__file__)) )

#Project: contains all targets in your project
prj = nobs.Project(
    "My Project",
    nobs.Directory(".build/"),      #Build result directory
    nobs.Directory(".build-temp/"), #Build temp directory
    nobs.Directory(".ides/")        #Build files directory
)

#Generators: describes desired build files
##gen_gmake = nobs.GeneratorGMake(prj)
gen_vs  = nobs.GeneratorVS2017(prj)

#Configurations: ways to generate the targets in your project.  By default, each target
#   inherits all configurations, but targets may exclude themselves from or customize
#   any given configuration.
opts_deb = nobs.BuildOptions("debug")
opts_rel = nobs.BuildOptions("release-with-symbols")
opts_deb.set_dynamic_stdlib(); opts_deb.simd=nobs.BuildOptions.SIMD_SSE4_2
opts_rel.set_dynamic_stdlib(); opts_rel.simd=nobs.BuildOptions.SIMD_SSE4_2
    
toolchain_gcc   = nobs.Toolchain("gcc-7.1")
toolchain_clang = nobs.Toolchain("clang-4.0.0")
toolchain_msvc  = nobs.Toolchain("msvc-2017")
toolchain_intel = nobs.Toolchain("intel-17.0")
##nobs.Configuration( gen_gmake, "gcc-s-deb", "lin-deb-x32-gcc-s", opts_deb, toolchain_gcc,  nobs.Architecture("x86"   ) )
##nobs.Configuration( gen_gmake, "gcc-s-deb", "lin-deb-x64-gcc-s", opts_deb, toolchain_gcc,  nobs.Architecture("x86-64") )
##nobs.Configuration( gen_gmake, "gcc-s-rel", "lin-deb-x32-gcc-s", opts_rel, toolchain_gcc,  nobs.Architecture("x86"   ) )
##nobs.Configuration( gen_gmake, "gcc-s-rel", "lin-deb-x64-gcc-s", opts_rel, toolchain_gcc,  nobs.Architecture("x86-64") )
##nobs.Configuration( gen_gmake, "clang-s-deb", "lin-deb-x32-clang-s", opts_deb, toolchain_clang,  nobs.Architecture("x86"   ) )
##nobs.Configuration( gen_gmake, "clang-s-deb", "lin-deb-x64-clang-s", opts_deb, toolchain_clang,  nobs.Architecture("x86-64") )
##nobs.Configuration( gen_gmake, "clang-s-rel", "lin-deb-x32-clang-s", opts_rel, toolchain_clang,  nobs.Architecture("x86"   ) )
##nobs.Configuration( gen_gmake, "clang-s-rel", "lin-deb-x64-clang-s", opts_rel, toolchain_clang,  nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs, "msvc-s-deb", "win-deb-x32-msvc-s", opts_deb, toolchain_msvc, nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs, "msvc-s-deb", "win-deb-x64-msvc-s", opts_deb, toolchain_msvc, nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs, "msvc-s-rel", "win-rel-x32-msvc-s", opts_rel, toolchain_msvc, nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs, "msvc-s-rel", "win-rel-x64-msvc-s", opts_rel, toolchain_msvc, nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs, "intel-s-deb", "win-deb-x32-intel-s", opts_deb, toolchain_intel, nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs, "intel-s-deb", "win-deb-x64-intel-s", opts_deb, toolchain_intel, nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs, "intel-s-rel", "win-rel-x32-intel-s", opts_rel, toolchain_intel, nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs, "intel-s-rel", "win-rel-x64-intel-s", opts_rel, toolchain_intel, nobs.Architecture("x86-64") )

#Targets: all build targets (executables, libraries) relevant to your project.  If you
#   add them, they will be built.

#   Get a target static or dynamic library that's expected to be on the system.  Many
#       are pre-defined for you.  You can always tweak them or add your own in "nobs-sys/".
##target_zlib = nobs.find_target_system("zlib")

#   Define a static library as a build target, depending on "target_zlib".
target_mylib = nobs.TargetStaticLibrary(prj,
    "My Library",
    nobs.Export(
        [nobs.Directory(".")], #Include directories
        [] #Additional definitions
    ),
    nobs.get_files_list("mylib/*.h") + nobs.get_files_list("mylib/*"),
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
    [ #dependencies
        target_mylib
    ]
)

#Generate project files
prj.generate()





















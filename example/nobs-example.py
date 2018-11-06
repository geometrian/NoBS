#Mental model of hierarchy of a NoBS-managed project:
#
#	• Project:
#
#		• Name
#
#		• Project root directory
#		• Directory for build result
#		• Directory for build temporaries
#		• Directory for project files
#
#		• Set of generators, each with:
#
#			• List of configurations (user-ordered), each with:
#
#				• Name
#				• Additional include directories
#				• Standard build options
#					• Basic type; one of: { "debug", "release", "release-with-symbols" }
#					• Defines
#					• SIMD instruction set
#				• Toolchain
#					• Compiler/assembler/linker
#					• Additional defines
#					• Additional build options
#				• Architecture
#
#			• Optional exclusions/overrides of list of targets to appear
#
#		• List of targets (auto-sorted, accounting for dependencies), each with:
#
#			• Type
#
#			• Name
#
#			• Exported incl/lib directories and defines (libraries only)
#
#			• Headers listW
#			• Sources list
#
#			• Dependencies, each with:
#				• Include directories list
#				• Libraries directories list
#				• Library targets list
#
#			• Optional exclusion of a given configuration
#			• Optional extensions/overrides for a given configuration
#				• Additional defines
#				• Additional build options
#				• Additional dependencies
#				• Exports


import os,sys; sys.path.append("../")

import nobs
import nobs.sys


#The return-values of all the below functions are objects which have additional properties, which
#	you might enjoy customizing (see docs).


#Change current working directory to be that of this file, if it wasn't already.  This must be the
#	root directory of your project!
os.chdir( os.path.dirname(os.path.abspath(__file__)) )

#Project: contains all targets in your project
prj = nobs.Project(
	"My Project",
	nobs.Directory("."      ), #Project root directory
	nobs.Directory(".build/"), #Build result directory
	nobs.Directory(".build/"), #Build temp directory
	nobs.Directory(".ides/" )  #Project files directory
)

#Generators: describes desired build files
#gen_gmake = nobs.GeneratorGMake(prj)
gen_vs    = nobs.GeneratorVS   (prj)

#Configurations: ways to generate the targets in your project.  By default, each target inherits all
#	configurations, but targets may exclude themselves from or customize any given configuration.

#	Build options
opts_deb_s = nobs.BuildOptions("debug"               )
opts_rel_s = nobs.BuildOptions("release-with-symbols")
for opts in [opts_deb_s,opts_rel_s]:
	opts.setStdLibStatic()
	opts.simd = nobs.BuildOptions.SIMD_SSE4_2

#	Toolchains
toolchain_gcc   = nobs.Toolchain("gcc"  )
toolchain_clang = nobs.Toolchain("clang")
toolchain_intel = nobs.Toolchain("intel")
toolchain_msvc  = nobs.Toolchain("msvc" )

#	Configurations
#nobs.Configuration( gen_gmake, "gcc-s-deb",   "lin-deb-x32-gcc-s",   opts_deb_s, toolchain_gcc,   nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_gmake, "gcc-s-deb",   "lin-deb-x64-gcc-s",   opts_deb_s, toolchain_gcc,   nobs.Architecture("x86-64") )
#nobs.Configuration( gen_gmake, "gcc-s-rel",   "lin-deb-x32-gcc-s",   opts_rel_s, toolchain_gcc,   nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_gmake, "gcc-s-rel",   "lin-deb-x64-gcc-s",   opts_rel_s, toolchain_gcc,   nobs.Architecture("x86-64") )
#nobs.Configuration( gen_gmake, "clang-s-deb", "lin-deb-x32-clang-s", opts_deb_s, toolchain_clang, nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_gmake, "clang-s-deb", "lin-deb-x64-clang-s", opts_deb_s, toolchain_clang, nobs.Architecture("x86-64") )
#nobs.Configuration( gen_gmake, "clang-s-rel", "lin-deb-x32-clang-s", opts_rel_s, toolchain_clang, nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_gmake, "clang-s-rel", "lin-deb-x64-clang-s", opts_rel_s, toolchain_clang, nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs,    "debug-msvc-static",    "win-deb-x32-msvc-s",  opts_deb_s, toolchain_msvc,  nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs,    "debug-msvc-static",    "win-deb-x64-msvc-s",  opts_deb_s, toolchain_msvc,  nobs.Architecture("x86-64") )
nobs.Configuration( gen_vs,    "release-msvc-static",  "win-rel-x32-msvc-s",  opts_rel_s, toolchain_msvc,  nobs.Architecture("x86"   ) )
nobs.Configuration( gen_vs,    "release-msvc-static",  "win-rel-x64-msvc-s",  opts_rel_s, toolchain_msvc,  nobs.Architecture("x86-64") )
#nobs.Configuration( gen_vs,    "debug-intel-static",   "win-deb-x32-intel-s", opts_deb_s, toolchain_intel, nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_vs,    "debug-intel-static",   "win-deb-x64-intel-s", opts_deb_s, toolchain_intel, nobs.Architecture("x86-64") )
#nobs.Configuration( gen_vs,    "release-intel-static", "win-rel-x32-intel-s", opts_rel_s, toolchain_intel, nobs.Architecture("x86"   ) )
#nobs.Configuration( gen_vs,    "release-intel-static", "win-rel-x64-intel-s", opts_rel_s, toolchain_intel, nobs.Architecture("x86-64") )


#Targets: all build targets (executables, libraries) relevant to your project.  If you add them,
#	they will be built.

#	Get a target static or dynamic library that's expected to be on the system.  Many are pre-
#		defined for you.  You can always tweak them or add your own in "nobs-sys/".
target_zlib = nobs.sys.get_system_target("zlib")

#	Define a static library as a build target.
target_mylib = nobs.TargetStaticLibrary(prj,
	"My Library",
	nobs.Export(
		[                            ], #Exported additional definitions
		[ nobs.Directory(".")        ], #Exported include directories
		[ nobs.File("mylib/include") ] #Exported headers
		#[ nobs.Directory(".build/")  ]  #Exported libraries root directories (optional and usually unecessary; will use build directory by default)
	),
	nobs.get_files_list("mylib/**/*.hpp") + [ nobs.File("mylib/include") ],
	nobs.get_files_list("mylib/**/*.cpp"),
	[ target_zlib ], #Dependencies
	None #PCH (optional: tuple (header,source) or default `None`)
)
#	Define an executable as a build target, depending on `target_mylib`.  Note: because
#		`target_mylib` depends on `target_zlib`, that will be added as a dependency automatically.
#		However, if you specified it again, NoBS is smart enough not to include it as a dependency
#		twice.
target_myexec = nobs.TargetExecutable(prj,
	"My Executable",
	nobs.get_files_list("myexec/**/*.hpp"),
	nobs.get_files_list("myexec/**/*.cpp"),
	[ #dependencies
		target_mylib
	]
)


#Generate project files
prj.generate()

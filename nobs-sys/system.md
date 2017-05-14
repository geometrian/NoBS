#System Packages

NoBS requires system packages to be compiled and stored in a sensible way.  This is typically easiest on Linux, primarily because the system's package manager does this for you.  Usually.  It is most difficult on Windows, because there is no such standard practice.

##Windows

Since there are no established standards, NoBS creates one.  All packages are stored into:
	Includes: C:/Program Files (x86)/Windows Kits/10/Include/user/*
	Libraries: C:/Program Files (x86)/Windows Kits/10/Lib/user/*
All packages are stored by name and version.  So e.g., zlib 1.2.11 is stored in the folder "zlib-1.2.11/" (also accessible by symlink "zlib/"; such name-only symlinks point to the latest package version).  The includes for the library are stored in a subdirectory "include/" and the libraries in "lib/".

So, for our whole example, the directory structure might look like:

Program Files (x86)/
	Windows Kits/
		10/
			Include/
				user/
					zlib-1.2.11/
						[zlib includes]
					zlib.props
			Lib/
				user/
					zlib-1.2.11/
						msvc-x86-s-deb/
							zlib.lib
						[other targets/configurations in form [compiler]-[arch]-[static/dyn C++]-[config]]
			Source/
				user/
					zlib-1.2.11/
						[zlib source]
			user-build/
				zlib-1.2.11/
					includes/
						[zlib includes]
					lib/
						msvc-x86-s-deb/
							zlib.lib
						[other targets/configurations in form [compiler]-[arch]-[static/dyn C++]-[config]]
					lib-temp/
						[zlib build temporary files; same subdir names as "lib/*"]
					src/
						[zlib source]
					misc/
						[zlib non-code files]
					zlib.sln
					zlib.vcxproj
					zlib.vcxproj.filters

You are encouraged to recompile everything using NoBS's preferred format.  A selection is provided for a variety of projects in "files-for-projects/".  Simply adjust the search directory at the top to point to an empty directory and run it; NoBS will generate MSVC 2017 build files.

Of course, package maintainers update all the time, so compatibility can only be guaranteed for a particular version.  This lamentable fact is unavoidable, due to the lack of automation on Windows.

##Linux

The assumption is that a package manager is handling builds for you using the system compiler.  

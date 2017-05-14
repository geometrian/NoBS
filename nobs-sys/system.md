#System Packages

NoBS requires system packages to be compiled and stored in a sensible way.

## Windows

There are no established standards for where dependencies go.  Hence, NoBS creates one.  All packages are stored into:
	Includes: `C:/Program Files (x86)/Windows Kits/10/Include/user/*`
	Libraries: `C:/Program Files (x86)/Windows Kits/10/Lib/user/*`
This is the directory used by MSVC for its library, so it makes some sense to store system packages here as well.  All packages are stored by name and version.  So e.g., zlib 1.2.11 is stored in the folder `zlib-1.2.11/` (also accessible by symlink `zlib/`; a symlink pointing to the latest version).  For `zlib`, the salient portion of the directory structure looks like:

Program Files (x86)/
	Windows Kits/
		10/
			Include/
				user/
					zlib/ -> zlib-1.2.11/
					zlib-1.2.11/
						<zlib public includes (symlinks to below)>
						zlib.props
					<etc.>
				<etc.>
			Lib/
				user/
					zlib/ -> zlib-1.2.11/
					zlib-1.2.11/
						win-deb-x32-msvc-s/
							zlib.lib (symlink to below)
						<other targets/configurations in form `[platform]-[config]-[arch]-[compiler]-[static/dyn C++]`>
					<etc.>
				<etc.>
			Source/
				user/
					zlib/ -> zlib-1.2.11/
					zlib-1.2.11/
						.nobs/
							.build/
								win-deb-x32-msvc-s/
									zlib.idb
									zlib.lib
									zlib.pdb
								<other targets/configurations in same form as above>
							.build-temp/
								<build temporary files>
							.ides/
								zlib.vcxproj
								zlib.vcxproj.filters
								zlib.vcxproj.user
								zlib.sln
						<zlib 1.2.11 distribution>
					download-cache/
						zlib-1.2.11.tar.gz
						<etc.>
				<etc.>
			<etc.>
		<etc.>
	<etc.>
<etc.>

You are encouraged to recompile everything using NoBS's preferred format.  A selection is provided for a variety of dependencies in "files-for-projects/".  These scripts automatically search for, configure, and build the dependencies.  Of course, package maintainers update all the time, so compatibility can only be guaranteed for a particular version.

## Linux

Roughly speaking, for multiarch packages, includes go in `/usr/include/<package>/*` and libs go in `/usr/lib/<arch>-linux-gnu/<package>/*`.  This makes disambiguating the compiler that built it hard, but compilers on Linux tend to be more careful about ABI-compatibility, so at least it's usually not a crippling failure.

For non-multiarch packages, it can be `/usr/lib32/...`, `/usr/libx32/...`, and so on.  This is obviously horrible.

Overall, the situation ranged from sub-optimal to awful, but compiler-built-in configured paths and the system's package manager seem to make it work most of the time.

This means that NoBS doesn't attempt to build dependencies on Linux at all.

from ._define import Define


class Toolchain(object):
	#Search Name, Visual Studio Identifier
	toolchains_gcc = [
		#https://gcc.gnu.org/releases.html (Where's GCC 7.0?  I know it was released!)
		( "gcc-6.5", None ),
		( "gcc-7.3", None ),
		( "gcc-8.2", None )
	]
	toolchains_clang = [
		#http://releases.llvm.org/
		( "clang-5.0.2", None ),
		( "clang-6.0.1", None ),
		( "clang-7.0.0", None )
	]
	toolchains_msvc = [
		#MSVC
		( "msvc-2013", "v120" ),
		( "msvc-2015", "v140" ),
		( "msvc-2017", "v141" )
	]
	toolchains_intel = [
		#Intel
		( "intel-16.0", "Intel C++ Compiler 16.0" ),
		( "intel-17.0", "Intel C++ Compiler 17.0" ),
		( "intel-18.0", "Intel C++ Compiler 18.0" )
	]
	toolchains = toolchains_gcc + toolchains_clang + toolchains_msvc + toolchains_intel

	GCC_6_5,     GCC_7_3,     GCC_8_2     = toolchains_gcc
	CLANG_5_0_2, CLANG_6_0_1, CLANG_7_0_2 = toolchains_clang
	MSVC_2013,   MSVC_2015,   MSVC_2017   = toolchains_msvc
	INTEL_16_0,  INTEL_17_0,  INTEL_18_0  = toolchains_intel

	GCC   = GCC_8_2
	CLANG = CLANG_7_0_2
	MSVC  = MSVC_2017
	INTEL = INTEL_18_0

	def __init__(self, search_name):
		def find_matching_toolchain():
			#Look for exact match
			for toolchain in Toolchain.toolchains:
				name,msvc = toolchain
				if search_name == name:
					return toolchain

			#Look for most-recent match
			if   search_name=="gcc":   return Toolchain.GCC
			elif search_name=="clang": return Toolchain.CLANG
			elif search_name=="msvc":  return Toolchain.MSVC
			elif search_name=="intel": return Toolchain.INTEL

			#Error
			msg = "Unrecognized toolchain \""+str(search_name)+"\"!  Supported toolchains are {\n"
			for toolchain in Toolchain.toolchains:
				msg += "  \""+toolchain[0]+"\""
				if   toolchain[0]==Toolchain.GCC  [0]: msg+=" = \"gcc\""
				elif toolchain[0]==Toolchain.CLANG[0]: msg+=" = \"clang\""
				elif toolchain[0]==Toolchain.MSVC [0]: msg+=" = \"msvc\""
				elif toolchain[0]==Toolchain.INTEL[0]: msg+=" = \"intel\""
				msg += ",\n"
			msg = msg[:-2] + "\n}."
			raise Exception(msg)

		self.type = find_matching_toolchain()

		self.additional_defines = []
		self.additional_build_options = []

##            self.additional_defines.append(Define( "__builtin_huge_val()", "HUGE_VAL"  ))
##            self.additional_defines.append(Define( "__builtin_huge_valf()","HUGE_VALF" ))
##            self.additional_defines.append(Define( "__builtin_nan",  "nan"  ))
##            self.additional_defines.append(Define( "__builtin_nanf", "nanf" ))
##            self.additional_defines.append(Define( "__builtin_nans", "nan"  ))
##            self.additional_defines.append(Define( "__builtin_nansf","nanf" ))
##            self.additional_defines.append(Define( "__is_assignable","__is_trivially_assignable" ))
##
##            self.additional_build_options.append( "-Qansi-alias" )
##            self.additional_build_options.append( "-traceback" )
##            self.additional_build_options.append( "/Quse-intel-optimized-headers" )
##            self.additional_build_options.append( "/Qdiag-disable:673,809,11074,11075" )
##            self.additional_build_options.append( "/debug:expr-source-pos" )

	def _getMSVCName(self):
		if self.type[1] == None:
			raise Exception("Toolchain \""+self.type[0]+"\" for MSVC project!")
		return self.type[1]

#Older releases we'll probably never ever need.

#	(0, "gcc-2.95",    None),
#	(0, "gcc-2.95.1",  None),
#	(0, "gcc-2.95.2",  None),
#	(0, "gcc-2.95.3",  None),
#	(0, "gcc-3.0",     None),
#	(0, "gcc-3.0.1",   None),
#	(0, "gcc-3.0.2",   None),
#	(0, "gcc-3.0.3",   None),
#	(0, "gcc-3.0.4",   None),
#	(0, "gcc-3.1",     None),
#	(0, "gcc-3.1.1",   None),
#	(0, "gcc-3.2",     None),
#	(0, "gcc-3.2.1",   None),
#	(0, "gcc-3.2.2",   None),
#	(0, "gcc-3.2.3",   None),
#	(0, "gcc-3.3",     None),
#	(0, "gcc-3.3.1",   None),
#	(0, "gcc-3.3.2",   None),
#	(0, "gcc-3.3.3",   None),
#	(0, "gcc-3.3.4",   None),
#	(0, "gcc-3.3.5",   None),
#	(0, "gcc-3.3.6",   None),
#	(0, "gcc-3.4.0",   None),
#	(0, "gcc-3.4.1",   None),
#	(0, "gcc-3.4.2",   None),
#	(0, "gcc-3.4.3",   None),
#	(0, "gcc-3.4.4",   None),
#	(0, "gcc-3.4.5",   None),
#	(0, "gcc-3.4.6",   None),
#	(0, "gcc-4.0.0",   None),
#	(0, "gcc-4.0.1",   None),
#	(0, "gcc-4.0.2",   None),
#	(0, "gcc-4.0.3",   None),
#	(0, "gcc-4.0.4",   None),
#	(0, "gcc-4.1.0",   None),
#	(0, "gcc-4.1.1",   None),
#	(0, "gcc-4.1.2",   None),
#	(0, "gcc-4.2.0",   None),
#	(0, "gcc-4.2.1",   None),
#	(0, "gcc-4.2.2",   None),
#	(0, "gcc-4.2.3",   None),
#	(0, "gcc-4.2.4",   None),
#	(0, "gcc-4.3.0",   None),
#	(0, "gcc-4.3.1",   None),
#	(0, "gcc-4.3.2",   None),
#	(0, "gcc-4.3.3",   None),
#	(0, "gcc-4.3.4",   None),
#	(0, "gcc-4.3.5",   None),
#	(0, "gcc-4.3.6",   None),
#	(0, "gcc-4.4.0",   None),
#	(0, "gcc-4.4.1",   None),
#	(0, "gcc-4.4.2",   None),
#	(0, "gcc-4.4.3",   None),
#	(0, "gcc-4.4.4",   None),
#	(0, "gcc-4.4.5",   None),
#	(0, "gcc-4.4.6",   None),
#	(0, "gcc-4.4.7",   None),
#	(0, "gcc-4.5.0",   None),
#	(0, "gcc-4.5.1",   None),
#	(0, "gcc-4.5.2",   None),
#	(0, "gcc-4.5.3",   None),
#	(0, "gcc-4.5.4",   None),
#	(0, "gcc-4.6.0",   None),
#	(0, "gcc-4.6.1",   None),
#	(0, "gcc-4.6.2",   None),
#	(0, "gcc-4.6.3",   None),
#	(0, "gcc-4.6.4",   None),
#	(0, "gcc-4.7.0",   None),
#	(0, "gcc-4.7.1",   None),
#	(0, "gcc-4.7.2",   None),
#	(0, "gcc-4.7.3",   None),
#	(0, "gcc-4.7.4",   None),
#	(0, "gcc-4.8.0",   None),
#	(0, "gcc-4.8.1",   None),
#	(0, "gcc-4.8.2",   None),
#	(0, "gcc-4.8.3",   None),
#	(0, "gcc-4.8.4",   None),
#	(0, "gcc-4.8.5",   None),
#	(0, "gcc-4.9.0",   None),
#	(0, "gcc-4.9.1",   None),
#	(0, "gcc-4.9.2",   None),
#	(0, "gcc-4.9.3",   None),
#	(0, "gcc-4.9.4",   None),
#	(0, "gcc-5.1",     None),
#	(0, "gcc-5.2",     None),
#	(0, "gcc-5.3",     None),
#	(0, "gcc-5.4",     None),
#	(0, "gcc-5.5",     None),
#	(0, "gcc-6.1",     None),
#	(0, "gcc-6.2",     None),
#	(0, "gcc-6.3",     None),
#	(0, "gcc-6.4",     None),
#	(0, "gcc-7.1",     None),
#	(0, "gcc-7.2",     None),
#	(0, "gcc-8.1",     None),

#	(0, "clang-1.0",   None),
#	(0, "clang-1.1",   None),
#	(0, "clang-1.2",   None),
#	(0, "clang-1.3",   None),
#	(0, "clang-1.4",   None),
#	(0, "clang-1.5",   None),
#	(0, "clang-1.6",   None),
#	(0, "clang-1.7",   None),
#	(0, "clang-1.8",   None),
#	(0, "clang-1.9",   None),
#	(0, "clang-2.0",   None),
#	(0, "clang-2.1",   None),
#	(0, "clang-2.2",   None),
#	(0, "clang-2.3",   None),
#	(0, "clang-2.4",   None),
#	(0, "clang-2.5",   None),
#	(0, "clang-2.6",   None),
#	(0, "clang-2.7",   None),
#	(0, "clang-2.8",   None),
#	(0, "clang-2.9",   None),
#	(0, "clang-3.0",   None),
#	(0, "clang-3.1",   None),
#	(0, "clang-3.2",   None),
#	(0, "clang-3.3",   None),
#	(0, "clang-3.4",   None),
#	(0, "clang-3.4.1", None),
#	(0, "clang-3.4.2", None),
#	(0, "clang-3.5.0", None),
#	(0, "clang-3.5.1", None),
#	(0, "clang-3.5.2", None),
#	(0, "clang-3.6.0", None),
#	(0, "clang-3.6.1", None),
#	(0, "clang-3.6.2", None),
#	(0, "clang-3.7.0", None),
#	(0, "clang-3.7.1", None),
#	(0, "clang-3.8.0", None),
#	(0, "clang-3.8.1", None),
#	(0, "clang-3.9.0", None),
#	(0, "clang-3.9.1", None),
#	(0, "clang-4.0.0", None),
#	(0, "clang-4.0.1", None),
#	(0, "clang-5.0.0", None),
#	(0, "clang-5.0.1", None),
#	(0, "clang-5.0.2", None),
#	(0, "clang-6.0.0", None),
#	(0, "clang-6.0.1", None),
#	(0, "clang-7.0.0", None),

#	(?, "msvc-2005", ????)
#	(0, "msvc-2008",  "v90")
#	(0, "msvc-2010", "v100")
#	(0, "msvc-2012", "v110")

#	( ?,"intel-15.0","Intel C++ Compiler 15.0")

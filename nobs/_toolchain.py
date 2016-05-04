from ._define import Define


class Toolchain(object):
    GCC_4_8     = ( 0,   "gcc-4.8",                     None)
    GCC_4_9     = ( 1,   "gcc-4.9",                     None)
    GCC_5_1     = ( 2,   "gcc-5.1",                     None)
    GCC_5_2     = ( 3,   "gcc-5.2",                     None)
    GCC_5_3     = ( 4,   "gcc-5.3",                     None)
    GCC_6_1     = ( 5,   "gcc-6.1",                     None)
##    MSVC_2005 = ( 6, "msvc-2005",                     ????)
    MSVC_2008   = ( 7, "msvc-2008",                    "v90")
    MSVC_2010   = ( 8, "msvc-2010",                   "v100")
    MSVC_2013   = ( 9, "msvc-2013",                   "v120")
    MSVC_2015   = (10, "msvc-2015",                   "v140")
    CLANG_3_7   = (11, "clang-3.7",         "v140_clang_3_7")
    CLANG_3_8   = (12, "clang-3.8",                     None)
    INTEL_16_0  = (13,"intel-16.0","Intel C++ Compiler 16.0")
    def __init__(self, search_name):
        self.additional_defines = []
        self.additional_build_options = []
        
        if   search_name == "gcc-4.8":
            self.type = Toolchain.GCC_4_8
        elif search_name in ["gcc-4.9","gcc-4"]:
            self.type = Toolchain.GCC_4_9
        elif search_name == "gcc-5.1":
            self.type = Toolchain.GCC_5_1
        elif search_name == "gcc-5.2":
            self.type = Toolchain.GCC_5_2
        elif search_name in ["gcc-5.3","gcc-5"]:
            self.type = Toolchain.GCC_5_3
        elif search_name in ["gcc-6.1","gcc-6","gcc"]:
            self.type = Toolchain.GCC_6_1
##        elif search_name == "msvc-2005":
##            self.type = Toolchain.MSVC_2005
        elif search_name == "msvc-2008":
            self.type = Toolchain.MSVC_2008
        elif search_name == "msvc-2010":
            self.type = Toolchain.MSVC_2010
        elif search_name == "msvc-2013":
            self.type = Toolchain.MSVC_2013
        elif search_name in ["msvc","msvc-2015"]:
            self.type = Toolchain.MSVC_2015
        elif search_name == "clang-3.7":
            self.type = Toolchain.CLANG_3_7
        elif search_name in ["clang-3.8","clang-3","clang"]:
            self.type = Toolchain.CLANG_3_8
        elif search_name in ["intel-16.0","intel-16","intel"]:
            self.type = Toolchain.INTEL_16_0

            self.additional_defines.append(Define( "__builtin_huge_val()", "HUGE_VAL"  ))
            self.additional_defines.append(Define( "__builtin_huge_valf()","HUGE_VALF" ))
            self.additional_defines.append(Define( "__builtin_nan",  "nan"  ))
            self.additional_defines.append(Define( "__builtin_nanf", "nanf" ))
            self.additional_defines.append(Define( "__builtin_nans", "nan"  ))
            self.additional_defines.append(Define( "__builtin_nansf","nanf" ))
            self.additional_defines.append(Define( "__is_assignable","__is_trivially_assignable" ))

            self.additional_build_options.append( "-Qansi-alias" )
            self.additional_build_options.append( "-traceback" )
            self.additional_build_options.append( "/Quse-intel-optimized-headers" )
            self.additional_build_options.append( "/Qdiag-disable:673,809,11074,11075" )
            self.additional_build_options.append( "/debug:expr-source-pos" )
        else:
            raise Exception("Unrecognized toolchain \""+str(search_name)+"""\"!  Supported toolchains are { "gcc-4.8", "gcc-4.9"="gcc-4", "gcc-5.1", "gcc-5.2", "gcc-5.3"="gcc-5", "gcc-6.1"="gcc-6"="gcc", "msvc-2008", "msvc-2010", "msvc-2013", "msvc-2015"="msvc", "clang-3.7", "clang-3.8"="clang-3"="clang", "intel-16.0"="intel-16"="intel" }.""")

    def _validate_basic(self):
        pass

    def _get_msvc_name(self):
        if self.type[2] == None:
            raise Exception("Toolchain \""+self.type[1]+"\" for MSVC project!")
        return self.type[2]
    

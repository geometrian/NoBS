from ._define import Define


class Toolchain(object):
    #Index, Search Name, Visual Studio Identifier
    toolchains = [
        #https://gcc.gnu.org/releases.html (Where's GCC 7.0?  I know it was released!)
        (0, "gcc-6.2",    None),
        (1, "gcc-6.3",    None),
        (2, "gcc-7.1",    None),

        #http://releases.llvm.org/
        (3, "clang-3.9.0", None),
        (4, "clang-3.9.1", None),
        (5, "clang-4.0.0", None),

        #MSVC
        (6, "msvc-2013", "v120"),
        (7, "msvc-2015", "v140"),
        (8, "msvc-2017", "v141"),

        #Intel
        ( 9,"intel-15.0","Intel C++ Compiler 15.0"),
        (10,"intel-16.0","Intel C++ Compiler 16.0"),
        (11,"intel-17.0","Intel C++ Compiler 17.0")
    ]
    GCC_6_2,GCC_6_3,GCC_7_1, CLANG_3_9_0,CLANG_3_9_1,CLANG_4_0_0, MSVC_2013,MSVC_2015,MSVC_2017, INTEL_15_0,INTEL_16_0,INTEL_17_0 = toolchains
    GCC=GCC_7_1; CLANG=CLANG_4_0_0; MSVC=MSVC_2017; INTEL=INTEL_17_0
    def __init__(self, search_name):
        found = False
        for index,name,msvc in Toolchain.toolchains:
            if search_name == name:
                found = index
                break
        if found == False:
            if   search_name==  "gcc": found=Toolchain.  GCC[0]
            elif search_name=="clang": found=Toolchain.CLANG[0]
            elif search_name== "msvc": found=Toolchain. MSVC[0]
            elif search_name=="intel": found=Toolchain.INTEL[0]
            else:
                mesg = "Unrecognized toolchain \""+str(search_name)+"\"!  Supported toolchains are {\n"
                for toolchain in Toolchain.toolchains:
                    mesg += "  \""+toolchain[1]+"\""
                    if   toolchain[0]==Toolchain.  GCC[0]: mesg+=" = \"gcc\""
                    elif toolchain[0]==Toolchain.CLANG[0]: mesg+=" = \"clang\""
                    elif toolchain[0]==Toolchain. MSVC[0]: mesg+=" = \"msvc\""
                    elif toolchain[0]==Toolchain.INTEL[0]: mesg+=" = \"intel\""
                    mesg += ",\n"
                mesg = mesg[:-2] + "\n}."
                raise Exception(mesg)
        self.type = Toolchain.toolchains[found]

        self.additional_defines = []
        self.additional_build_options = []

##        if   search_name == "gcc-4.8":
##            self.type = Toolchain.GCC_4_8
##        elif search_name in ["gcc-4.9","gcc-4"]:
##            self.type = Toolchain.GCC_4_9
##        elif search_name == "gcc-5.1":
##            self.type = Toolchain.GCC_5_1
##        elif search_name == "gcc-5.2":
##            self.type = Toolchain.GCC_5_2
##        elif search_name in ["gcc-5.3","gcc-5"]:
##            self.type = Toolchain.GCC_5_3
##        elif search_name in ["gcc-6.1","gcc-6","gcc"]:
##            self.type = Toolchain.GCC_6_1
####        elif search_name == "msvc-2005":
####            self.type = Toolchain.MSVC_2005
##        elif search_name == "msvc-2008":
##            self.type = Toolchain.MSVC_2008
##        elif search_name == "msvc-2010":
##            self.type = Toolchain.MSVC_2010
##        elif search_name == "msvc-2013":
##            self.type = Toolchain.MSVC_2013
##        elif search_name in ["msvc","msvc-2015"]:
##            self.type = Toolchain.MSVC_2015
##        elif search_name == "clang-3.7":
##            self.type = Toolchain.CLANG_3_7
##        elif search_name in ["clang-3.8","clang-3","clang"]:
##            self.type = Toolchain.CLANG_3_8
##        elif search_name in ["intel-16.0","intel-16","intel"]:
##            self.type = Toolchain.INTEL_16_0
##
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
##        else:
##            
####        if "gcc" in self.type[1]:
####            #GCC arguments

    def _validate_basic(self):
        pass

    def _get_msvc_name(self):
        if self.type[2] == None:
            raise Exception("Toolchain \""+self.type[1]+"\" for MSVC project!")
        return self.type[2]

#Older releases we'll probably never ever need.

##(0, "gcc-2.95",   None),
##(0, "gcc-2.95.1", None),
##(0, "gcc-2.95.2", None),
##(0, "gcc-2.95.3", None),
##(0, "gcc-3.0",    None),
##(0, "gcc-3.0.1",  None),
##(0, "gcc-3.0.2",  None),
##(0, "gcc-3.0.3",  None),
##(0, "gcc-3.0.4",  None),
##(0, "gcc-3.1",    None),
##(0, "gcc-3.1.1",  None),
##(0, "gcc-3.2",    None),
##(0, "gcc-3.2.1",  None),
##(0, "gcc-3.2.2",  None),
##(0, "gcc-3.2.3",  None),
##(0, "gcc-3.3",    None),
##(0, "gcc-3.3.1",  None),
##(0, "gcc-3.3.2",  None),
##(0, "gcc-3.3.3",  None),
##(0, "gcc-3.3.4",  None),
##(0, "gcc-3.3.5",  None),
##(0, "gcc-3.3.6",  None),
##(0, "gcc-3.4.0",  None),
##(0, "gcc-3.4.1",  None),
##(0, "gcc-3.4.2",  None),
##(0, "gcc-3.4.3",  None),
##(0, "gcc-3.4.4",  None),
##(0, "gcc-3.4.5",  None),
##(0, "gcc-3.4.6",  None),
##(0, "gcc-4.0.0",  None),
##(0, "gcc-4.0.1",  None),
##(0, "gcc-4.0.2",  None),
##(0, "gcc-4.0.3",  None),
##(0, "gcc-4.0.4",  None),
##(0, "gcc-4.1.0",  None),
##(0, "gcc-4.1.1",  None),
##(0, "gcc-4.1.2",  None),
##(0, "gcc-4.2.0",  None),
##(0, "gcc-4.2.1",  None),
##(0, "gcc-4.2.2",  None),
##(0, "gcc-4.2.3",  None),
##(0, "gcc-4.2.4",  None),
##(0, "gcc-4.3.0",  None),
##(0, "gcc-4.3.1",  None),
##(0, "gcc-4.3.2",  None),
##(0, "gcc-4.3.3",  None),
##(0, "gcc-4.3.4",  None),
##(0, "gcc-4.3.5",  None),
##(0, "gcc-4.3.6",  None),
##(0, "gcc-4.4.0",  None),
##(0, "gcc-4.4.1",  None),
##(0, "gcc-4.4.2",  None),
##(0, "gcc-4.4.3",  None),
##(0, "gcc-4.4.4",  None),
##(0, "gcc-4.4.5",  None),
##(0, "gcc-4.4.6",  None),
##(0, "gcc-4.4.7",  None),
##(0, "gcc-4.5.0",  None),
##(0, "gcc-4.5.1",  None),
##(0, "gcc-4.5.2",  None),
##(0, "gcc-4.5.3",  None),
##(0, "gcc-4.5.4",  None),
##(0, "gcc-4.6.0",  None),
##(0, "gcc-4.6.1",  None),
##(0, "gcc-4.6.2",  None),
##(0, "gcc-4.6.3",  None),
##(0, "gcc-4.6.4",  None),
##(0, "gcc-4.7.0",  None),
##(0, "gcc-4.7.1",  None),
##(0, "gcc-4.7.2",  None),
##(0, "gcc-4.7.3",  None),
##(0, "gcc-4.7.4",  None),
##(0, "gcc-4.8.0",  None),
##(0, "gcc-4.8.1",  None),
##(0, "gcc-4.8.2",  None),
##(0, "gcc-4.8.3",  None),
##(0, "gcc-4.8.4",  None),
##(0, "gcc-4.8.5",  None),
##(0, "gcc-4.9.0",  None),
##(0, "gcc-4.9.1",  None),
##(0, "gcc-4.9.2",  None),
##(0, "gcc-4.9.3",  None),
##(0, "gcc-4.9.4",  None),
##(0, "gcc-5.1",    None),
##(0, "gcc-5.2",    None),
##(0, "gcc-5.3",    None),
##(0, "gcc-5.4",    None),
##(0, "gcc-6.1",    None),
    
##(0, "clang-1.0", None),
##(0, "clang-1.1", None),
##(0, "clang-1.2", None),
##(0, "clang-1.3", None),
##(0, "clang-1.4", None),
##(0, "clang-1.5", None),
##(0, "clang-1.6", None),
##(0, "clang-1.7", None),
##(0, "clang-1.8", None),
##(0, "clang-1.9", None),
##(0, "clang-2.0", None),
##(0, "clang-2.1", None),
##(0, "clang-2.2", None),
##(0, "clang-2.3", None),
##(0, "clang-2.4", None),
##(0, "clang-2.5", None),
##(0, "clang-2.6", None),
##(0, "clang-2.7", None),
##(0, "clang-2.8", None),
##(0, "clang-2.9", None),
##(0, "clang-3.0", None),
##(0, "clang-3.1", None),
##(0, "clang-3.2", None),
##(0, "clang-3.3", None),
##(0, "clang-3.4", None),
##(0, "clang-3.4.1", None),
##(0, "clang-3.4.2", None),
##(0, "clang-3.5.0", None),
##(0, "clang-3.5.1", None),
##(0, "clang-3.5.2", None),
##(0, "clang-3.6.0", None),
##(0, "clang-3.6.1", None),
##(0, "clang-3.6.2", None),
##(0, "clang-3.7.0", None),
##(0, "clang-3.7.1", None),
##(0, "clang-3.8.0", None),
##(0, "clang-3.8.1", None),

###(?, "msvc-2005", ????)
##(0, "msvc-2008",  "v90")
##(0, "msvc-2010", "v100")
##(0, "msvc-2012", "v110")

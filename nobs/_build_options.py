from ._define import Define


class BuildOptions(object):
    SIMD_NONE = 0
    SIMD_MMX = 1
    SIMD_SSE = 2
    SIMD_SSE2 = 3
    SIMD_SSE3 = 4
    SIMD_SSSE3 = 5
    SIMD_SSE4_1 = 6
    SIMD_SSE4_2 = 7
    SIMD_AVX = 8
    SIMD_AVX2 = 9
    SIMD_AVX512F = 10
    SIMD_AVX512VL = 11
    SIMD_NEON = 12
    def __init__(self, basic_type=None):
        self.defines = []
        
        if   basic_type == None:
            self.is_debug = None
            self.with_symbols = None
            self.optimization = None
            self.buffer_check = None
        elif basic_type == "debug":
            self.is_debug = True
            self.with_symbols = True
            self.optimization = 0
            self.defines.append(Define("DEBUG"))
            self.buffer_check = True
        elif basic_type == "release":
            self.is_debug = False
            self.with_symbols = False
            self.optimization = 1
            self.defines.append(Define("NDEBUG"))
            self.buffer_check = False
        elif basic_type == "release-with-symbols":
            self.is_debug = False
            self.with_symbols = True
            self.optimization = 1
            self.defines.append(Define("NDEBUG"))
            self.buffer_check = False
        else:
            raise Exception("Unrecognized basic type \""+str(basic_type)+"\"!  Supported types are { None, \"debug\", \"release\", \"release-with-symbols\" }.")

        self.is_stdlib_dynamically_linked = None

        self.simd = BuildOptions.SIMD_NONE
        #e.g. -msse4.1

        #debug
##        gcc: "-fsanitize=address","-fsanitize=leak","-fno-omit-frame-pointer","-fno-common", "-fPIC", "-static-libasan","-static-liblsan"
##        clang: also "-fsanitize=memory", "-fsanitize=integer"

    def set_dynamic_stdlib(self):
        self.is_stdlib_dynamically_linked = True
    def set_static_stdlib(self):
        self.is_stdlib_dynamically_linked = False

    def add_define(self, define):
        if not isinstance(define,Define):
            raise Exception("Define must be an instance of \"nobs.Define\"!")
        self.defines.append(define)

    def _validate_basic(self):
        if not isinstance(self.is_debug,bool): raise Exception("Build options \".is_debug\" must be set to a boolean!")
        if not isinstance(self.with_symbols,bool): raise Exception("Build options \".with_symbols\" must be set to a boolean!")
        if not isinstance(self.optimization,int) or self.optimization<0 or self.optimization>1:
            raise Exception("Build options \".optimization\" must be set to either 0 or 1!")
        if not isinstance(self.buffer_check,bool): raise Exception("Build options \".buffer_check\" must be set to a boolean!")
        if self.is_stdlib_dynamically_linked == None: raise Exception("Build options must call either \".set_dynamic_stdlib()\" or \".set_static_stdlib()\"!")

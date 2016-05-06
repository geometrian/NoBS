import os

from . import _helpers
from ._architecture import Architecture
from ._build_options import BuildOptions
from . import _platform
from ._target import _TargetBase


def _generate_msvc2015(project):
    #We need to generate three files:
    #   A ".sln" "project" file.  This ties together the target files
    #   Some ".vcxproj" "target" file(s).  This describes a set of files and how to compile them into a target
    #   Some ".vcxproj.filters" "filters" file(s).  This describes how the files appear in the IDE.

    found = False
    for platform in project.platforms:
        if platform.type == _platform.Platform.WINDOWS:
            found = True
            break
    if not found:
        raise Exception("Cannot generate MSVC build files; \"windows\" platform not requested by project.")

    _generate_msvc2015_sln(project)
    for target in project.targets:
        _generate_msvc2015_vcxproj(project,target)
        _generate_msvc2015_vcxprojfilters(project,target)
def _generate_msvc2015_sln(project):
    #Example:

    ##Microsoft Visual Studio Solution File, Format Version 12.00
    ##VisualStudioVersion = 14.0.25123.0
    ##MinimumVisualStudioVersion = 10.0.40219.1
    ##Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "FooAppl", "FooAppl.vcxproj", "{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}"
    ##EndProject
    ##Global
    ##	GlobalSection(SolutionConfigurationPlatforms) = preSolution
    ##		Debug|x64 = Debug|x64
    ##		Debug|x86 = Debug|x86
    ##		Release|x64 = Release|x64
    ##		Release|x86 = Release|x86
    ##	EndGlobalSection
    ##	GlobalSection(ProjectConfigurationPlatforms) = postSolution
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x64.ActiveCfg = Debug|x64
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x64.Build.0 = Debug|x64
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x86.ActiveCfg = Debug|Win32
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x86.Build.0 = Debug|Win32
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x64.ActiveCfg = Release|x64
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x64.Build.0 = Release|x64
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x86.ActiveCfg = Release|Win32
    ##		{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x86.Build.0 = Release|Win32
    ##	EndGlobalSection
    ##	GlobalSection(SolutionProperties) = preSolution
    ##		HideSolutionNode = FALSE
    ##	EndGlobalSection
    ##EndGlobal

    configs = []
    for platform in project.platforms:
        if platform.type == _platform.Platform.WINDOWS:
            for config in platform.configurations:
                configs.append(config)

    data =\
    """Microsoft Visual Studio Solution File, Format Version 12.00
VisualStudioVersion = 14.0.25123.0
MinimumVisualStudioVersion = 10.0.40219.1
"""
    for target in project.targets:
        #Project specification.
        #   See http://stackoverflow.com/a/2328668/688624
        #   See http://www.codeproject.com/Reference/720512/List-of-Visual-Studio-Project-Type-GUIDs
        
        ##Project("{<Project Type UUID>}") = "<Project Name>", "<Project File's Location>", "{<Unique Project UUID>}"
        ##	ProjectSection(ProjectDependencies) = postProject
        ##		{<Dependency1 Project UUID>} = {<Dependency1 Project UUID>}
        ##		{<Dependency2 Project UUID>} = {<Dependency2 Project UUID>}
        ##		{<Dependency3 Project UUID>} = {<Dependency3 Project UUID>}
        #...
        ##	EndProjectSection
        ##EndProject

        #All targets are C++ targets.
        data += "Project(\"{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}\") = \""+target.name+"\", \""+target.name+".vcxproj\", \"{"+target.uuid+"}\"\n"

        deps = target._get_flattened_dependencies_list()
        deps_salient = [] #All of this target's ultimate dependencies that are also defined in this project
        for dep in deps:
            if dep in project.targets:
                deps_salient.append(dep)
        if len(deps_salient) > 0:
            data += "\tProjectSection(ProjectDependencies) = postProject\n"
            for dep in sorted(list(deps_salient)):
                data += "\t\t{"+dep.uuid+"} = {"+dep.uuid+"}\n"
            data += "\tEndProjectSection\n"
        data += "EndProject\n"
    data += """Global
\tGlobalSection(SolutionConfigurationPlatforms) = preSolution
"""
    for config in configs:
        data += "\t\t"+config._get_msvc_name()+" = "+config._get_msvc_name()+"\n"
        #\t\tdebug|Win32 = debug|Win32
    data += "\tEndGlobalSection\n\tGlobalSection(ProjectConfigurationPlatforms) = postSolution\n"
    for target in project.targets:
        for config in configs:
            msvc_name = config._get_msvc_name()
            data +=\
                "\t\t{"+target.uuid+"}."+msvc_name+".ActiveCfg = "+msvc_name+"\n" +\
                "\t\t{"+target.uuid+"}."+msvc_name+".Build.0   = "+msvc_name+"\n"
    data += """\tEndGlobalSection
\tGlobalSection(SolutionProperties) = preSolution
\t\tHideSolutionNode = FALSE
\tEndGlobalSection
EndGlobal
"""

    file = open(os.path.join(project.build_files_directory.abspath,project.name+".sln"),"w")
    file.write(data)
    file.close()

def _generate_msvc2015_vcxproj(project,target):
    configs = []
    for platform in project.platforms:
        if platform.type == _platform.Platform.WINDOWS:
            for config in platform.configurations:
                if target.configurations == None or config in target.configurations:
                    configs.append(config)

    #Note: the value for xmlns must be the dead link "http://schemas.microsoft.com/developer/msbuild/2003",
    #   not the more sensible https://msdn.microsoft.com/en-us/library/5dy88c2e.aspx
    data = """<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
\t<ItemGroup Label="ProjectConfigurations">"""
    for config in configs:
        data += """
\t\t<ProjectConfiguration Include="%s">
\t\t\t<Configuration>%s</Configuration>
\t\t\t<Platform>%s</Platform>
\t\t</ProjectConfiguration>""" % (config._get_msvc_configplat(),config.name,config._get_msvc_arch())
    data += """
\t</ItemGroup>
\t<PropertyGroup Label="Globals">
\t\t<ProjectGuid>{%s}</ProjectGuid>
\t\t<Keyword>Win32Proj</Keyword>
\t\t<RootNamespace>%s</RootNamespace>
\t\t<WindowsTargetPlatformVersion>8.1</WindowsTargetPlatformVersion>
\t\t<CharacterSet>Unicode</CharacterSet>
\t</PropertyGroup>
\t<Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props"/>
""" % (target.uuid,target.name)
    for config in configs:
        data += """\t<PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s'" Label="Configuration">
\t\t<ConfigurationType>%s</ConfigurationType>
\t\t<UseDebugLibraries>%s</UseDebugLibraries>
\t\t<PlatformToolset>%s</PlatformToolset>
\t</PropertyGroup>\n""" % (
        config._get_msvc_configplat(),
        target._get_msvc_type(),
        "true" if config.build_options.is_debug else "false",
        config.toolchain._get_msvc_name()
    )
    data += """\t<Import Project="$(VCTargetsPath)\Microsoft.Cpp.props"/>
\t<ImportGroup Label="ExtensionSettings"/>"""
    for config in configs:
        data += """
\t<ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='%s'">
\t\t<Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
\t</ImportGroup>""" % (config._get_msvc_configplat())
    data += """
\t<PropertyGroup Label="UserMacros"/>
"""

    dirs_inc = []
    dirs_lib = []
    dep_libs = []
    for dep in target._get_flattened_dependencies_list():
        dirs_inc += [
            os.path.relpath(incl.abspath,project.build_files_directory.abspath)
            for incl in dep.exported.dirs_incl_list
        ]
        dirs_lib += [ _helpers._reslash(
            os.path.relpath( dep.project.build_result_directory.abspath, project.build_files_directory.abspath ) + "\\"
        ) ]
        dep_libs += [ dep.name + ".lib" ]
    
    for config in configs:
        data += """\t<PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s'">""" % (config._get_msvc_configplat())
        if target.type == _TargetBase.EXECUTABLE:
            data += """
\t\t<LinkIncremental>true</LinkIncremental>"""
        data += """
\t\t<OutDir>%s</OutDir>
\t\t<IntDir>%s</IntDir>
""" % (
            _helpers._reslash( os.path.relpath(project.build_result_directory.relpath+config.name_build,project.build_files_directory.abspath) + "\\" ),
            _helpers._reslash( os.path.relpath(project.build_temporary_directory.relpath+config.name_build+"/"+target.name,project.build_files_directory.abspath) + "\\" )
        )
        if len(dirs_inc) > 0:
            data += "\t\t<IncludePath>"+"".join([inc+";" for inc in dirs_inc])+"$(IncludePath)</IncludePath>\n"
        if len(dirs_lib) > 0:
            data += "\t\t<LibraryPath>"+"".join([lib+config.name_build+"/;" for lib in dirs_lib])+"$(LibraryPath)</LibraryPath>\n"
        data += """\t</PropertyGroup>
"""

    for config in configs:
        data += "\t<ItemDefinitionGroup Condition=\"'$(Configuration)|$(Platform)'=='"+config._get_msvc_configplat()+"""'">
\t\t<ClCompile>
\t\t\t<PrecompiledHeader>"""+("Use" if target.pch!=None else "NotUsing")+"""</PrecompiledHeader>
\t\t\t<Optimization>"""+("Disabled","MaxSpeed")[config.build_options.optimization]+"""</Optimization>
\t\t\t<WarningLevel>Level3</WarningLevel>
\t\t\t<PreprocessorDefinitions>"""
        for define in config.build_options.defines:
            data += define.symbol
            if define.value!=None: data+="="+define.value
            data += ";"
        data += """%(PreprocessorDefinitions)</PreprocessorDefinitions>
\t\t\t<MultiProcessorCompilation>true</MultiProcessorCompilation>
\t\t\t<RuntimeLibrary>MultiThreaded"""
        if config.build_options.is_debug:
            data += "Debug"
        if config.build_options.is_stdlib_dynamically_linked:
            data += "DLL"
        data += "</RuntimeLibrary>\n"
        if config.architecture.type == Architecture.ARCH_X86:
            #Due to a long-standingly-denied bug, MSVC only accepts these in x86 mode.  It generates them automatically for x86-64 mode.
            if   config.build_options.simd in [BuildOptions.SIMD_NONE,BuildOptions.SIMD_MMX]: pass
            elif config.build_options.simd == BuildOptions.SIMD_SSE:
                data += "\t\t\t<EnableEnhancedInstructionSet>StreamingSIMDExtensions</EnableEnhancedInstructionSet>\n"
            elif config.build_options.simd in [BuildOptions.SIMD_SSE2,BuildOptions.SIMD_SSE3,BuildOptions.SIMD_SSSE3,BuildOptions.SIMD_SSE4_1,BuildOptions.SIMD_SSE4_2]:
                data += "\t\t\t<EnableEnhancedInstructionSet>StreamingSIMDExtensions2</EnableEnhancedInstructionSet>\n"
            elif config.build_options.simd == BuildOptions.SIMD_AVX:
                data += "\t\t\t<EnableEnhancedInstructionSet>AdvancedVectorExtensions</EnableEnhancedInstructionSet>\n"
            elif config.build_options.simd == BuildOptions.SIMD_AVX2:
                data += "\t\t\t<EnableEnhancedInstructionSet>AdvancedVectorExtensions2</EnableEnhancedInstructionSet>\n"
            else: pass
        if len(config.toolchain.additional_build_options) > 0:
            data += "\t\t\t<AdditionalOptions>"+"".join([opt+" " for opt in config.toolchain.additional_build_options])+"%(AdditionalOptions)</AdditionalOptions>\n"
        data += """\t\t</ClCompile>
\t\t<Link>
"""
        if config.build_options.with_symbols:
            data += "\t\t\t<GenerateDebugInformation>Debug</GenerateDebugInformation>\n"
        if len(dep_libs) > 0:
            data += "\t\t\t<AdditionalDependencies>"+"".join([dep+";" for dep in dep_libs])+"%(AdditionalDependencies)</AdditionalDependencies>\n"
        data += """\t\t</Link>
\t</ItemDefinitionGroup>
"""

    files = target.headers_list + target.sources_list
    if len(files) > 0:
        data += "\t<ItemGroup>\n"
        for file in files:
            relpath = _helpers._reslash( os.path.relpath(file.abspath,project.build_files_directory.abspath) )
            if target.pch != None and path == target.pch[1]:
                if file.is_header:
                    data += "\t\t<ClInclude Include=\""+relpath+"\">\n\t\t\t<PrecompiledHeader>Create</PrecompiledHeader>\t\t</ClInclude>\n"
                elif file.is_source:
                    data += "\t\t<ClCompile Include=\""+relpath+"\">\n\t\t\t<PrecompiledHeader>Create</PrecompiledHeader>\t\t</ClCompile>\n"
                else:
                    data += "\t\t<Text Include=\""+relpath+"\">\n\t\t\t<PrecompiledHeader>Create</PrecompiledHeader>\t\t</Text>\n"
            else:
                if file.is_header:
                    data += "\t\t<ClInclude Include=\""+relpath+"\"/>\n"
                elif file.is_source:
                    data += "\t\t<ClCompile Include=\""+relpath+"\"/>\n"
                else:
                    data += "\t\t<Text Include=\""+relpath+"\"/>\n"
        data += "\t</ItemGroup>\n"

    data += """\t<Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets"/>
\t<ImportGroup Label="ExtensionTargets"/>
</Project>
"""

    file = open(os.path.join(project.build_files_directory.abspath,target.name+".vcxproj"),"w")
    file.write(data)
    file.close()

def _generate_msvc2015_vcxprojfilters(project,target):
    files = target.headers_list + target.sources_list
    
    folders = []
    for file in files:
        if file.absdir not in folders: folders.append(file.absdir)
    folders = sorted(folders)
    
    #Note: the value for xmlns must be the dead link "http://schemas.microsoft.com/developer/msbuild/2003",
    #   not the more sensible https://msdn.microsoft.com/en-us/library/5dy88c2e.aspx
    data = """<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
\t<ItemGroup>
"""
    for folder in folders:
##        print("folder")
##        print(folder)
##        print("abspath")
##        print(project.build_files_directory.abspath)
##        print("done")
        relpath = _helpers._reslash( os.path.relpath(folder,project.build_files_directory.abspath) )
        data += "\t\t<Filter Include=\""+relpath+"""\">
\t\t\t<UniqueIdentifier>{"""+_helpers._get_uuid(relpath)+"""}</UniqueIdentifier>
\t\t</Filter>
"""
    data += """\t</ItemGroup>
\t<ItemGroup>
"""

    for file in files:
        relpath = _helpers._reslash( os.path.relpath(file.abspath,project.build_files_directory.abspath) )
        reldir = _helpers._reslash( os.path.relpath(file.absdir,project.build_files_directory.abspath) )
        if file.is_header:
            data += "\t\t<ClInclude Include=\""+relpath+"""\">
\t\t\t<Filter>"""+reldir+"""</Filter>
\t\t</ClInclude>
"""
        elif file.is_source:
            data += "\t\t<ClCompile Include=\""+relpath+"""\">
\t\t\t<Filter>"""+reldir+"""</Filter>
\t\t</ClCompile>
"""
        else:
            data += "\t\t<Text Include=\""+relpath+"""\">
\t\t\t<Filter>"""+reldir+"""</Filter>
\t\t</Text>
"""

    data += """\t</ItemGroup>
</Project>"""

    file = open(os.path.join(project.build_files_directory.abspath,target.name+".vcxproj.filters"),"w")
    file.write(data)
    file.close()










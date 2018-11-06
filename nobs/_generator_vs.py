import os

from . import _configuration
from . import _generator_base
from . import _helpers
from . import _project
from . import _target
from ._architecture import Architecture
from ._build_options import BuildOptions


class _GeneratorVS(_generator_base._GeneratorBase):
	def __init__(self, project, ver_year):
		_generator_base._GeneratorBase.__init__(self, project)

		if ver_year not in [2015,2017]:
			_helpers._error("Supported year versions are { 2015, 2017 }!")
		self.ver_year = ver_year

	def isVisualStudioGenerator(self):
		return True

	def generate                   (self        ):
		if len(self.configurations) == 0:
			_helpers._warning("No configurations for project; Visual Studio does not allow this, and so no Visual Studio output will be made.")
		else:
			#We need to generate three files:

			#	A ".sln" "project" file.  This ties together the target files
			sln_file_path = self._generateFileSolution()

			#		Make a link to the solution in the root directory
			sln_file_pathlink = self.project.directory_project_root.abspath + self.project.name+".sln"
			_helpers.overwrite_symlink( sln_file_path, sln_file_pathlink, None )

			#	Some ".vcxproj" "target" file(s).  This describes a set of files and how to compile them
			#		into a target
			#	Some ".vcxproj.filters" "filters" file(s).  This describes how the files appear in the
			#		IDE.
			for target in self.project.targets:
				self._generateFileProject       (target)
				self._generateFileProjectFilters(target)
				#Not strictly necessary, as VS will create these.  However, creating up-front
				#	prevents confusing projects' source control.
				self._generateFileProjectUser   (target)

	def _generateFileSolution      (self        ):
		#Example:
		#	Microsoft Visual Studio Solution File, Format Version 12.00
		#	# Visual Studio 15
		#	VisualStudioVersion = 15.0.28010.2003
		#	MinimumVisualStudioVersion = 10.0.40219.1
		#	Project("{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}") = "FooAppl", "FooAppl.vcxproj", "{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}"
		#	EndProject
		#	Global
		#		GlobalSection(SolutionConfigurationPlatforms) = preSolution
		#			Debug|x64 = Debug|x64
		#			Debug|x86 = Debug|x86
		#			Release|x64 = Release|x64
		#			Release|x86 = Release|x86
		#		EndGlobalSection
		#		GlobalSection(ProjectConfigurationPlatforms) = postSolution
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x64.ActiveCfg = Debug|x64
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x64.Build.0 = Debug|x64
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x86.ActiveCfg = Debug|Win32
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Debug|x86.Build.0 = Debug|Win32
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x64.ActiveCfg = Release|x64
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x64.Build.0 = Release|x64
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x86.ActiveCfg = Release|Win32
		#			{AF3C8D88-D7DB-4FDF-B631-7EE778D19E19}.Release|x86.Build.0 = Release|Win32
		#		EndGlobalSection
		#		GlobalSection(SolutionProperties) = preSolution
		#			HideSolutionNode = FALSE
		#		EndGlobalSection
		#	EndGlobal

		#Header
		data = "Microsoft Visual Studio Solution File, Format Version 12.00\n\n"
		if   self.ver_year == 2015:
			data += "VisualStudioVersion = 14.0.25123.0"
		elif self.ver_year == 2017:
			data += "# Visual Studio 15\n"
			data += "VisualStudioVersion = 15.0.28010.2003\n"
		data += "MinimumVisualStudioVersion = 10.0.40219.1\n\n"

		#Declare projects
		#	See http://stackoverflow.com/a/2328668/688624
		#	See http://www.codeproject.com/Reference/720512/List-of-Visual-Studio-Project-Type-GUIDs
		for target in self.project.targets:
			#Project("{<Project Type UUID>}") = "<Project Name>", "<Project File's Location>", "{<Unique Project UUID>}"
			#	ProjectSection(ProjectDependencies) = postProject
			#		{<Dependency1 Project UUID>} = {<Dependency1 Project UUID>}
			#		{<Dependency2 Project UUID>} = {<Dependency2 Project UUID>}
			#		{<Dependency3 Project UUID>} = {<Dependency3 Project UUID>}
			#		...
			#	EndProjectSection
			#EndProject

			#All targets are C++ targets (this UUID).
			data += "Project(\"{8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942}\") = \""+target.name+"\", \""+target.name+".vcxproj\", \"{"+target.uuid+"}\"\n"

			deps_salient = [] #All of this target's ultimate dependencies that are also defined in this project
			for dep in target.dependencies_list_flat:
				if dep in self.project.targets:
					deps_salient.append(dep)
			if len(deps_salient) > 0:
				data += "\tProjectSection(ProjectDependencies) = postProject\n"
				for dep in sorted(list(deps_salient)):
					data += "\t\t{"+dep.uuid+"} = {"+dep.uuid+"}\n"
				data += "\tEndProjectSection\n"
			data += "EndProject\n"

		#Global configuration section
		data += "\nGlobal\n"

		data += "\tGlobalSection(SolutionConfigurationPlatforms) = preSolution\n"
		temp_lines = []
		for config in self.configurations:
			#E.g. "\t\tdebug|Win32 = debug|Win32"
			temp_lines.append("\t\t"+config._getMSVCName()+" = "+config._getMSVCName()+"\n")
		temp_lines.sort() #VS sorts these, at least in VS 2017.
		data += "".join(temp_lines)
		data += "\tEndGlobalSection\n"

		data += "\tGlobalSection(ProjectConfigurationPlatforms) = postSolution\n"
		temp_lines = []
		for target in self.project.targets:
			for config in self.configurations:
				msvc_name = config._getMSVCName()
				if self.ver_year < 2017:
					temp_lines.append("\t\t{"+target.uuid+"}."+msvc_name+".ActiveCfg = "+msvc_name+"\n")
					temp_lines.append("\t\t{"+target.uuid+"}."+msvc_name+".Build.0   = "+msvc_name+"\n")
				else:
					msvc_config = config._getMSVCConfigPlat()
					temp_lines.append("\t\t{"+target.uuid+"}."+msvc_name+".ActiveCfg = "+msvc_config+"\n")
					temp_lines.append("\t\t{"+target.uuid+"}."+msvc_name+".Build.0   = "+msvc_config+"\n")
					#temp_lines.append("\t\t{"+target.uuid+"}."+msvc_name+".Deploy.0  = "+msvc_config+"\n")
		temp_lines.sort() #VS sorts these, at least in VS 2017.
		data += "".join(temp_lines)
		data += "\tEndGlobalSection\n"

		data += """\tGlobalSection(SolutionProperties) = preSolution
\t\tHideSolutionNode = FALSE
\tEndGlobalSection
"""

		data += "EndGlobal\n"

		path = self.project.directory_project_files.abspath + self.project.name+".sln"
		file = open(path,"w")
		file.write(data)
		file.close()

		return path

	def _generateFileProject       (self, target):
		#Note: the value for xmlns must be the dead link
		#	"http://schemas.microsoft.com/developer/msbuild/2003", not the more sensible
		#	"https://msdn.microsoft.com/en-us/library/5dy88c2e.aspx"
		data = """<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
\t<ItemGroup Label="ProjectConfigurations">"""
		for config in self.configurations:
			data += """
\t\t<ProjectConfiguration Include="%s">
\t\t\t<Configuration>%s</Configuration>
\t\t\t<Platform>%s</Platform>
\t\t</ProjectConfiguration>""" % (config._getMSVCConfigPlat(),config.name,config._getMSVCArch())
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
		for config in self.configurations:
			data += """\t<PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s'" Label="Configuration">
\t\t<ConfigurationType>%s</ConfigurationType>
\t\t<UseDebugLibraries>%s</UseDebugLibraries>
\t\t<PlatformToolset>%s</PlatformToolset>
\t</PropertyGroup>\n""" % (
			config._getMSVCConfigPlat(),
			target._getMSVCType(),
			"true" if config.build_options.is_debug else "false",
			config.toolchain._getMSVCName()
		)
		data += """\t<Import Project="$(VCTargetsPath)\Microsoft.Cpp.props"/>
\t<ImportGroup Label="ExtensionSettings"/>"""
		for config in self.configurations:
			data += """
\t<ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='%s'">
\t\t<Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform"/>
\t</ImportGroup>""" % (config._getMSVCConfigPlat())
		data += """
\t<PropertyGroup Label="UserMacros"/>
"""

		dirs_inc = []
		dirs_lib = []
		dep_libs = []
		for dep in target.dependencies_list_flat:
			for incl in dep.exported.dirs_incl_list:
				if incl.is_in_nobs_sys_dir: include=incl.abspath
				else:                       include=os.path.relpath( incl.abspath, self.project.directory_project_files.abspath ) + "\\"
				dirs_inc.append(_helpers.reslash(include))
			for libr in dep.exported.dirs_libroot_list:
				if libr.is_in_nobs_sys_dir: library=libr.abspath
				else:                       library=os.path.relpath( libr.abspath, self.project.directory_project_files.abspath ) + "\\"
				dirs_lib.append(_helpers.reslash(library))
			dep_libs += [ dep.name + ".lib" ]

		for config in self.configurations:
			data += """\t<PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s'">""" % (config._getMSVCConfigPlat())
			if target.type == _target._TargetBase.EXECUTABLE:
				data += """
\t\t<LinkIncremental>true</LinkIncremental>"""
			dir_out = _helpers.reslash(
				os.path.relpath(
					self.project.directory_build_result.   relpath+config.name_build,
					self.project.directory_project_files.abspath
				) +
				"\\"
			)
			dir_int = _helpers.reslash(
				os.path.relpath(
					self.project.directory_build_temporary.relpath+config.name_build+"/"+target.name,
					self.project.directory_project_files.abspath
				) +
				"\\"
			)
			data += """
\t\t<OutDir>%s</OutDir>
\t\t<IntDir>%s</IntDir>
""" % (dir_out,dir_int)
			if len(dirs_inc) > 0:
				data += "\t\t<IncludePath>"+"".join([dir_inc+";" for dir_inc in dirs_inc])+"$(IncludePath)</IncludePath>\n"
			if len(dirs_lib) > 0:
				data += "\t\t<LibraryPath>"+"".join([dir_lib+config.name_build+"/;" for dir_lib in dirs_lib])+"$(LibraryPath)</LibraryPath>\n"
			data += """\t</PropertyGroup>\n"""

		for config in self.configurations:
			data += "\t<ItemDefinitionGroup Condition=\"'$(Configuration)|$(Platform)'=='"+config._getMSVCConfigPlat()+"""'">
\t\t<ClCompile>
"""
			if len(config.additional_include_directories) > 0:
				data += "\t\t\t<AdditionalIncludeDirectories>"
				for d in config.additional_include_directories:
					data += _helpers.reslash( os.path.relpath(d.abspath,self.project.directory_project_files.abspath) ) + ";"
				data += "%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>\n"
			data +=\
"""\t\t\t<PrecompiledHeader>"""+("Use" if target.pch!=None else "NotUsing")+"""</PrecompiledHeader>
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
			data += "\t\t\t<BufferSecurityCheck>"+("true" if config.build_options.buffer_check else "false")+"</BufferSecurityCheck>\n"
			source_reldepth = max([_helpers.get_relative_depth(self.project.directory_project_root.abspath,self.project.directory_project_files.abspath),0])
			if source_reldepth > 0:
				data += "\t\t\t<ObjectFileName>$(IntDir)"+"/dummy"*source_reldepth+"/%(RelativeDir)/</ObjectFileName>\n"
			if target.type != _target._TargetBase.EXECUTABLE:
				data += "\t\t\t<ProgramDataBaseFileName>$(OutDir)$(ProjectName).pdb</ProgramDataBaseFileName>\n"
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
				relpath = _helpers.reslash( os.path.relpath(file.abspath,self.project.directory_project_files.abspath) )
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

		file = open(os.path.join(self.project.directory_project_files.abspath,target.name+".vcxproj"),"w")
		file.write(data)
		file.close()

	def _generateFileProjectFilters(self, target):
		files = target.headers_list + target.sources_list

		#Get a list of folders containing files
		folders = set(["."])
		#	Relative folders
		for file in files:
			relpath = os.path.relpath(file.absdir,self.project.directory_project_root.abspath)
			folders.add(relpath)
		#	Any intermediate folders must be specified too, apparently
		folders2 = folders.copy()
		for folder in folders:
			tmp = folder
			while tmp != ".":
				tmp = os.path.normpath(os.path.join(tmp,"../"))
				folders2.add(tmp)
		folders = folders2
		#	Remove identity directory
		folders.remove(".")
		#	Sort them
		folders = sorted(list(folders))
		#	Make them nice
		folders = [_helpers.reslash(folder) for folder in folders]

		#Note: the value for xmlns must be the dead link "http://schemas.microsoft.com/developer/msbuild/2003",
		#   not the more sensible https://msdn.microsoft.com/en-us/library/5dy88c2e.aspx
		data = """<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
\t<ItemGroup>
"""
		for folder in folders:
##            print("folder")
##            print(folder)
##            print("abspath")
##            print(project.directory_project_files.abspath)
##            print("done")
			data += "\t\t<Filter Include=\""+folder.replace("/","\\")+"""\">
\t\t\t<UniqueIdentifier>{"""+_helpers._get_uuid(folder)+"""}</UniqueIdentifier>
\t\t</Filter>
"""
		data += """\t</ItemGroup>
"""

		data_headers = ""
		data_sources = ""
		data_text    = ""
		for file in sorted(files,key=lambda file:file.abspath):
			relpath = _helpers.reslash( os.path.relpath(file.abspath,self.project.directory_project_files.abspath) )
			reldir  = _helpers.reslash( os.path.relpath(file.absdir, self.project.directory_project_root. abspath) )
			filter = reldir.replace("/","\\")
			if file.is_header:
				if filter == ".":
					data_headers += "\t\t<ClInclude Include=\""+relpath+"\"/>\n"
				else:
					data_headers += "\t\t<ClInclude Include=\""+relpath+"\">\n"
					data_headers += "\t\t\t<Filter>"+filter+"</Filter>\n"
					data_headers += "\t\t</ClInclude>\n"
			elif file.is_source:
				if filter == ".":
					data_sources += "\t\t<ClCompile Include=\""+relpath+"\"/>\n"
				else:
					data_sources += "\t\t<ClCompile Include=\""+relpath+"\">\n"
					data_sources += "\t\t\t<Filter>"+filter+"</Filter>\n"
					data_sources += "\t\t</ClCompile>\n"
			else:
				if filter == ".":
					data_text    += "\t\t<Text Include=\""+relpath+"\"/>\n"
				else:
					data_text    += "\t\t<Text Include=\""+relpath+"\">\n"
					data_text    += "\t\t\t<Filter>"+filter+"</Filter>\n"
					data_text    += "\t\t</Text>\n"
		if len(data_headers) > 0:
			data += "\t<ItemGroup>\n"+data_headers+"\t</ItemGroup>\n"
		if len(data_sources) > 0:
			data += "\t<ItemGroup>\n"+data_sources+"\t</ItemGroup>\n"
		if len(data_text   ) > 0:
			data += "\t<ItemGroup>\n"+data_text   +"\t</ItemGroup>\n"

		data += "</Project>"

		file = open(os.path.join(self.project.directory_project_files.abspath,target.name+".vcxproj.filters"),"w")
		file.write(data)
		file.close()

	def _generateFileProjectUser(self, target):
		file = open(os.path.join(self.project.directory_project_files.abspath,target.name+".vcxproj.user"),"w")
		file.write("""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
	<PropertyGroup/>
</Project>""")
		file.close()

class GeneratorVS2015(_GeneratorVS):
	def __init__(self, project):
		_GeneratorVS.__init__(self, project, 2015)

class GeneratorVS2017(_GeneratorVS):
	def __init__(self, project):
		_GeneratorVS.__init__(self, project, 2017)

GeneratorVS = GeneratorVS2017

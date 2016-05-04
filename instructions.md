# Instructions

NoBS is based on interpreting simple user-generated Python files (Python 2 or Python 3; it doesn't care).




To use NoBS, you write a single file for your whole solution.  Call it anything, but give it the extension ".nobs".

## Example







sln = nobs_sln("My Awesome Codebase")

sln.platforms.add_windows()
sln.platforms.add_linux()



sln.toolchains.add_gcc()
sln.toolchains.add_clang()
sln.toolchains.add_intel16()


nobs_build

nobs_compiler(






zlib.nobs-dep
	if nobs.
	
mycodebase.nobs-sol
```python
nobs_sln = {
	name : "My Awesome Codebase", #name
	configs : [
		nobs_staticlib(
			"Library 1"
			
		)
	]
}
```

	nobs_define_
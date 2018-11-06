# NoBS

A KISS System for C++ Windows/Linux Builds

## Motivation

My needs are simple: a simple, reliable, portable C++ build system that generates MSVC solution/projects and Linux GMake files, targeting x86, x86-64, and ARM.  I would have thought that such a setup was common and well-supported.  But I was wrong.

I have used several build tools, a development nightmare of ports and transitions from one to the other.  Some, I have switched to/from multiple times, as new patches make one marginally less sucky than others.  Through it all, I became more and more angry: it has been years—decades!—since C++ was introduced.  And yet, build tools for them are still somehow woefully inadequate for even the most obvious tasks.  Let's examine some common build systems:

- CMake: Probably the most-widely-used build tool, CMake suffers from overcomplexity and user-unfriendliness, with bad, bloated syntax and incomplete or incorrect documentation.  Windows support is barely an afterthought, with obvious failures such as lack-of-recursive-file-listing and utter absence of such important features as supporting-multiarch-in-one-solution.
- Premake: My build system of choice for a long time, Premake has evolved dramatically.  The project has lofty aims, but is unfortunately understaffed.  The outstanding bug list is, well, _outstanding_, and development is slow.  The documentation, various versions of which exist on at least three different websites, is occasionally satisfactory, but frequently misleading.  Still lacks important features, like proper post-build-event and build customizations, as well as e.g. putting include directories in the right place.  If you want to contribute to a build system, do it for this one.

So, I resolved to build my own.

## Philosophy

Part of the problem is the variety of build configurations in-use.  Some files can be auto-generated, or maybe you want to link in some JVM thing or run a custom build script or I don't care.

NoBS largely rejects such frivolousness.

NoBS is designed for simplicity first; it doesn't do very much, but it does it competently.  This requires imposing parochial and occasionally ruthless limitations.  NoBS is not sorry.

NoBS essentially supports hierarchical, ordered builds of multiple "targets" (executables, static libraries, or dynamic libraries) that are grouped into "projects".  Each project has:

1. (Optionally) a precompiled-header build step (nonparallel)
2. A compile step (parallel)
3. A link step (nonparallel)
3. (Optionally) a post-build run-a-script step (nonparallel)

Each project has at least one (but as many as you like) "configuration"s, which are (platform,architecture,compiler+flags,build-options) tuples.  For example, (linux,x86-64,gcc,debug).  There are more details, but this is the overall picture, and is the only thing NoBS supports.  I call it, self-consciously, the "One True Build Setup" (OTBS).

## Usage

Make a Python script somewhere and put in your project's configuration.  There are examples and documentation to help you do this.  Then run it; it will generate all the stuff you asked it to.

Note: Python 3.5+ is required to use modern globbing.

## Contributing and Feature Requests

Your patches and pull requests are welcome.  However, I will demand a very high standard of quality and elegance.  Implementations for other platforms, such as e.g. XCode, would be highly appreciated.

For feature requests, don't hold your breath.  Anything that improves the OTBS is probably something I want as well.  If you want something else, I'll take note, but probably it won't happen—even if you write the code and give it to me yourself.  NoBS aims to be simple first, not powerful.
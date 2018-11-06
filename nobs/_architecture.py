class Architecture(object):
	ARCH_X86 = 0
	ARCH_X86_64 = 1
	ARCH_ARM = 2

	def __init__(self, search_name):
		if   search_name == "x86":
			self.type = Architecture.ARCH_X86
		elif search_name == "x86-64":
			self.type = Architecture.ARCH_X86_64
		elif search_name == "ARM":
			self.type = Architecture.ARCH_ARM
		else:
			raise Exception("Unrecognized architecture \""+str(search_name)+"\"!  Supported architectures are { \"x86\", \"x86-64\", \"ARM\" }.")

	def _validateBasic(self):
		pass

import hashlib
import os
import subprocess
import uuid


##_inited = False
##_script_absdir = None
##def init(script_absdir):
##    global _inited
##    global _script_absdir
##    
##    if not isinstance(script_absdir,str): raise Exception("Absolute path must be a string!")
##    if not os.path.exists(script_absdir):
##        raise Exception("Could not find absolute directory \""+script_absdir+"\"!")
##    _script_absdir = script_absdir
##    
##    _inited = True

def _get_uuid(name=None):
	if name == None:
		u = uuid.uuid4() #Random UUID
	else:
		#Note: the namespace doesn't really matter.  It's just an input to the hashing function.
		u = uuid.uuid5(uuid.NAMESPACE_X500,name) #SHA-1 deterministic UUID
	return str(u).upper()

def get_file_hash(path):
	h = hashlib.sha256()
	with open(path,"rb") as file:
		for chunk in iter(lambda:file.read(4096),b""):
			h.update(chunk)
	return h.hexdigest()

def reslash(path):
	return path.replace("\\","/")

def overwrite_symlink(source, link, print_with_indent=None):
	if print_with_indent != None:
		print(" "*print_with_indent + "Making \""+link+"\" -> \""+source+"\"")

	#On Windows, must apparently be absolute paths with backslashes (or else the symlink will
	#	complete, but the result will be invalid).
	source = os.path.normpath(os.path.abspath(source))
	link   = os.path.normpath(os.path.abspath(link  ))

	if os.path.exists(link):
		#print("  (deleting old first)")
		if os.path.isdir(link): os.rmdir (link)
		else:                   os.unlink(link)

	os.symlink(source,link)

def get_relative_depth(path1,path2):
	path1 = os.path.normpath(path1)
	path2 = os.path.normpath(path2)
	common = os.path.commonpath((path1,path2))
	depth1=0; depth2=0
	while path1 != common:
		path1 = os.path.normpath(os.path.join(path1,"../"))
		depth1 += 1
	while path2 != common:
		path2 = os.path.normpath(os.path.join(path2,"../"))
		depth2 += 1
	return depth2 - depth1

def run_subproc(cmd,print_invocation=True):
	if print_invocation:
		print("  Running in subprocess: \"%s\""%cmd)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	stdout,stderr = p.communicate()
	if p.returncode != 0:
		err = ""
		if stdout!=None: err+=stdout.decode("utf-8")
		if stderr!=None: err+=stderr.decode("utf-8")
		print(err)
		raise Exception(err)

def _error(msg):
	raise Exception("Fatal Error: "+msg)
def _errorinstance(name,type_or_types):
	if type(type_or_types) == type([]):
		s = ""
		for t in type_or_types: s+=t.__name__+", "
		s = s[:-2]
		_error(name+" must be an instance of { "+s+" }!")
	else:
		_error(name+" must be an instance of `nobs."+type_or_types.__name__+"`!")
def _warning(msg):
	print("Warning: "+msg)
def _check_type(var,name,type_or_types):
	if type(type_or_types) == type([]):
		for t in type_or_types:
			if isinstance(var,t): return
	else:
		if isinstance(var,type_or_types): return
	_errorinstance(name,type_or_types)

try:
	strinput = raw_input
except:
	strinput = input

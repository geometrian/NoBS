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

try:
    strinput = raw_input
except:
    strinput = input

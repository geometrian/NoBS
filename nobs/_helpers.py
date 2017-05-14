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

def _reslash(path):
    return path.replace("\\","/")

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path,"rb") as file:
        for chunk in iter(lambda:file.read(4096),b""):
            h.update(chunk)
    return h.hexdigest()

def run_bat(path):
    p = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE)
    stdout,stderr = p.communicate()
    if p.returncode != 0:
        raise Exception((stdout+stderr).decode("utf-8"))

try:
    strinput = raw_input
except:
    strinput = input

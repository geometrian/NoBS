import os
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

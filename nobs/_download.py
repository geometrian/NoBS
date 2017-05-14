import sys
try:
    import urllib.request
    python3 = True
except ImportError:
    import urllib2
    python3 = False


def download_progress_callback_simple(downloaded,total):
    sys.stdout.write(
        "\r" +
        (len(str(total))-len(str(downloaded)))*" " + str(downloaded) + "/%d"%total +
        " [%3.2f%%]"%(100.0*float(downloaded)/float(total))
    )
    sys.stdout.flush()

def _download_helper(srcurl, out_obj, progress_callback, block_size):
    def _download_op(response, file_size):
        if progress_callback!=None: progress_callback(0,file_size)
        if block_size == None:
            buffer = response.read()
            out_obj.write(buffer)
            
            if progress_callback!=None: progress_callback(file_size,file_size)
        else:
            file_size_dl = 0
            while True:
                buffer = response.read(block_size)
                if not buffer: break

                file_size_dl += len(buffer)
                out_obj.write(buffer)

                if progress_callback!=None: progress_callback(file_size_dl,file_size)
    if python3:
        with urllib.request.urlopen(srcurl) as response:
            #meta = response.info()
            file_size = int(response.getheader("Content-Length"))
            _download_op(response,file_size)
    else:
        response = urllib2.urlopen(srcurl)
        meta = response.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        _download_op(response,file_size)
def download_to_file(srcurl, dstfilepath, progress_callback=None, block_size=8192):
    with open(dstfilepath,"wb") as out_file:
        _download_helper(srcurl, out_file, progress_callback, block_size)
def download_to_mem(srcurl, progress_callback=None, block_size=8192):
    class Wrapper(object):
        def __init__(self): self.data=bytes()
        def write(self, buffer): self.data+=buffer
    data = Wrapper()
    _download_helper(srcurl, data, progress_callback, block_size)
    return data.data

##import traceback
##try:
##    srcurl = "https://geometrian.com/data/programming/projects/glLib/glLib%20Reloaded%200.5.9/0.5.9.zip"
####    dstfile = "test dl output.zip"
####    download_to_file(srcurl,dstfile,download_progress_callback_simple)
##    data = download_to_mem(srcurl, download_progress_callback_simple)
##except:
##    traceback.print_exc()
##    input()

#!/usr/bin/python

import urllib2
import os

def fetchHttpFile(url, tmpdir):
	# http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python

    print "> fetch: %s" % url
    os.chdir(tmpdir)

    # put sources in ~/rpmbuild/SOURCES
    #srcdir = os.path.join(os.environ['HOME'], 'rpmbuild', 'SOURCES')
    #assert os.path.isdir(srcdir), "please create %s" % srcdir

    file_name = url.split('/')[-1]
    #file_name = os.path.join(srcdir, file_name)

    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    #import epdb; epdb.st()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

    return file_name

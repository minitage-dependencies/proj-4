
import os,sys

import urllib2
import zipfile
from minitage.core.unpackers.interfaces import IUnpackerFactory
from minitage.core.common import test_md5,md5sum

def installmaps(options,buildout):
    # adding maps files
    dest = '%s/nad' % options['compile-directory']
    url = options['mapsurl'].strip()
    md5 = options['mapsmd5'].strip()
    ldest = os.path.join(buildout['buildout']['directory'], os.path.basename(url))
    dl = True
    if os.path.exists(ldest):
        dl = False
        if not test_md5(ldest, md5):
            print 'md5 does not match redownload'
            dl = True
    if dl:
        print "Downloading mapfiles (nad) from %s" % url
        try:
            contents = urllib2.urlopen(url).read()
            s = open(ldest, 'wb')
            s.write(contents)
            s.flush()
            s.close()
            if not test_md5(ldest, md5):
                raise Exception('md5 does not match')
        except Exception, e:
            print "!!! Problem while downloading/writing to disk !!!"
            print e
            os.remove(ldest)
            sys.exit(-1)
    else:
        print "mapfiles alreazdy present, do not redownload"
        

    if os.path.exists(ldest):
        print "Extracting  mapfiles"
        f = IUnpackerFactory()
        unpacker = f(ldest)
        unpacker.unpack(ldest, dest)



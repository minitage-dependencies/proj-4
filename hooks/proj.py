
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
        
def h(options,buildout):
    if sys.platform.startswith('cygwin'):
        print
        print 'Reconfiguring'
        print
        c = os.getcwd()
        os.chdir(options['compile-directory'])
        os.system("autoreconf -ifv")
    installmaps(options, buildout)

def p(options, buildout):
    ip = os.path.join(options['location'], 'share', 'proj', 'epsg')
    fp = open(ip, 'a')
    fp.write("""
# Google Spherical Mercator projection
<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over<> 
""")
    fp.flush()
    fp.close()



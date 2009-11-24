
import os,sys

import urllib2
import zipfile

def installmaps(options,buildout):
    # adding maps files
    dest = '%s/nad' % options['compile-directory']
    url = options['mapsurl'].strip()
    ldest = os.path.join(buildout['buildout']['directory'], os.path.basename(url))
    if not os.path.exists(ldest):
        print "Downloading mapfiles (nad) from %s" % url
        try:
            contents = urllib2.urlopen(url).read()
            s = open(ldest, 'wb')
            s.write(contents)
            s.flush()
            s.close()
        except Exception, e:
            print "Problem while downloading/writing to disk"
            print e
            os.remove(ldest)
            sys.exit(-1)
    else:
        print "mapfiles alreazdy present, do not redownload"

    if os.path.exists(ldest):
        print "Extracting  mapfiles"
        zip = zipfile.ZipFile(open(ldest))
        zip.extractall(dest)  



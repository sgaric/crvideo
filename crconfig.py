import os, json, errno

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CRConfiguration(QDialog):
    defaultconfig = { u'sourcedirs': set((u'/private/var/folders',)), 
                     u'destdir': u'/Users/account/Movies/CRVideo'}
    defaultconfigfile = '/Users/account/.crvideo'
    
    def __init__(self, parent=None):
        super(CRConfiguration, self).__init__(parent)
        self.sourcedirs = set(())
        self.destdir = ''
        self.setdefaultconfig()
    
    def setdefaultconfig(self):
        pathcomponents = str(CRConfiguration.defaultconfig[u'destdir']).split(os.sep)
        # index 0 corresponds to an empty string from the leading '/' of the path
        if pathcomponents[1].lower() == 'users':
            pathcomponents[2] = os.environ['LOGNAME']
            CRConfiguration.defaultconfig[u'destdir'] = unicode(os.sep.join(pathcomponents))
        
            CRConfiguration.defaultconfigfile = os.sep.join(pathcomponents[:3] + ['.crvideo'])
        else:
            CRConfiguration.defaultconfigfile = os.sep.join(['', 'Users', 
                                                           os.environ['LOGNAME'], '.crvideo'])
  
    def loadconfig(self):
        try:
            fp = open(CRConfiguration.defaultconfigfile, 'rb')
            config = json.load(fp)
            fp.close()
            
            self.sourcedirs = set(config[u'sourcedirs'])
            self.destdir = config[u'destdir']
            if not os.path.exists(self.destdir):
                os.makedirs(self.destdir, 0700)
        except IOError, e:
            if e.errno == errno.ENOENT:
                self.sourcedirs = CRConfiguration.defaultconfig[u'sourcedirs']
                self.destdir = CRConfiguration.defaultconfig[u'destdir']
                self.storeconfig()
            else:
                raise
        except OSError, e:
            if e.errno == errno.EACCES:
                print "Permission Denied: Cannot create %s directory" % self.destdir
            else:
                raise
       
    def storeconfig(self, default=False):
        fp = open(CRConfiguration.defaultconfigfile, 'wb')
        if default:
            json.dump(CRConfiguration.defaultconfig, fp, indent=1)
        else:
            config = {u'sourcedirs': list(self.sourcedirs), 
                      u'destdir': self.destdir}
            json.dump(config, fp, indent=1)
        
        fp.close()
    
    def setsources(self, sources):
        self.sourcedirs = sources
        
    def addsource(self, source):
        self.sourcedirs.add(source)
        
    def removesource(self, source):
        self.sourcedirs.remove(source)
        
    def getsources(self):
        return self.sourcedirs
    
    def setdestination(self, dest):
        self.destdir = dest
        
    def getdestination(self):
        return self.destdir
    
    def __str__(self):
        return `self.sourcedirs, self.destdir`
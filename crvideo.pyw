# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
####################################################################
#    
#    CRVIDEO Application - Find and copy mp4 and mkv files hidden in private folders
#    Copyright (C) 2012 Slavisa Garic
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
####################################################################

import subprocess
import json

import sys
import os
import shutil
import errno
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from crconfig import CRConfiguration
from crconfigdialog import ConfigDialog
from crcopyCFEdialog import MapShownameDialog

MAC = "qt_mac_set_native_menubar" in dir()


            
class CRVideoDialog(QDialog):

    def __init__(self, parent=None):
        super(CRVideoDialog, self).__init__(parent)
        
        self.configObj = CRConfiguration()
        self.configObj.loadconfig()
        
        self.files = {}
        self.destfiles = []
        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.searchWidget = QLineEdit()
        buttonLayout = QVBoxLayout()
        for text, slot in (("&Copy...", self.copy),
                           ("&Move...", self.move),
                           ("&Config...", self.config)):
            button = QPushButton(text)
            if not MAC:
                button.setFocusPolicy(Qt.NoFocus)
            
            buttonLayout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)
            
        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.setWindowTitle("DDM Cache Search")
        self.search()

        
    def loaddestfiles(self):
        import glob
        self.destfiles = []
        destfiles = glob.glob(os.path.join(self.configObj.getdestination(), '*.mp4'))
        for dfile in destfiles:
            self.destfiles.append(os.path.basename(dfile))
        destfiles = glob.glob(os.path.join(self.configObj.getdestination(), '*.mkv'))
        for dfile in destfiles:
            self.destfiles.append(os.path.basename(dfile))
        
        destfiles = glob.glob(os.path.join(self.configObj.getdestination(), '*.cfE'))
        for dfile in destfiles:
            self.destfiles.append(os.path.basename(dfile))
         
    def search(self): # Idea taken from the Python Cookbook
        output = ''
        self.loaddestfiles()
        self.listWidget.clear()
        self.files = {}
        for source in self.configObj.getsources():
            args = ['/usr/bin/find', source, '-iname', "*.[cm][pkf][4vE]"]
            try:
                p = subprocess.Popen(args, stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, shell=False)
                output 	= p.communicate()[0]
            except:
                raise

            searchfor = unicode(self.searchWidget.text());
            lines = output.split()
            
            for line in lines:
                if (len(searchfor) == 0 or (line.lower().find(searchfor.lower()) >= 0)) and \
                    (line.endswith('.mp4') or line.endswith('.mkv') or line.endswith('.cfE')):
                    if os.path.basename(line) not in self.destfiles:
                        llabel = time.strftime("Created_%Y-%m-%d_%I-%M%p", time.localtime(os.path.getctime(line)))
                        appendOriginalName = True
                        if line.endswith(".cfE"):
                            parts = os.path.basename(line).split(".")
                            key = parts[0]
                            if len(parts) > 3:
                                key = '.'.join(parts[0:2])
                            value = self.configObj.getmapping(key)
                            if value is not None:
                                llabel = value + "_" + llabel
                                appendOriginalName = False
                                    
                        if appendOriginalName:
                            llabel = os.path.basename(line) + "_" + llabel

                        if llabel + ".mp4" not in self.destfiles:
                            self.files[llabel] = line
        
        self.listWidget.addItems(self.files.keys())
        self.listWidget.setMinimumWidth(self.listWidget.sizeHintForColumn(0)+5)
        self.listWidget.setMaximumHeight(130)
        
        
    def copy(self):
        for item in self.listWidget.selectedItems():
            move = False
            destination = str(item.text())
            if self.files[str(item.text())].endswith(".cfE"):
                destination = self.getFilenameForCFE(item)
                move = True
            
            if move:
                shutil.move(self.files[str(item.text())], 
                    os.path.join(self.configObj.getdestination(), destination))
            else:
                shutil.copy(self.files[str(item.text())], 
                    os.path.join(self.configObj.getdestination(), destination))
            self.listWidget.takeItem(self.listWidget.row(item))

            del item
            
    def move(self):
        for item in self.listWidget.selectedItems():
            destination = str(item.text())
            if self.files[str(item.text())].endswith(".cfE"):
                destination = self.getFilenameForCFE(item)

            shutil.move(self.files[str(item.text())], 
                    os.path.join(self.configObj.getdestination(), destination))
            self.listWidget.takeItem(self.listWidget.row(item))
            del item

    def getFilenameForCFE(self, item):
        destination = str(item.text()) + ".mp4"
        parts = os.path.basename(self.files[str(item.text())]).split(".")
        key = parts[0]
        if len(parts) > 3:
            key = '.'.join(parts[0:2])
        value = self.configObj.getmapping(key)

        dialog = MapShownameDialog()
        if value is not None:
            dialog.setshowname(value)
            dialog.disableShownameQLineEdit()
                
        if dialog.exec_():
            #should again raise error message
            showname = dialog.getshowname()
            episode = dialog.getepisode()
            season = dialog.getseason()

            llabel = ''
            if len(episode) == 0 and len(season) == 0:
                llabel = time.strftime("_Created_%Y-%m-%d_%I-%M%p", time.localtime(os.path.getctime(self.files[str(item.text())])))
            else:
                if len(season) > 0:
                    llabel = llabel + "S" + season
                if len(episode) > 0:
                    llabel = llabel + "E" + episode
                            
            destination = showname + llabel + ".mp4"

            print destination
            self.configObj.setmapping(key, showname)
            self.configObj.storeconfig()
        
        return destination

    def config(self):
        dialog = ConfigDialog()
        if dialog.exec_():
            self.configObj = dialog.getconfigdetails()
            self.loaddestfiles()
            self.search()
            self.configObj.storeconfig()
   
#fp = open(os.path.join(os.environ['HOME'], ".crvideo.json"))
#config = json.load(fp)
#sourcedirs = config[u'sourcedirs'] 
app = QApplication(sys.argv)
form = CRVideoDialog()
form.show()
app.exec_()


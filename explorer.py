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

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *


MAC = "qt_mac_set_native_menubar" in dir()

class DirExplorer(QDialog):
    def __init__(self, currentSelection="", startPath="", 
                 treefilter=QDir.NoDotAndDotDot | QDir.AllDirs, parent=None):
        super(DirExplorer, self).__init__(parent)
        self.currentSelection = currentSelection
        self.selection = ""
        self.name = "Select Directory"
        self.treeview = QTreeView()
        
        font = QFont()
        font.setUnderline(True)
        font.setBold(True)
        font.setItalic(True)
        
        title = QLabel("/Users/%s :" % os.environ['LOGNAME'])
        title.setFont(font)
        firstLine = DirExplorer._createLine(self, "sep1")
        confirmBBox = QDialogButtonBox(QDialogButtonBox.Cancel|
                                     QDialogButtonBox.Ok)

        self.startPath = startPath if startPath != "" else u"/Users/%s" % os.environ['LOGNAME']
        self.dirmodel = QDirModel(self)
        self.dirmodel.setFilter(treefilter)
        
        startIndex = self.dirmodel.index(self.startPath) 
        selectionIndex = self.dirmodel.index(self.currentSelection)
        
        self.treeview.setModel(self.dirmodel)
        self.treeview.setRootIndex(startIndex)
        self.treeview.expand(selectionIndex)
        self.treeview.resizeColumnToContents(0)
        self.treeview.setHeaderHidden(True)
        self.treeview.setCurrentIndex(selectionIndex)
        self.treeview.scrollTo(selectionIndex)
        
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        
        
        self.connect(confirmBBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(confirmBBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        
        
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(firstLine)
        layout.addWidget(self.treeview)
        layout.addWidget(confirmBBox)
        self.setLayout(layout)
        
    
        
    def accept(self):
        index = self.treeview.selectionModel().selectedIndexes()[0]
        self.selection = unicode(str(self.dirmodel.fileInfo(index).absoluteFilePath()))
        QDialog.accept(self)
    
    def getselection(self):
        return self.selection
    
    @staticmethod
    def _createLine(parent, label, height=3):
        line = QFrame(parent=parent)
        line.setObjectName(label)
        line.setGeometry(QRect(320, 150, 118, height))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    form = DirExplorer("/Users/slavisa/Movies/CRVideo", startPath="/.")
    form.show()
    app.exec_()

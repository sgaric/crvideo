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
from crconfig import CRConfiguration
from explorer import DirExplorer
        

MAC = "qt_mac_set_native_menubar" in dir()

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.name = "Configuration"
        self.configObj = CRConfiguration()
        self.configObj.loadconfig()
        sLabel = QLabel("Source Directories")
        dLabel = QLabel("Destination Directory")
        
        font = QFont()
        font.setUnderline(True)
        font.setBold(True)
        font.setItalic(True)
        
        sLabel.setFont(font)
        dLabel.setFont(font)
        
        firstLine = DirExplorer._createLine(self, "sep1")
        secondLine = DirExplorer._createLine(self, "sep2")
        thirdLine = DirExplorer._createLine(self, "sep3")
        self.listWidget = QListWidget()
        self.destination = QLineEdit()
        self.destination.setEnabled(False)
        #self.destination.setMinimumWidth(self)
        confirmBBox = QDialogButtonBox(QDialogButtonBox.Cancel|
                                     QDialogButtonBox.Ok)
        

        grid = QGridLayout()
        grid.addWidget(sLabel, 0, 0)
        grid.addWidget(firstLine, 1, 0, 1, 2)
        grid.addWidget(self.listWidget, 2, 0, 3, 1)
        
        for text, slot, x, y in (("&Add", self.add, 2, 1),
                           ("&Edit", self.edit, 3, 1),
                           ("&Delete", self.delete, 4, 1),
                           ("&Set Destination", self.updatedest, 10, 1)):
            
            button = QPushButton(text)
            if not MAC:
                button.setFocusPolicy(Qt.NoFocus)
             
            self.connect(button, SIGNAL("clicked()"), slot)
            
            grid.addWidget(button, x, y)
            
        grid.addWidget(secondLine, 6, 0, 1, 2) 
        grid.addWidget(dLabel, 8, 0)
        grid.addWidget(thirdLine, 9, 0, 1, 2) 
        grid.addWidget(self.destination, 10, 0)
        grid.addWidget(confirmBBox, 11, 0, 1, 2)
        self.setLayout(grid)
        
        self.connect(confirmBBox, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(confirmBBox, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        
        self.setup()
        self.listWidget.setMinimumWidth(self.listWidget.sizeHintForColumn(0)+5)
        self.listWidget.setMaximumHeight(130)
    
    def setup(self):
        self.listWidget.addItems(list(self.configObj.getsources()))
        self.destination.setText(self.configObj.getdestination())
    
    
    def add(self):
        dialog = DirExplorer(treefilter=QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Hidden,
                             startPath="/",
                             parent=self)
        if dialog.exec_():
            addsource = True
            removesources = False
            selection = dialog.getselection()
            for source in self.configObj.getsources():
                if source in selection:
                    addsource = False
                    quickNote = QMessageBox()
                    quickNote.setText("Path not added as parent directory already a source")
                    quickNote.setInformativeText("Parent path:%s" % source)
                    quickNote.exec_()
                    break
                elif selection in source:
                    quickNote = QMessageBox()
                    reply = QMessageBox.question(self, "Check sources",
                        "Some of the current sources are under `%s' directory. Do you want to remove them from the list?" % dialog.getselection(),
                        QMessageBox.Abort|QMessageBox.No|QMessageBox.Yes)
                    
                    if reply == QMessageBox.Yes:
                        removesources = True
                    elif reply == QMessageBox.Abort:
                        addsource = False
                    break
    
            if removesources:  
                for row in range(self.listWidget.count()):
                    item = self.listWidget.item(row)     
                    if selection == str(item.text())[0:len(selection)]:
                        self.configObj.removesource(str(item.text()))
                        item = self.listWidget.takeItem(row)
                        del item
                                           
            if addsource:
                self.listWidget.addItem(selection)
                self.configObj.addsource(selection)

            
    
    def edit(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        oldsrc = unicode(str(item.text()))
        if item is not None:
            title = "Edit Source Directory"
            string, ok = QInputDialog.getText(self, title, title,
                                QLineEdit.Normal, item.text())
            if ok and not string.isEmpty():
                item.setText(string)
                self.configObj.addsource(unicode(str(string)))
                self.configObj.removesource(oldsrc)
                
    def delete(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "Remove",
                        "Remove source `%s'?" % unicode(item.text()),
                        QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.listWidget.takeItem(row)
            self.configObj.removesource(str(item.text()))
            del item
        
            
    def updatedest(self):
        current = str(self.destination.text())
        dialog = DirExplorer(currentSelection=current, parent=self)
        if dialog.exec_():
            self.configObj.setdestination(dialog.getselection())
            self.destination.setText(self.configObj.getdestination())
            
        
    def getconfigdetails(self):
        return self.configObj
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ConfigDialog()
    form.show()
    app.exec_()

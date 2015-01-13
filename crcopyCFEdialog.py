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
from explorer import DirExplorer
        

MAC = "qt_mac_set_native_menubar" in dir()

class MapShownameDialog(QDialog):
    def __init__(self, parent=None):
        super(MapShownameDialog, self).__init__(parent)

        self.showname = None
        self.season = None
        self.episode = None

        self.name = "Moving cfE file Dialog"
        shownameQLabel = QLabel("Enter ShowName: ")
        seasonQLabel = QLabel("Enter Season Number: ")
        episodeQLabel = QLabel("Enter Episode Number: ")
        
        font = QFont()
        font.setBold(True)
        
        shownameQLabel.setFont(font)
        seasonQLabel.setFont(font)
        episodeQLabel.setFont(font)
        
        firstLine = DirExplorer._createLine(self, "sep1")
        self.shownameQLineEdit = QLineEdit()
        self.shownameQLineEdit.setEnabled(True)
        self.seasonQLineEdit = QLineEdit()
        self.seasonQLineEdit.setEnabled(True)
        self.seasonQLineEdit.setInputMask("99")
        self.episodeQLineEdit = QLineEdit()
        self.episodeQLineEdit.setEnabled(True)
        self.episodeQLineEdit.setInputMask("99")

        grid = QGridLayout()
        grid.addWidget(shownameQLabel, 0, 0)
        grid.addWidget(self.shownameQLineEdit, 0, 1)
        grid.addWidget(seasonQLabel, 1, 0)
        grid.addWidget(self.seasonQLineEdit, 1, 1)
        grid.addWidget(episodeQLabel, 2, 0)
        grid.addWidget(self.episodeQLineEdit, 2, 1)
            
        button = QPushButton("&Set Values")
        if not MAC:
            button.setFocusPolicy(Qt.NoFocus)
             
        self.connect(button, SIGNAL("clicked()"), self.setvalues)
        grid.addWidget(button, 1, 2)
            
        self.setLayout(grid)
        
    def setvalues(self):
        if self.shownameQLineEdit.text() is None or \
           len(str(self.shownameQLineEdit.text())) == 0:
            return
                #but should display dialog that name must be entered
        else:
            self.setshowname(str(self.shownameQLineEdit.text()))
            self.setseason(str(self.seasonQLineEdit.text()))
            self.setepisode(str(self.episodeQLineEdit.text()))
            self.accept()


    def disableShownameQLineEdit(self):
        self.shownameQLineEdit.setEnabled(False)

    def setshowname(self, showname):
        self.showname = showname
        self.shownameQLineEdit.setText(showname)
        self.shownameQLineEdit.setEnabled(False)

    def setseason(self, season):
        self.season = season
    
    def setepisode(self, episode):
        self.episode = episode
    
    def getshowname(self):
        return self.showname

    def getseason(self):
        return self.season

    def getepisode(self):
        return self.episode

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MapShownameDialog()
    form.setshowname("Slavisa Garic")
    form.setshowname("Slavisa Garic")
    form.setshowname("Slavisa Garic")
    form.setshowname("Slavisa Garic")
    form.show()
    app.exec_()

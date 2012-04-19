import subprocess, json
import sys, os, shutil, errno

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from crconfig import CRConfiguration
from crconfigdialog import ConfigDialog

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
         
    def search(self): # Idea taken from the Python Cookbook
        output = ''
        self.loaddestfiles()
        self.listWidget.clear()
        self.files = {}
        for source in self.configObj.getsources():
            args = ['/usr/bin/find', source, '-iname', "*.mp4*"]
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
                    line.endswith('.mp4'):
                    if os.path.basename(line) not in self.destfiles:
                        self.files[os.path.basename(line)] = line
            
        self.listWidget.addItems(self.files.keys())
        self.listWidget.setMinimumWidth(self.listWidget.sizeHintForColumn(0)+5)
        self.listWidget.setMaximumHeight(130)
        
        
    def copy(self):
        for item in self.listWidget.selectedItems():
            shutil.copy(self.files[str(item.text())], 
                    os.path.join(self.configObj.getdestination(), str(item.text())))
            self.listWidget.takeItem(self.listWidget.row(item))
            del item
            
    def move(self):
        for item in self.listWidget.selectedItems():
            shutil.move(self.files[str(item.text())], 
                    os.path.join(self.configObj.getdestination(), str(item.text())))
            self.listWidget.takeItem(self.listWidget.row(item))
            del item
    
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


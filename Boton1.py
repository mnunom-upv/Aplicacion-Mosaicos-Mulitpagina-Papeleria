
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from PIL.ImageQt import ImageQt, Image
from PIL import ImageGrab, Image
from PyQt5.QtWidgets import QWidget, QShortcut, QApplication, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys




class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def getTextUp (self):
        return (self.textUpQLabel.text)#setText(text)

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath,pixmapita):
        #qpixi = QPixmap(imagePath)
        low_rez = QSize(150, 150)
        high_rez = QSize(400, 400)
        pixmap = QPixmap(imagePath)

        pixmap = pixmapita.scaled(low_rez)
        self.iconQLabel.setPixmap(pixmap)

        
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'System for '
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.Lista=[]
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.msgSc = QShortcut(QKeySequence('Ctrl+V'), self)
        self.msgSc.activated.connect(self.on_click)

        self.myQListWidget = QListWidget(self)
        self.myQListWidget.setGeometry(10, 10, 800, 600)
        self.myQListWidget.itemClicked.connect(self.itemSeleccionado)


        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(900,300)
        button.clicked.connect(self.on_click)
        
        self.show()
    def itemSeleccionado (self):
        #self.myQListWidget.currentItem().textDownQLabel.text
        #print ("pluto",self.myQListWidget.currentItem().textDownQLabel.text)
        #item = self.myQListWidget.item(0)
        #widget = self.ui.listWidget.itemWidget(item)
        print ("pluto")
        #Obj = (QCustomQWidget) ( self.myQListWidget.currentItem() )
        #print (Obj.getTextUp())
        #print(self.myQListWidget.getItemWidget())


        #item = self.myQListWidget.itemWidget()
        #print (item)
        #text = item.getTextUp()
        print(self.myQListWidget.currentIndex())
        print(self.myQListWidget.currentRow())
        print(self.myQListWidget.count())
        print(self.Lista.get(0))
 
        #print(self.myQListWidget.currentIndex().getTextUp())

    def funcionRara (self):

        for index, name, icon in [('No.1', 'Meyoko',  'C:\\Users\\alici\\OneDrive\\Documentos\\mujer.jpg'),
            ('No.2', 'Nyaruko', 'C:\\Users\\alici\\OneDrive\\Documentos\\mujer.jpg'),
            ('No.3', 'Louise',  'C:\\Users\\alici\\OneDrive\\Documentos\\mujer.jpg')]:
            print (name)
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.Lista.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        img = ImageGrab.grabclipboard()
        print(img)
        # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=200x71 at 0x105E68700>

        if isinstance(img, Image.Image):
            # True

            print(img.size)
            # (200, 71)

            print(img.mode)
            # RGB

            pixmapita = None

            self.img = ImageQt(img)
            pixmapita = QPixmap.fromImage(self.img)            
            #pixmapita = QPixmap(ImageQt.ImageQt(img))

            #img.save('data/temp/clipboard_image.jpg')
                    # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp('0')
            myQCustomQWidget.setTextDown(str(img.size))
            myQCustomQWidget.setIcon('C:\\Users\\alici\\OneDrive\\Documentos\\mujer.jpg',pixmapita)
                # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

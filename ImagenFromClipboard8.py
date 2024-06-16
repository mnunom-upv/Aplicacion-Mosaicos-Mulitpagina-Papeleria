"""
Permite copiar de "Memoria" las imagenes, las guarda en la carpeta "HOME"
La idea es integarla con el programa "AComodar N imagenes en Hoja Carta" para completar el formateador de imagenes
"""

from AcomodarNimagenesEnHojaCartaInterfaz import AcomodoImagenes
import sys
#from PyQt4 import QtCore, QtGui
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget,  QGridLayout, QListWidget,  QListWidgetItem, QPushButton
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

#import gi
#gi.require_version("Gtk", "3.0")
#from gi.repository import Gtk, Gdk
from PIL import Image as PILImage, ImageQt
from PIL import Image 
from PIL import ImageGrab, Image

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modificar Lista de Operaciones")
        self.botonA = QPushButton("Eliminar Imagen Actual")
        self.botonB = QPushButton("Duplicar Imagen Actual")
        self.botonA.clicked.connect(self.Vamonos)
        self.botonB.clicked.connect(self.Vamonos2)				

        self.layout = QVBoxLayout()
        message = QLabel("Operaciones Permitidas Sobre La Lista de Imágenes")
        message.setMinimumSize(300, 200)
        self.layout.addWidget(message)
        #self.layout.addWidget(self.buttonBox)
        self.layout.addWidget(self.botonA)
        self.layout.addWidget(self.botonB)
        self.setLayout(self.layout)

    def Vamonos(self):
        self.result=10
        QDialog.done(self,10)

    def Vamonos2(self):
        self.result=20
        QDialog.done(self,20)

    def GetValue(self):
        return self.result


class MyCustomWid(QWidget):
    def __init__(self, label, imagePath, indexe=-1, pixmapTBP=None, parent=None):
        super(MyCustomWid, self).__init__(parent)
        horizontalLayout = QHBoxLayout()
        self.imagePath = imagePath
        self.captLbl = label
        self.index = indexe
        self.captLbl = QLabel(self.captLbl)
        horizontalLayout.addWidget(self.captLbl)
        #horizontalLayout.addWidget(QPushButton("X"))
        self.imageLbl = QLabel()
        if pixmapTBP is None: 
        	pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(self.imagePath))
        else:
        	pixmap = pixmapTBP
        self.imageLbl.setPixmap(pixmap.scaled(QtCore.QSize(350,100)))
        horizontalLayout.addWidget(self.imageLbl)
        self.setLayout(horizontalLayout)

    def getIndex(self):
        return self.index


    def getPixmap(self):
        return self.imageLbl.pixmap()

    def getImagePath(self):
        return self.imagePath

    def getText(self):
        return self.captLbl.text()

class MyList(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        imagePath = "moon.png"
        imagePath2 = "Zorro.png"


        self.currentItem =QListWidgetItem()
#        label = MyCustomWid("Blaa", imagePath)
#        label2 = MyCustomWid("Blaa", imagePath2)
#        item = QListWidgetItem()
#        item2 = QListWidgetItem()
#        item.setSizeHint(QtCore.QSize(200,110))
#        item2.setSizeHint(QtCore.QSize(200,110))

#        self.addItem(item)
#        self.addItem(item2)
#        self.setItemWidget(item,label)
#        self.setItemWidget(item2,label2)
        self.setIconSize(QtCore.QSize(300,350))
        self.setSelectionMode(1)            # 1 = SingleSelection, 2 = MultiSelection, not necessary, default mode is singleSelection
        self.setGeometry(200,200,300,500)
        self.itemClicked.connect(self.findSel)

    def agregar(self,texto="Bla",pixmap=None,index=-1):
        imagePath = "Moon.png"
        label = MyCustomWid(texto, imagePath,pixmapTBP=pixmap,indexe=index)
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(100,110))
        self.addItem(item)
        self.setItemWidget(item,label)



    def findSel(self, current):
        self.currentItem = self.itemWidget(current)
        pixmap = self.currentItem.getPixmap()
        imagePath = self.currentItem.getImagePath()
        lblTxt = self.currentItem.getText()
        print (pixmap, imagePath, lblTxt)
        # self.labelBigImageDisplay(current.pixmap())

class MyWindow(QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 1400, 800)
        self.setWindowTitle("Generador de Mosaicos de Imágenes para Papelerías")

        #self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        #self.image = Gtk.Image.new_from_icon_name("process-stop", Gtk.IconSize.MENU)

        self.msgSc = QShortcut(QKeySequence('Ctrl+V'), self)
        self.msgSc.activated.connect(self.paste_image)
        self.Contador=0
        self.IndiceActual=0
        self.lista=[]

        #layout = QVBoxLayout()
        self.textLbl = MyList()
        #layout.addWidget(textLbl)
        #self.setLayout(layout)
        self.textLbl.itemClicked.connect(self.clickearElemento)

        self.tempButton = QPushButton("Generar PDF")
        self.tempButton.clicked.connect(self.agregarElemento)		

        self.tempButton2 = QPushButton("Borrar Todo")
        self.tempButton2.clicked.connect(self.borrarTodoAlaChing)		


        mainLayout = QHBoxLayout()
        #mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.textLbl)
        #mainLayout.addWidget(self.tempButton)
        mainLayout2 = QVBoxLayout()

        # loading image
        #self.pixmap = QPixmap('moon.png')
        self.pixmap = QPixmap()  
        # adding image to label
        # creating label
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setFixedSize(QSize(600,800))
        mainLayout.addWidget(self.label)

        self.listView = QListView()
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setObjectName("listView-1")	
        self.listView.clicked[QModelIndex].connect(self.on_clicked_lista_modos)

        values = [str(AcomodoImagenes.obtener_dimensiones_matriz(0)[0])]
        #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
        for i in values:
        	self.model.appendRow(QStandardItem(i))

        self.textLbl.setFixedSize(QSize(600,800))
        mainLayout2.addWidget(self.tempButton)
        mainLayout2.addWidget(self.tempButton2)
        self.labelInfo = QLabel("Imagenes : "+str(self.Contador))
        self.labelInfo2 = QLabel("IndiceActual : "+str(self.IndiceActual))
        mainLayout2.addWidget(self.labelInfo)
        mainLayout2.addWidget(self.labelInfo2)


        self.AgregarPaginaBlanco = QPushButton("Agregar Pagina en Blanco")
        mainLayout2.addWidget(self.AgregarPaginaBlanco)
        self.AgregarPaginaBlanco.clicked.connect(self.agregaImagenBlancaALista)


        self.AgregarBlanco = QPushButton("Agregar Imagen en Blanco")
        mainLayout2.addWidget(self.AgregarBlanco)
        self.AgregarBlanco.clicked.connect(self.agregaImagenBlancaALista)


        self.BorrarUltimo = QPushButton("Borrar Ultima Agregada")
        mainLayout2.addWidget(self.BorrarUltimo)
        self.BorrarUltimo.clicked.connect(self.borrarTodoAlaChing_Menos_El_Ultimo)
        
        mainLayout2.addWidget(self.listView)
        
        mainLayout2.addWidget(QPushButton("T0"))
        mainLayout2.addWidget(QPushButton("T1"))
        mainLayout2.addWidget(QPushButton("T2"))
        mainLayout.addLayout(mainLayout2)
        self.setLayout(mainLayout)

    def on_clicked_lista_modos(self, index):
        #item = self.model.itemFromIndex(index)
        #print (item.text())
        self.IndiceActual=index.row() # Agregar una imagen nueva -> Por defecto configuración 0
        self.labelInfo.setText("Imagenes : "+str(self.Contador))
        self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))


    def clickearElemento(self):
        dlg = CustomDialog()
        if dlg.exec():
        	value = dlg.GetValue()
        	print(value)

        if value==10:
        	#print("Success!")
        	print ("ELIMINAR", self.textLbl.currentItem.getText(),self.textLbl.currentItem.getIndex())
        if value==20:
#        	print("Success!")
        	print ("DUPLICAR", self.textLbl.currentItem.getText(),self.textLbl.currentItem.getIndex())
        	
        #else:
        #	print("Cancel!")

        #print ("Valer madre", self.textLbl.currentItem.getText(),self.textLbl.currentItem.getIndex())
        #self.textLbl.currentItem.getPixmap()
        self.label.setPixmap(self.textLbl.currentItem.getPixmap())
        self.label.setFixedSize(QSize(600,800))
        
    def borrarTodoAlaChing_Menos_El_Ultimo(self):
        if len (self.lista) > 0:
            print ("Pinche PUTO")
            self.textLbl.clear()
            self.lista.pop()
            self.Contador=0
            for i in self.lista:
                self.Contador+=1
                print (i)
                pil_image= Image.open(i)
                #print (pil_image)


                newsize = (150, 150)
                pil_image = pil_image.resize(newsize)

                pixmap = ImageQt.toqpixmap(pil_image)

                self.textLbl.agregar(texto="Imagen"+str(self.Contador),pixmap=pixmap)
                self.IndiceActual=0 # Agregar una imagen nueva -> Por defecto configuración 0
                self.labelInfo.setText("Imagenes : "+str(self.Contador))
                self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))

                self.model.clear()
                #values = [str(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))]
                values = AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))
                #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
                for i in values:
                    #self.model.appendRow(QStandardItem(i))
                    self.model.appendRow(QStandardItem(str(i)))
                    

 
            #self.lista.append(i)
    def ValerVerga (self):
#self.lista.append("Temporal/ZZ_Temporal"+str(self.Contador)+".png")




        #print (self.lista)
#        def resto_paste_imageX(self):

        #self.model.clear()
            #values = [str(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))]
        #values = AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))
            #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
        #for i in values:
                #self.model.appendRow(QStandardItem(i))
        #    self.model.appendRow(QStandardItem(str(i)))


        xx=0        
        

    def borrarTodoAlaChing(self):
        self.Contador=0
        self.IndiceActual=0
        self.lista=[]
        self.labelInfo.setText("Imagenes : "+str(self.Contador))
        self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))

        self.textLbl.clear()


        im = Image.new('RGB', (600, 800), color = (255,0,0))
        #pixmap = ImageQt.toqpixmap(img)      
        #self.label.setPixmap(pixmap)
        #self.label.setFixedSize(QSize(600,800))
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "BGRA")
        qim = QtGui.QImage(data, im.width, im.height, QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        #qim = ImageQt(im)
        #pix = QtGui.QPixmap.fromImage(qim)
        self.label.setPixmap(pixmap)
        #self.label.setFixedSize(QSize(600,800))

        self.model.clear()
        values = [str(AcomodoImagenes.obtener_dimensiones_matriz(0)[0])]
        #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
        for i in values:
        	self.model.appendRow(QStandardItem(i))

#        self.tempButton.setEnabled (False)



    def agregarElemento(self):
        self.tempButton.setEnabled (False)
        #self.textLbl.agregar()
        #A = AcomodoImagenes(self.lista,r'temporal.png',4,(2,2))
        A = AcomodoImagenes(self.lista,r'temporal.png',len(self.lista),AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))[self.IndiceActual])
        Imagen = A.GenerarImagen()  
		#pil_image = pil_image.resize(newsize)
        newsize = (600, 800)
        Imagen = Imagen.resize(newsize)
        pixmap = ImageQt.toqpixmap(Imagen)      
        self.label.setPixmap(pixmap)
        #self.label.setFixedSize(QSize(600,800))
        self.tempButton.setEnabled (True)

        
    def agregaImagenBlancaALista (self):
        print ("Agregar una imagen en blanco")
        I = Image.new('RGB', (500, 500), color = (255,255,255))
        self.AgregarImagenALista(I)

    def paste_image(self):
        #image = self.clipboard.wait_for_image()
        img = ImageGrab.grabclipboard()
        #print(img)
        # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=200x71 at 0x105E68700>

        if isinstance(img, Image.Image):
            self.AgregarImagenALista(img)
            
    def Fake (self):
        if True:
            
            # True
            print("Resolucion",img.size)
            # (200, 71)
            self.Contador+=1
            pil_image = img
            pil_image.save("Temporal/ZZ_Temporal"+str(self.Contador)+".png")
            self.lista.append("Temporal/ZZ_Temporal"+str(self.Contador)+".png")

            newsize = (150, 150)
            pil_image = pil_image.resize(newsize)

            pixmap = ImageQt.toqpixmap(pil_image)


            self.textLbl.agregar(texto="Imagen"+str(self.Contador),pixmap=pixmap)
            self.IndiceActual=0 # Agregar una imagen nueva -> Por defecto configuración 0
            self.labelInfo.setText("Imagenes : "+str(self.Contador))
            self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))
            print (self.lista)
#        def resto_paste_imageX(self):

            self.model.clear()
            #values = [str(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))]
            values = AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))
            #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
            for i in values:
                #self.model.appendRow(QStandardItem(i))
                self.model.appendRow(QStandardItem(str(i)))
    def AgregarImagenALista(self, img):
        if True:
            
            # True
            print("Resolucion",img.size)
            # (200, 71)
            self.Contador+=1
            pil_image = img
            pil_image.save("Temporal/ZZ_Temporal"+str(self.Contador)+".png")
            self.lista.append("Temporal/ZZ_Temporal"+str(self.Contador)+".png")

            newsize = (150, 150)
            pil_image = pil_image.resize(newsize)

            pixmap = ImageQt.toqpixmap(pil_image)


            self.textLbl.agregar(texto="Imagen"+str(self.Contador),pixmap=pixmap,index=self.Contador-1)
            self.IndiceActual=0 # Agregar una imagen nueva -> Por defecto configuración 0
            self.labelInfo.setText("Imagenes : "+str(self.Contador))
            self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))
            print (self.lista)
#        def resto_paste_imageX(self):

            self.model.clear()
            #values = [str(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))]
            values = AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))
            #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
            for i in values:
                #self.model.appendRow(QStandardItem(i))
                self.model.appendRow(QStandardItem(str(i)))

    def resto_paste_image(self):
        if image is not None:
            self.Contador+=1
            print ("Resoulcion de imagen copiada: [",image.get_height(),",",image.get_width(),"]")
            print ("Conteo de Imagenes: ",self.Contador)
            #print (image.get_width())
            #print (image.get_height())            			            			
            self.image.set_from_pixbuf(image)
            print (type(self.image),"Resoulcion de imagen copiada: [",image.get_height(),",",image.get_width(),"]")
            pil_image = self.pixbuf2image(image)
            pil_image.save("/home/marco/ZZ_Temporal"+str(self.Contador)+".png")
            self.lista.append("/home/marco/ZZ_Temporal"+str(self.Contador)+".png")

            newsize = (300, 300)
            pil_image = pil_image.resize(newsize)

            pixmap = ImageQt.toqpixmap(pil_image)
            self.textLbl.agregar(texto="Imagen"+str(self.Contador),pixmap=pixmap)

            #print ("Tamaño en Pixeles de una Hoja tamaño letter ",letter)
            #w, h = letter
            #c = canvas.Canvas("image.pdf", pagesize=letter)
            # Place the logo in the upper left corner.
            #img = ImageReader("/home/marco/XNO.png")
            #img2 = ImageReader("/home/marco/oWa67.png")
            # Get the width and height of the image.
            #img_w, img_h = img.getSize()
            # h - img_h is the height of the sheet minus the height
            # of the image.
            #c.drawImage(img, 0, h - img_h)
            #c.drawImage(img2, 0, 0)
            #c.save()

            self.IndiceActual=0 # Agregar una imagen nueva -> Por defecto configuración 0
            self.labelInfo.setText("Imagenes : "+str(self.Contador))
            self.labelInfo2.setText("IndiceActual : "+str(self.IndiceActual))
            print (self.lista)

            self.model.clear()
            #values = [str(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))]
            values = AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista))
            #print(AcomodoImagenes.obtener_dimensiones_matriz(len(self.lista)))
            for i in values:
            	#self.model.appendRow(QStandardItem(i))
            	self.model.appendRow(QStandardItem(str(i)))

    def pixbuf2image(self,pix):
        """Convert gdkpixbuf to PIL image"""
        data = pix.get_pixels()
        w = pix.props.width
        h = pix.props.height
        stride = pix.props.rowstride
        mode = "RGB"
        if pix.props.has_alpha == True:
            mode = "RGBA"
        im = PILImage.frombytes(mode, (w, h), data, "raw", mode, stride)
        return im

if __name__ == '__main__':
    app=QApplication(sys.argv)
    new=MyWindow()
    new.show()
    app.exec_()

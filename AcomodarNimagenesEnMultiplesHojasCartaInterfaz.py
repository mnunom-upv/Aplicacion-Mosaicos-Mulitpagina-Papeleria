# Python program to explain cv2.line() method 

import numpy as np
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
import img2pdf
import io
from PyPDF2 import PdfMerger

   
# importing cv2 
#import cv2 

#print ("Kguama1")


class AcomodoImagenes :
	@staticmethod
	def obtener_dimensiones_matriz(argument):
		# Genera los acomodos donde el espacio desperdiciado sea el menor posible 
		switcher = {
		    0: [(0,0)],
		    1: [(1,1)],
		    2: [(2,1),(1,2)],
			3: [(3,1),(1,3)],
		    4: [(2,2),(1,4),(4,1)],
	        5: [(3,2),(2,3),(1,5),(5,1)],
		    6: [(3,2),(2,3),(1,6),(6,1)],
		    7: [(4,2),(3,3),(2,4),(1,7),(7,1)],
		    8: [(2,4),(4,2),(1,8),(8,1)],
		    9: [(3,3),(5,2),(2,5),(1,9),(9,1)],
		    10: [(2,5),(5,2),(4,3),(3,4),(1,10),(10,1)],
		    11: [(4,3),(3,4)],
		    12: [(4,3),(3,4)],
		    13: [(7,2),(2,7)],
		    14: [(7,2),(2,7)],
		    15: [(5,3),(3,5)],
		    16: [(4,4)],
		    17: [(6,3),(3,6),(9,2),(2,9)],
		    18: [(6,3),(3,6),(9,2),(2,9)],
		    19: [(5,4),(4,5)],
		    20: [(5,4),(4,5)],
		    21: [(7,3),(3,7)]
		}
	 
		# get() method of dictionary data type returns
		# value of passed argument if it is present
		# in dictionary otherwise second argument will
		# be assigned as default value of passed argument
		return switcher.get(argument, "nothing")

	def __init__(self, ListaImagenes = [], rutaImagenSalida= r'collage.png',ImagenesAAcomodar=1,organizacion=(1,1)):
		self.listaImagenes = ListaImagenes
		self.path=rutaImagenSalida
		self.ImagenesAAcomodar=ImagenesAAcomodar
		self.organizacion = organizacion

		self.window_name = 'Image'
#		self.ImagenResultadoFilas=792*2  #72 dpi
#		self.ImagenResultadoColumnas=612*2

		self.ImagenResultadoFilas=2197  #200 dpi
		self.ImagenResultadoColumnas=1701


	def GenerarImagen (self):
		print ("Archivo de Imagen de Salida: ",self.path)
		for i in self.listaImagenes:
			print ("\t",i)		

		#self.ImagenesAAcomodar=10
		self.indice_image=0
		self.collage = Image.new("RGBA", (self.ImagenResultadoColumnas,self.ImagenResultadoFilas), color=(255,255,255,255))
		print ("Valer V")

		#print (obtener_dimensiones_matriz(ImagenesAAcomodar))
		#Filas=self.obtener_dimensiones_matriz(ImagenesAAcomodar)[0]
		#Columnas=self.obtener_dimensiones_matriz(ImagenesAAcomodar)[1]
		Filas=self.organizacion[0]
		Columnas=self.organizacion[1]

		IncrementoY=int(self.ImagenResultadoFilas/Filas)
		IncrementoX=int(self.ImagenResultadoColumnas/Columnas)

		print ("Resulucion de cada cacho (Filas,Columnas)",IncrementoY,IncrementoX)

		FijarResolucionPorAltura=True


		print ("Dimensiones:",Filas,Columnas)
		filaInicio=0
		for i in range (0,Filas):
			columnaInicio=0
			for j in range (0,Columnas):
				#indice_image+=1
				if (self.indice_image < self.ImagenesAAcomodar):

					print ("procesando",self.indice_image)			
					file = self.listaImagenes[self.indice_image]
					photo = Image.open(file).convert("RGBA")
					width, height = photo.size
					print ("Dimensiones Originales",width, height)
					print (i,j)
					if (width>height): #Rotar a Fuerza
						# Checar dimensiones del cacho
						if (IncrementoX>IncrementoY):
							print (" Imagen Ancha en Porcion Ancha")
							FijarResolucionPorAltura=True		
						else:
							# Rotar
							print (" Rotando Imagen Ancha para hacerla Alta")
							photo  = photo.transpose(Image.ROTATE_90)
							#FijarResolucionPorAltura=False		
							if Filas>Columnas:
								FijarResolucionPorAltura=False
							else:
								FijarResolucionPorAltura=True		
					else:
						if (IncrementoY<IncrementoX): 
							print (" Rotando Imagen Alta para hacerla Ancha")
							photo  = photo.transpose(Image.ROTATE_90)		
							if Filas>Columnas:
								FijarResolucionPorAltura=True
							else:
								FijarResolucionPorAltura=False		
						else:
							print (" Imagen Alta en Porcion Alta")
							FijarResolucionPorAltura=True		


					width, height = photo.size
					print ("Rotada - diemsiones postrotacion ",width, height)

				#else:
				#if (vertical_horizontal==0):
					print ("vertical")
					
					print (filaInicio,columnaInicio)
					start_point = (columnaInicio, 0)
					#end_point = (columnaInicio, image.shape[0])
					print (start_point)
					#print (end_point)
					color = (255, 0, 0)
					thickness = 9
					#image = cv2.line(image, start_point, end_point, color, thickness)

					width, height = photo.size
					ratio = width / height
					print ("ratio",ratio)

					if FijarResolucionPorAltura:
						print ("Fijando Altura")
						filas_temporal =IncrementoY
						while (True):
							new_height = filas_temporal
							new_width = int(ratio * new_height)
							print ("Dimensiones Nuevas h,w",new_height,new_width,IncrementoY,IncrementoX)
							filas_temporal-=10
							if (new_width<IncrementoX) and (new_height<IncrementoY):
								break
						print ("Dimensiones Nuevas h,w",new_height,new_width,IncrementoY,IncrementoX)
						resized_im = photo.resize((new_width, new_height))
					else:
						columnas_temporal =IncrementoX
						while (True):
							new_width = columnas_temporal
							new_height = int(ratio * new_width)
							print ("Dimensiones Nuevas h,w",new_height,new_width,IncrementoY,IncrementoX)
							columnas_temporal-=10
							if (new_width<IncrementoX) and (new_height<IncrementoY):
								break
						print ("Dimensiones Nuevas h,w",new_height,new_width,IncrementoY,IncrementoX)				
						resized_im = photo.resize((new_height,new_width))
					#Save the cropped image
					resized_im.save('resizedimage.png')
					self.collage.paste(resized_im, (columnaInicio,filaInicio))
					columnaInicio+=IncrementoX
					#else:
					#	print ("horizontal")
				self.indice_image+=1

			start_point = (0, filaInicio)
			#end_point = (image.shape[1], filaInicio)
			print (start_point)
			#print (end_point)
			color = (0, 0, 255)
			thickness = 9
			#image = cv2.line(image, start_point, end_point, color, thickness)


			filaInicio+=IncrementoY

	
 
		#self.collage.show() 

		#self.collageF = self.collage.convert('RGB')
		self.collageF = self.remove_transparency(self.collage)
		
		#self.collageF.save("zzzPDf.pdf")


		a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
		letterinpt = (img2pdf.mm_to_pt(216),img2pdf.mm_to_pt(279))
		layout_fun = img2pdf.get_layout_fun(letterinpt)
		bytes_io = io.BytesIO()
		self.collageF.save(bytes_io, 'PNG')

		with open("zzzPDf2.pdf","wb") as f:
			f.write(img2pdf.convert(bytes_io.getvalue(), layout_fun=layout_fun))

		return self.collageF


	def remove_transparency(self,im, bg_colour=(255, 255, 255)):

		# Only process if image has transparency (http://stackoverflow.com/a/1963146)
		if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

		    # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
		    alpha = im.convert('RGBA').split()[-1]

		    # Create a new background image of our matt color.
		    # Must be RGBA because paste requires both images have the same format
		    # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
		    bg = Image.new("RGBA", im.size, bg_colour + (255,))
		    bg.paste(im, mask=alpha)
		    return bg

		else:
		    return im


MacroLista = [
[
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
],
[
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
]
]
Configuraciones = [[4,(2,2)],
                   [6,(3,2)]]

letterinpt = (img2pdf.mm_to_pt(216),img2pdf.mm_to_pt(279))
layout_fun = img2pdf.get_layout_fun(letterinpt)

# FASE 0: Generar las imagenes de manera separada
i=0
merger = PdfMerger()
for L in MacroLista :
        print ("Procesando Lista",i,Configuraciones[i])
        #print (L)
        A = AcomodoImagenes(L,'Imagen'+str(i)+'.png',Configuraciones[i][0],Configuraciones[i][1])
        Collage1 = A.GenerarImagen()
        bytes_io = io.BytesIO()
        Collage1.save(bytes_io, 'PNG')
        # Se guarda cada pagina como una imagen para efecto de previsualizar
        Collage1.save('Imagen'+str(i)+'.png')   

        with open('Resultado'+str(i)+'.pdf','wb') as f:
                f.write(img2pdf.convert(bytes_io.getvalue(), layout_fun=layout_fun))
        merger.append('Resultado'+str(i)+'.pdf')
                
        i+=1
# FASE 1: Pegar las imagenes en un PDF
merger.write("ZZZZ_SalidasPegadas.pdf")
merger.close()        
exit()


listaArchivosR=[
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png",
"Moon.png"
]


print ("Kguama")





B = AcomodoImagenes(listaArchivosR,r'temporal2.png',6,(3,2))
Collage2 = B.GenerarImagen()
bytes_io2 = io.BytesIO()
Collage2.save(bytes_io2, 'PNG')

with open("ResultadoA.pdf","wb") as f:
	f.write(img2pdf.convert(bytes_io.getvalue(), layout_fun=layout_fun))

with open("ResultadoB.pdf","wb") as f:
	f.write(img2pdf.convert(bytes_io2.getvalue(), layout_fun=layout_fun))


merger.append('ResultadoA.pdf')
merger.append('ResultadoB.pdf')

#Write out the merged PDF file
merger.write("ZZZZ_SalidasPegadas.pdf")
merger.close()
	#f.append(img2pdf.convert(bytes_io2.getvalue(), layout_fun=layout_fun))

#AcomodoImagenes.obtener_dimensiones_matriz(10)
#AcomodoImagenes.obtener_dimensiones_matriz = staticmethod(AcomodoImagenes.obtener_dimensiones_matriz)
#print(AcomodoImagenes.obtener_dimensiones_matriz(10))


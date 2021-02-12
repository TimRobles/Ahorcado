from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtGui import *
import sys, os

rutaBase=os.getcwd()

factorEspacio=24
versiculos=[]
imagenes=[]
imagenes.append("Imagen1")
# imagenes.append("Imagen2")
# imagenes.append("Imagen3")
imagenes.append("Imagen4")
imagenes.append("Imagen5")
imagenes.append("Imagen6")
imagenes.append("Imagen7")
imagenes.append("Imagen8")
imagenes.append("Imagen9")
archivo=open(r"versiculos.txt")
v=True
fila=[]
for linea in archivo.readlines():
    fila.append(linea)
    if v:
        v=False
    else:
        versiculos.append(fila)
        fila=[]
        v=True

abecedario=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
maximoError=5

def verImagen(lbl, imagen):
    image = QImage()
    image.load(r"%s/%s" % (rutaBase, imagen))
    lbl.setPixmap(QPixmap(image))

def buscarEspacios(texto):
    espacios=[]
    aumentar={}
    contador=0
    desfase=0
    anterior=0
    filas=1
    for letra in texto:
        if letra==" ":
            if contador+desfase>factorEspacio*filas:
                aumento=factorEspacio*filas-anterior-desfase
                aumentar[anterior]=aumento
                desfase+=aumento
                filas+=1
            anterior=contador
            espacios.append(contador)
        contador+=1
    if contador+desfase>factorEspacio*filas:
        aumento=factorEspacio*filas-anterior-desfase
        aumentar[anterior]=aumento
        desfase+=aumento
        filas+=1
    print(espacios, aumentar)
    return aumentar


def verLetras(texto):
    letras=[]
    for letra in texto:
        if not letra in abecedario:
            continue
        if not letra in letras:
            letras.append(letra)
    letras.sort()
    return letras

def verificarLetras(totalLetras, letras):
    contador=len(totalLetras)
    for letra in letras:
        if letra in totalLetras: contador-=1

    if contador==0:
        return True
    return False

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Ahorcado.ui",self)
        self.numero=-1
        self.letras=[]
        self.letrasMostrar=[]
        self.errores=0
        self.frase=""
        self.totalLetras=""

        self.btnIngresar.clicked.connect(self.ingresarLetra)
        self.btnSiguiente.clicked.connect(self.iniciar)

        self.iniciar()

    def iniciar(self):
        if self.numero+1==len(versiculos):
            QMessageBox.information(self, "Fin del juego", "Hasta el próximo aniversario", QMessageBox.Ok)
            return
        self.lblLetras.setText("")
        self.numero+=1
        self.errores=0
        self.letras=[]
        self.letrasMostrar=[]
        self.frase=versiculos[self.numero][0].upper()
        self.frase=self.frase.replace("Á", "A")
        self.frase=self.frase.replace("É", "E")
        self.frase=self.frase.replace("Í", "I")
        self.frase=self.frase.replace("Ó", "O")
        self.frase=self.frase.replace("Ú", "U")
        self.totalLetras=verLetras(self.frase)
        self.mostrar(self.frase, verificarLetras(self.totalLetras, self.letras), versiculos[self.numero][1])
        self.btnSiguiente.setEnabled(False)

    def mostrar(self, texto, fin, ubicacion):
        textoMostrar=[]
        aumentar=buscarEspacios(texto)
        contador=0
        for letra in texto:
            if contador in aumentar:
                for i in range(aumentar[contador]):
                    textoMostrar.append(" ")
            if not letra in abecedario:
                textoMostrar.append(letra)
            elif letra in self.letras:
                textoMostrar.append(letra)
            else:
                textoMostrar.append("_")
            contador+=1
        if fin:
            self.lblTexto.setText("%s\n%s" % (" ".join(textoMostrar), ubicacion))
        else:
            self.lblTexto.setText(" ".join(textoMostrar))

        if self.errores>maximoError:
            verImagen(self.lblImagen, imagenes[-1])
        else:
            verImagen(self.lblImagen, imagenes[self.errores])
            # self.lblImagen.setText("Errores: " + str(self.errores))

    def ingresarLetra(self):
        if self.btnSiguiente.isEnabled():
            self.iniciar()
            return

        letra=self.leLetra.text().upper()
        self.leLetra.setText("")
        if not letra in abecedario: return
        if letra in self.letras:
            QMessageBox.information(self, "¡Ups!", "La letra %s ya existe" % letra, QMessageBox.Ok)
            return
        if letra in self.totalLetras:
            self.letrasMostrar.append(letra)
        else:
            self.letrasMostrar.append("(%s)" % letra)
            self.errores+=1
        if self.errores==maximoError: QMessageBox.information(self, "¡Ups!", "¡Ups!", QMessageBox.Ok)
        self.letras.append(letra)
        self.letrasMostrar.sort()
        self.lblLetras.setText(", ".join(self.letrasMostrar))

        self.mostrar(self.frase, verificarLetras(self.totalLetras, self.letras), versiculos[self.numero][1])

        if verificarLetras(self.totalLetras, self.letras):
            QMessageBox.information(self, "Felicidades", "Versículo completado", QMessageBox.Ok)
            self.btnSiguiente.setEnabled(True)


app=QApplication(sys.argv)
_main=Principal()
_main.show()
app.exec_()

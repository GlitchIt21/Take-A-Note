from PyQt5.QtWidgets import *
import sys
import os

class VentanaPrincipal(QMainWindow):

    #esta funcion se encarga de guardar el archivo si este no existe (hay que agregar ".txt" al final del nombre, sino el documento 
    # no se guardará correctamente)

    def guardarArchivoComo(self, e):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        archivo, _ = QFileDialog.getSaveFileName(self, 'Guardar', 'C:\\', 'Text files (*.txt)', options = options)

        with open(archivo, 'wt') as f:
            f.write(self.campoDeTexto.toPlainText())

    
    #esta funcion se encarga de guardar el archivo ya existente

    def guardarArchivo(self, e):
        archivoGuardado = self.archivo
        if( os.path.exists(archivoGuardado[0]) == True):
            with open(archivoGuardado[0], 'wt') as f:
                f.write(self.campoDeTexto.toPlainText())

    #esta función hace que el botón "Guardar" solo se active cuando sea un archivo que ya existe

    def botonGuardar_changed(self):
        if (self.existe == 1):
            self.botonGuardar.setEnabled(True)
        else:
            self.botonGuardar.setEnabled(False)

    #esta funcion limpia lo que está escrito (hay que apretarla dos veces)
    def nuevo(self, e):
        self.campoDeTexto.setText("")
        if(self.campoDeTexto != ""):
            self.botonGuardar.setEnabled(False)
            self.existe = self.existe - 1

    #esta funcion se encarga de abrir un archivo que ya existe 

    def abrir_archivos(self, e):
        self.archivo = QFileDialog.getOpenFileName(self, 'Abrir un documento existente', 'C:\\', "Text files (*.txt)")
        if self.archivo[0]:
            with open(self.archivo[0], 'rt') as f:
                datos = f.read()
                self.campoDeTexto.setText(datos)
        
        self.existe = self.existe + 1

    #esta función se encarga de cerrar el programa correctamente 

    def salir(self, e):

        sys.exit(0)

    def __init__(self):

    #Medidas de la ventana

        super().__init__()
        self.nombre_archivo = "Sin título"
        self.nombre_programa = "Take A Note"
        self.setWindowTitle(self.nombre_programa + ": " + self.nombre_archivo)
        self.posX = 400
        self.posY = 150
        self.ancho = 600
        self.alto = 450
        self.setGeometry(self.posX, self.posY, self.ancho, self.alto)

        containerPrincipal = QVBoxLayout()

    #Menú interactivo

        menu = QHBoxLayout()
        notaNueva = QPushButton()
        notaAbrir = QPushButton()
        self.botonGuardar = QPushButton()
        notaGuardarComo = QPushButton()
        botonSalir = QPushButton()

        notaNueva.setText('Nuevo documento')
        notaAbrir.setText('Abrir un documento existente')
        self.botonGuardar.setText('Guardar')
        notaGuardarComo.setText('Guardar como...')
        botonSalir.setText('Salir')

        notaNueva.clicked.connect(self.nuevo)
        notaAbrir.clicked.connect(self.abrir_archivos)
        self.botonGuardar.clicked.connect(self.guardarArchivo)
        self.botonGuardar.setEnabled(False)
        notaGuardarComo.clicked.connect(self.guardarArchivoComo)
        botonSalir.clicked.connect(self.salir)
        
        menu.addWidget(notaNueva)
        menu.addWidget(notaAbrir)
        menu.addWidget(self.botonGuardar)
        menu.addWidget(notaGuardarComo)
        menu.addWidget(botonSalir)

        self.existe = 0

    #Campo de texto

        container = QHBoxLayout()

        self.campoDeTexto = QTextEdit()
        self.campoDeTexto.textChanged.connect(self.botonGuardar_changed)
        #self.campoDeTexto.textChanged.connect(self.guardarArchComo_changed)
        self.campoDeTexto.setPlaceholderText('¡Empieza por escribir algo!')
        container.addWidget(self.campoDeTexto)

        containerPrincipal.addLayout(menu)
        containerPrincipal.addLayout(container)
        widget = QWidget()
        widget.setLayout(containerPrincipal)
        self.setCentralWidget(widget)

    #barra de estado

        self.statusBar().showMessage('esta es mi barra de estado')



if __name__ == '__main__' :
    blocDeNotas = QApplication(sys.argv)
    ventanaEmergente = VentanaPrincipal()
    ventanaEmergente.show()
    finalizacion = blocDeNotas.exec_()
    sys.exit(finalizacion)
from PyQt5.QtWidgets import *
import sys
import os

class VentanaPrincipal(QMainWindow):

    #esta funcion se encarga de guardar el archivo si este no existe (hay que agregar ".txt" al final del nombre, sino el documento 
    # no se guardará correctamente)

    def guardarArchivoComo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        msg = QMessageBox()
        msg.setWindowTitle('¡Importante!')
        msg.setText('Recuerda colocar ".txt" al final del nombre de tu archivo para que este se guarde correctamente')
        msg.setIcon(QMessageBox.Information)
        msg.addButton(QMessageBox.Ok)

        archivo, _ = QFileDialog.getSaveFileName(self, 'Guardar', 'C:\\', 'Documentos de texto (*.txt)', options = options)

        with open(archivo, 'wt') as f:
            f.write(self.campoDeTexto.toPlainText())
            self.existe = self.existe + 1
            nombre = archivo.format(__name__)
            self.setWindowTitle(self.nombre_programa + ': ' + nombre)
            
    #esta funcion se encarga de guardar el archivo ya existente (sobreescribe el texto del documento con el nuevo texto 
    # dentro del campo de texto)

    def guardarArchivo(self):
        archivoGuardado = self.archivo
        if( os.path.exists(archivoGuardado[0]) == True):
            with open(archivoGuardado[0], 'wt') as f:
                f.write(self.campoDeTexto.toPlainText())

        msg = QMessageBox()
        msg.setWindowTitle('Guardar')
        msg.setText('Los cambios se han guardado correctamente.')
        msg.setIcon(QMessageBox.Information)
        msg.addButton(QMessageBox.Ok)
        msg.exec_()

    #esta función hace que el botón "Guardar" solo se active cuando se esté escribiendo en un documento existente 

    def botonGuardar_changed(self):
        if (self.existe == 1):
            self.botonGuardar.setEnabled(True)
        else:
            self.botonGuardar.setEnabled(False)

    #esta funcion limpia lo que está escrito en el campo de texto

    def nuevo(self):
        self.campoDeTexto.setText("")
        if(self.campoDeTexto != ""):
            self.botonGuardar.setEnabled(False)
            self.setWindowTitle(self.nombre_programa + ": " + self.sinTitulo)
            self.existe = self.existe - 1

    #esta funcion se encarga de abrir un documento de texto

    def abrir_archivos(self):
        self.archivo = QFileDialog.getOpenFileName(self, 'Abrir un documento existente', 'C:\\', "Text files (*.txt)")
        if self.archivo[0]:
            with open(self.archivo[0], 'rt') as f:
                datos = f.read()
                self.campoDeTexto.setText(datos)
                self.existe = self.existe + 1
                nombre = self.archivo[0].format(__name__)
                self.setWindowTitle(self.nombre_programa + ': ' + nombre)
        

    #estas dos funciones se encargan de cerrar el programa correctamente. Primero se chequea si el contenido del campo de 
    #texto cambió, si cambió y se apreta el botón salir, se abrirá un dialogo para preguntarle al usuario si este ha 
    #guardado los nuevos cambios o si de no existir el archivo, crear uno nuevo para guardar el contenido.

    def text_changedSalir(self):
        self.botonSalir.clicked.connect(self.salir_ifTextChanged)

    def salir_ifTextChanged(self):
        enabled = self.botonGuardar.isEnabled()
        datos = self.campoDeTexto.toPlainText()
        warning = QMessageBox()
        warning.setWindowTitle("Salir")
        warning.setText('¡Estás por salir!')

        if(enabled == False and datos != ""):
            warning.setInformativeText('¿Deseas guardar los cambios en un documento nuevo?')
            warning.setStandardButtons(QMessageBox.Save| QMessageBox.Close)
            ret = warning.exec()

            if(ret == 2048):
                self.guardarArchivoComo()
                sys.exit(0)
            else: 
                sys.exit(0)

        elif(enabled == True and datos != ""):
            warning.setInformativeText('¿Deseas guardar los cambios?')
            warning.setStandardButtons(QMessageBox.Save| QMessageBox.Close)
            ret = warning.exec()
            if(ret == 2048):
                self.guardarArchivo()
                sys.exit(0)
            else: 
                sys.exit(0)

        else: 
            sys.exit(0)

    def salirCorrectamente(self):
        datos = self.campoDeTexto.toPlainText()
        if(datos == ""):
            sys.exit(0)
        else:
            self.text_changedSalir()

    #esta funcion devuelve un string con la cantidad de carácteres que se encuentran en el campo de texto cada vez que el texto cambia

    def contadorDeCaracteres(self):
            self.statusBar().clearMessage()
            char = self.campoDeTexto.toPlainText()
            cant_textchar = len(char)
            self.contadorDeChar.setText('Carácteres: ' + str(cant_textchar))
            self.statusBar().addWidget(self.contadorDeChar)

    #-------------------------------------- VENTANA DE LA INTERFAZ GRÁFICA --------------------------------------

    def __init__(self):

    #Medidas de la ventana

        super().__init__()
        self.sinTitulo = "Sin título"
        self.nombre_programa = "Take A Note"
        self.setWindowTitle(self.nombre_programa + ": " + self.sinTitulo)
        self.posX = 400
        self.posY = 150
        self.ancho = 600
        self.alto = 450
        self.setGeometry(self.posX, self.posY, self.ancho, self.alto)

        containerPrincipal = QVBoxLayout()

    #-------------------------------------------MENÚ INTERACTICO--------------------------------------------------

        menu = QHBoxLayout()
        notaNueva = QPushButton()
        notaAbrir = QPushButton()
        self.botonGuardar = QPushButton()
        notaGuardarComo = QPushButton()
        self.botonSalir = QPushButton()

        notaNueva.setText('Nuevo documento')
        notaAbrir.setText('Abrir un documento existente')
        self.botonGuardar.setText('Guardar')
        notaGuardarComo.setText('Guardar como...')
        self.botonSalir.setText('Salir')

        notaNueva.clicked.connect(self.nuevo)
        notaAbrir.clicked.connect(self.abrir_archivos)
        self.botonGuardar.clicked.connect(self.guardarArchivo)
        self.botonGuardar.setEnabled(False)
        notaGuardarComo.clicked.connect(self.guardarArchivoComo)
        self.botonSalir.clicked.connect(self.salirCorrectamente)

        menu.addWidget(notaNueva)
        menu.addWidget(notaAbrir)
        menu.addWidget(self.botonGuardar)
        menu.addWidget(notaGuardarComo)
        menu.addWidget(self.botonSalir)

        #una variable genérica para ayudar al correcto funcionamiento del botón Guardar Como 
        self.existe = 0

    #---------------------------------------------------CAMPO DE TEXTO -------------------------------------------------

        container = QHBoxLayout()

        self.campoDeTexto = QTextEdit()
        self.campoDeTexto.textChanged.connect(self.botonGuardar_changed)
        self.campoDeTexto.textChanged.connect(self.text_changedSalir)
        self.campoDeTexto.setPlaceholderText('¡Empieza por escribir algo!')
        container.addWidget(self.campoDeTexto)
        containerPrincipal.addLayout(menu)
        containerPrincipal.addLayout(container)
        widget = QWidget()
        widget.setLayout(containerPrincipal)
        self.setCentralWidget(widget)

    #------------------------------------------------ BARRA DE ESTADO ---------------------------------------------------
        self.estado = QStatusBar()
        self.contadorDeChar = QLabel()
        self.statusBar().showMessage('Carácteres: 0')
        self.campoDeTexto.textChanged.connect(self.contadorDeCaracteres)
        

if __name__ == '__main__' :
    blocDeNotas = QApplication(sys.argv)
    ventanaEmergente = VentanaPrincipal()
    ventanaEmergente.show()
    finalizacion = blocDeNotas.exec_()
    sys.exit(finalizacion)
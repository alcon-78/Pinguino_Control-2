import sys
import time

from pynguino.pusb import PynguinoUSB
from PySide import QtCore, QtGui
from test_ui import Ui_MainWindow

pinguino = PynguinoUSB(vboot="v4")


class TestApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.on)
        self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.off)
        self.connect(self.ui.pushPuerto, QtCore.SIGNAL("clicked()"),
            self.puerto)
        self.connect(self.ui.pushPuertoA, QtCore.SIGNAL("clicked()"),
            self.puertoA)
        self.connect(self.ui.pushManual, QtCore.SIGNAL("clicked()"),
            self.manual)
        self.connect(self.ui.pushAutomatic, QtCore.SIGNAL("clicked()"),
            self.automatic)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Esta seguro de querer cerrar la ventana", QtGui.QMessageBox.Yes,
QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def automatic(self):
        self.ui.dial_ON.setDisabled(False)
        
        self.ui.dial_OFF.setDisabled(False)
        
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_2.setDisabled(True)
        pinguino.pinMode(int(self.ui.spinPuerto.value()), "OUTPUT")
        if self.ui.esc_10_ON.isChecked():
            tiempo_ON = self.ui.dial_ON.value() * 10
        elif self.ui.esc_100_ON.isChecked():
            tiempo_ON = self.ui.dial_ON.value() * 100
        else:
            tiempo_ON = self.ui.dial_ON.value()
        if self.ui.esc_10_OFF.isChecked():
            tiempo_OFF = self.ui.dial_OFF.value() * 10
        elif self.ui.esc_100_OFF.isChecked():
            tiempo_OFF = self.ui.dial_OFF.value() * 100
        else:
            tiempo_OFF = self.ui.dial_OFF.value()
        # self.ui.lcd_ON.display(tiempo_ON)
        # self.ui.lcd_OFF.display(tiempo_OFF)
        #...........#        
        self.connect(self.ui.dial_ON, QtCore.SIGNAL('valueChanged(int)'), self.ui.lcd_ON,
            QtCore.SLOT('display(int)'))
        self.connect(self.ui.dial_OFF, QtCore.SIGNAL('valueChanged(int)'), self.ui.lcd_OFF,
            QtCore.SLOT('display(int)'))
        #...........#        
        for i in range(20):
            pinguino.digitalWrite(self.ui.spinPuerto.value(), "HIGH")
            pinguino.delay(tiempo_ON)
            pinguino.digitalWrite(self.ui.spinPuerto.value(), "LOW")
            pinguino.delay(tiempo_OFF)

    def manual(self):
        self.ui.pushButton.setDisabled(False)
        self.ui.pushButton_2.setDisabled(False)
        self.ui.dial_ON.setDisabled(True)
        self.ui.dial_OFF.setDisabled(True)

    def puerto(self):
        pinguino.pinMode(int(self.ui.spinPuerto.value()), "OUTPUT")

    def puertoA(self):
        pinguino.pinMode(self.ui.spinPuerto_A.value(), "INPUT")
        #i = 1
        #while i == 1:
        potenciometro = pinguino.analogRead(self.ui.spinPuerto_A.value())
        self.ui.lcdAnalog.display(potenciometro)
            #if self.ui.radioButton_ON.isChecked():
                #i = 1
            #else:
                #i = 0
        

    def on(self):
        pinguino.digitalWrite(self.ui.spinPuerto.value(), 1)

    def off(self):
        pinguino.digitalWrite(self.ui.spinPuerto.value(), 0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())

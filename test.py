import sys

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
        for i in range(20):
            pinguino.digitalWrite(self.ui.spinPuerto.value(), "HIGH")
            pinguino.delay(self.ui.dial_ON.value())
            pinguino.digitalWrite(self.ui.spinPuerto.value(), "LOW")
            pinguino.delay(self.ui.dial_OFF.value())

    def manual(self):
        self.ui.pushButton.setDisabled(False)
        self.ui.pushButton_2.setDisabled(False)
        self.ui.dial_ON.setDisabled(True)
        self.ui.dial_OFF.setDisabled(True)

    def puerto(self):
        pinguino.pinMode(int(self.ui.spinPuerto.value()), "OUTPUT")

    def puertoA(self):
        pinguino.pinMode(self.ui.spinPuerto_A.value(), "INPUT")
        potenciometro = pinguino.analogRead(self.ui.spinPuerto_A.value())
        self.ui.lcdAnalog.display(potenciometro)

    def on(self):
        pinguino.digitalWrite(self.ui.spinPuerto.value(), 1)

    def off(self):
        pinguino.digitalWrite(self.ui.spinPuerto.value(), 0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())

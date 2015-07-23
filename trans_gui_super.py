import qt_ui
from PyQt4 import QtGui, QtCore, uic
import sys 

if (__name__ == "__main__"):
    print dir(qt_ui)

    app = QtGui.QApplication(sys.argv)
    scr = qt_ui.AddStopIdScreen()
    scr.init()
    sys.exit(app.exec_())
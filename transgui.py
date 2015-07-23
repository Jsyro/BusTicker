#!/usr/bin/python
import sys

from PyQt4 import QtCore, QtGui, uic
from functools import partial

class addStopIdScreen(QtGui.QWidget):

    def numpad_bksp_clicked(self):
        if self.lcd_number_value < 10:
            self.lcd_number_value = 0
        else:
            self.lcd_number_value /= 10
        self.lcd_display.display(self.lcd_number_value)

    def numpad_pb_clicked(self,numpad_pb_objectName):
        if self.lcd_number_value > 100000 :
            print "only 6 digits"
            return
        pb_num = int(numpad_pb_objectName[-1:])
        self.lcd_number_value *= 10
        self.lcd_number_value += pb_num
        self.lcd_display.display(self.lcd_number_value)
  
 
    def init(self):
        self.lcd_number_value = 0
        self.screen_widget = uic.loadUi("qt_ui/addStopID.ui")
        numpad_pb_list = [self.screen_widget.findChild(QtGui.QPushButton, 'pushButton_{}'.format(id)) for id in range(0,10)] 
        numpad_bksp = self.screen_widget.findChild(QtGui.QPushButton, 'pushButton_bksp')
        numpad_bksp.clicked.connect(self.numpad_bksp_clicked)
        
        
        self.lcd_display = self.screen_widget.findChild(QtGui.QLCDNumber, 'lcdNumber')
        self.lcd_display.intValue = 0
        
        for pb in numpad_pb_list:
            name = pb.objectName()
            pb.clicked.connect(partial(self.numpad_pb_clicked, name))
        self.screen_widget.show()


if (__name__ == "__main__"):
    app = QtGui.QApplication(sys.argv)
    scr = addStopIdScreen()
    scr.init()
    sys.exit(app.exec_())
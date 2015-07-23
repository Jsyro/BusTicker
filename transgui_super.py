from qt_ui.add_stop_id import AddStopIdScreen
from PyQt4 import QtGui, QtCore, uic
import sys 



class bt_gui_manager():
    def scr_add_stop_id_CALLBACK(self, stop_id):
        self.set_stop_id.add(stop_id)
        print self.set_stop_id
        # TO-DO: make screen that asks user what    
        #        routes they want to see from that stop 
        



    def init(self):
        self.dict_screens = {}
        self.set_stop_id = set()
        self.app = QtGui.QApplication(sys.argv)
        
        self.scr_add_stop_id = AddStopIdScreen()
        self.scr_add_stop_id.init(self.scr_add_stop_id_CALLBACK)
        self.scr_add_stop_id.screen_widget.show()
        

if (__name__ == "__main__"):
    bt_gui = bt_gui_manager()
    bt_gui.init()
    
    sys.exit(bt_gui.app.exec_())
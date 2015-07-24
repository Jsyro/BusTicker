from qt_ui.add_stop_id import AddStopIdScreen
from qt_ui.select_routes_at_stop import SelectRoutesAtStop
from PyQt4 import QtGui, QtCore, uic

from transdata import transdata
import sys 



class bt_gui_manager():

    def scr_select_routes_CALLBACK(self, routes_selected):
        print routes_selected

    def scr_add_stop_id_CALLBACK(self, stop_id):
        self.set_stop_id.add(stop_id)
        self.scr_add_stop_id.screen_widget.hide()
        self.scr_select_routes = SelectRoutesAtStop()
        
        #finds what routes go by that stop
        lst_routes_at_stop = self.td.routes_at_stop_id(stop_id)
        
        #loads next screen 
        self.scr_select_routes.init(self.scr_select_routes_CALLBACK, lst_routes_at_stop)
        

    def init(self):
        #transdata.py library
        self.td = transdata()
        self.td.init()
        
        self.set_stop_id = set()
        self.app = QtGui.QApplication(sys.argv)

        #makes first screen
        self.scr_add_stop_id = AddStopIdScreen()
        #starts first screen
        self.scr_add_stop_id.init(self.scr_add_stop_id_CALLBACK)
        self.scr_add_stop_id.screen_widget.show()
        

if (__name__ == "__main__"):
    bt_gui = bt_gui_manager()
    bt_gui.init()
    sys.exit(bt_gui.app.exec_())
from qt_ui.add_stop_id import AddStopIdScreen
from qt_ui.select_routes_at_stop import SelectRoutesAtStop
from PyQt4 import QtGui, QtCore, uic

from transdata import transdata
import sys 



class bt_gui_manager():

    """ +++++++++++   SELECT ROUTES CALLBACKS   +++++++"""

    def scr_select_routes_CALLBACK_NEXT(self, set_selected):
        print set_selected

    def scr_select_routes_CALLBACK_BACK(self):
        self.scr_select_routes.screen_widget.hide()
        self.scr_add_stop_id.init(self.scr_add_stop_id_CALLBACK)
        self.scr_add_stop_id.screen_widget.show()
        
    """ ++++++++++++   ENTER STOP ID CALLBACK    ++++++++"""    
        
    def scr_add_stop_id_CALLBACK(self, stop_id):
        self.set_stop_id.add(stop_id)
        self.scr_add_stop_id.screen_widget.hide()
        self.scr_select_routes = SelectRoutesAtStop()
        
        #finds what routes go by that stop
        lst_routes_at_stop = self.td.routes_at_stop_id(stop_id)
        
        #loads next screen 
        self.scr_select_routes.init(self.scr_select_routes_CALLBACK_NEXT, self.scr_select_routes_CALLBACK_BACK, lst_routes_at_stop)
        
    """ +++++++++++++++   HOW WE START   +++++++++++++++""" 
        
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
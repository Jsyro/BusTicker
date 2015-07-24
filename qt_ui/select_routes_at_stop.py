from PyQt4 import QtGui, QtCore, uic
from functools import partial
import sys 

class SelectRoutesAtStop(QtGui.QWidget):

    def route_toggle_button_selected(self,id):
        caller = self.screen_widget.findChild(QtGui.QPushButton, "route_col_" + str(id))
        caller.setText("selected")
        print id
        
    def next_button_clicked(self):
        print "next"

    def init(self, CALLBACK, routes_lst):
        self.routes_lst = routes_lst
        self.CALLBACK = CALLBACK
        self.screen_widget = uic.loadUi("qt_ui/select_routes_at_stop.ui")
        try:
            print self.routes_lst
            scrollArea = self.screen_widget.findChild(QtGui.QScrollArea, 'scrollArea')
            #scrollArea_contents = self.screen_widget.findChild(QtGui.QWidget, 'scrollAreaWidgetContents')
            scrollArea_cols = self.screen_widget.findChild(QtGui.QHBoxLayout, 'scrollArea_layout')

            for index, route in enumerate(self.routes_lst):
                route = route.split(',')

                route_item = QtGui.QVBoxLayout()
                route_item.addWidget(QtGui.QLabel("Route ID: \n" + route[0]))
                route_item.addWidget(QtGui.QLabel("Route Long Name: \n" + route[1]))

                route_toggle_button = QtGui.QPushButton()
                route_toggle_button.setObjectName("route_col_" + str(index))
                route_toggle_button.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum) 

                route_toggle_button.clicked.connect(partial(self.route_toggle_button_selected, index))
                route_item.addWidget(route_toggle_button)
                
                scrollArea_cols.addLayout(route_item)
                
                
            if len(self.routes_lst) == 0:    
               error_box = QtGui.QHBoxLayout()
               error_box.addWidget(QtGui.QLabel("NO ROUTES AT THAT STOP"))
               scrollArea_cols.addLayout(error_box)
                
            scrollArea.setLayout(scrollArea_cols)  
            #scrollArea_contents.show()
            next_button = self.screen_widget.findChild(QtGui.QPushButton, 'pushButton_Next')
            next_button.clicked.connect(self.next_button_clicked)

            self.screen_widget.show()
        except:
           print sys.exc_info()[0] 
           sys.exit(2)
        
def close_window():
    print "closed the window"
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    scr = SelectRoutesAtStop()
    scr.init(close_window, ['16','26'])
    sys.exit(app.exec_())

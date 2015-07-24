
import os
import csv
import sqlite3 as sql



class transdb:

    def init(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
        for fName in os.listdir(os.getcwd() + "\\transdata"):
            file = open(os.getcwd() + "\\transdata\\" + fName)
            if fName[-4:] == ".txt":
                header = file.readline()
                for column_header in header.split(','):
                    if column_header.isdigit():
                        print "number - " + column_header
                    else:
                        print "string - " + column_header
                
                
if (__name__ == '__main__' ):
    tb = transdb()
    tb.init()
    
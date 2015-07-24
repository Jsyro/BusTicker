
import os
import csv
import sqlite3 as sql



class transdb:

    def init(self):
        schema_sample = []
        schema_type = []
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
        for fName in os.listdir(os.getcwd() + "\\transdata"):
            file = open(os.getcwd() + "\\transdata\\" + fName)
            schema_sample = []
            schema_type = []
            if fName[-4:] == ".txt":
                headers_lbl = file.readline().split(',')
                data_sample = file.readline().split(',')
                
                schema_sample = [(headers_lbl[i],data_sample[i]) for i in range(0,len(headers_lbl))]
                #print schema_sample
                for name, sample in schema_sample :
                    if sample.isdigit():
                        #print "number - " + name
                        schema_type.append((name,'INTEGER'))

                    else:
                        #print "string - " + name
                        schema_type.append((name,'NVARCHAR(100)'))
                
                #print schema_type        
                
            sql_create = "CREATE TABLE {}(".format(fName[:-4])
            for (name,type) in schema_type:
                sql_create += "\n\t{} {}, ".format(name, type)
                
            sql_create += " PRIMARY KEY ({} ASC)".format(schema_type[1])    
            print sql_create
if (__name__ == '__main__' ):
    tb = transdb()
    tb.init()
    
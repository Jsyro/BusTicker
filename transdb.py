
import os
import csv
import sqlite3 as sql
import re


class transdb:
    
    def init(self,db_file):
        schema_sample = []
        schema_type = []
        conn = sql.connect(os.getcwd() + "/transdata/" + db_file)
        self.cur = conn.cursor()

        p = re.compile('-?\d+(\.\d+)?')

        for fName in os.listdir(os.getcwd() + "/transdata"):
            file = open(os.getcwd() + "/transdata/" + fName)
            print "Opening " + str(fName) + "..."
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
 
                    elif p.match(sample) != None: 
                        schema_type.append((name,'FLOAT'))
                   
                    else:
                        #print "string - " + name
                        schema_type.append((name,'NVARCHAR(100)'))
                    
                    
                sql_create = "CREATE TABLE {}(".format(fName[:-4])
                for (name,type) in schema_type:
                    sql_create += "\n\t{} {}, ".format(name, type)
                
                sql_create += " PRIMARY KEY ({} ASC))".format(schema_type[0][0])  
                print sql_create
                #self.cur.execute(str(sql_create))
                print "Closing " + str(fName) + "...\n"
            else:
                print "Skipping " + str(fName) + "...\n"
            
    def clean(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        
if (__name__ == '__main__' ):
    tb = transdb()
    tb.init("bus_ticker_test.db")
    
    
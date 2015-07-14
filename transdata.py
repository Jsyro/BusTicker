import csv
import sqlite3 as sql
import sqlalchemy
import os

class transdata:

    def init(self, agency="Victoria"):
        self.agency = agency
        self.initdb()

    def get_next_bus(self, route_id, stop_id):
        print "the next " + str(route_id) + " leaves in 15 minutes"

    def initdb(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
        for fname in os.listdir("transdata"):
            (name,ext) = os.path.splitext(os.getcwd() + "\\transdata\\" + fname)
            if (ext == ".txt"):
                os.rename(name+ext, name +".csv")


    def get_routes (self, agency="Victoria"):	
        self.cur.execute("SELECT * FROM routes where agency_id = '1';") 
        self.routes = self.cur.fetchall();
        #	for route in self.routes:
        #		print route[1]

    def get_route (self, request):
        if self.routes is None:	
            print ("INITIALIZE routes... call get_routes()")
        for route in self.routes:
            routeid = route[2] 
            if routeid == request:
                return route

    def	get_trip_ids (self, route):
        print type(route)
        routetripid ={}
        self.cur.execute("SELECT * FROM trips where route_id = '" + route[1] + "';")
        sqlret = self.cur.fetchall();
        for row in sqlret:
            print type(routetripid[str(route[1])])
            #print sqlret[1][1]


td = transdata()
td.init()
td.get_routes()		
r39 = td.get_route("39")
td.get_trip_ids(r39)
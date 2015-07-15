import csv
import sqlite3 as sql
import sqlalchemy
import os

class transdata:

    def init(self, agency="1"):
        self.initdb()
        self.agency = agency
        self.agencyRoutes = {}
        self.routeTimes = {}
        self.userRoutes = []
        self.userTrips = []
        self.userStops = []

    def initdb(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
        for fname in os.listdir("transdata"):
            (name,ext) = os.path.splitext(os.getcwd() + "\\transdata\\" + fname)
            if (ext == ".txt"):
                os.rename(name+ext, name +".csv")
                
                
    """  ------  Routes  -------- """ 
    # takes number and replaces with full route_id
    
    def add_route (self, routenum):
        self.userRoutes.append(routenum)
    

    
    def print_routes(self):
        print self.userRoutes

    """ ------  Stop IDs  -------- """ 

    def add_stopID (self,newStopID):
        self.userStops.append(newStopID)
          
    def print_stopIDs (self):
        print self.userStops
        
        
    def get_stops_for_trip(self, tripID):
        self.cur.execute("SELECT stop_ID, departure_time FROM stop_times where trip_ID ='" + tripID + "';")
        return self.cur.fetchall()
        
    def	get_trip_IDs (self, routeID):
        self.cur.execute("SELECT trip_ID, trip_headsign FROM trips where route_ID = '" + routeID + "';")
        return self.cur.fetchall();
        
        
    """ ------- Build DATA ----  """     
    def get_user_routes (self):	
        str = "("
        for num in self.userRoutes:
            str += "route_short_name == '" + num + "' OR "
            
        str = str[:-4]
        str += ");"
        self.userRoutes = []

        self.cur.execute("SELECT route_id \
                          FROM agency NATURAL JOIN routes\
                          WHERE agency_id == '"+ self.agency + "' AND " + 
                          str)
  
        self.userRoutes =(self.cur.fetchall())
        
    def get_user_trips(self):
        str = " "
        for routeID in self.userRoutes:
            self.cur.execute("SELECT trip_id, trip_headsign              \
                                FROM routes NATURAL JOIN trips         \
                                WHERE route_id == '" + routeID[0] + "';")
            self.agencyRoutes[routeID[0]] = self.cur.fetchall()
            str += "route_id != '" + routeID[0] + "' AND " 
            
        str = str[:-4]
        
        
        self.cur.execute("DELETE FROM trips \
                            WHERE" + str)  
        self.cur.execute("SELECT * FROM trips")
        print self.agencyRoutes
        print self.cur.fetchall()
    
    def get_times_for_route_at_stop(self):
    
        for (key, val) in self.agencyRoutes.iteritems():
            for (id,headsign) in val:
                self.cur.execute("SELECT departure_time\
                                    FROM stop_times\
                                    WHERE trip_id = '" + id + "' AND stop_id = '100666';")
                self.routeTimes[key] = self.cur.fetchall()
    
    
    def build_data(self):
        self.get_user_routes()
        self.get_user_trips()
        self.get_times_for_route_at_stop()
        #print self.routeTimes
        
        
        return 

    """
    def build_data(self):
        for uRoute in self.userRoutes:
            uRouteTrips = self.get_trip_IDs(uRoute)
            # Get Trips on that route
            for (rTripID,headSign) in uRouteTrips:
                tripStops = self.get_stops_for_trip(rTripID)
                # Get stops on that trip
                for (tripStop, time) in tripStops:
                    #get Stoptimes of those stops
                    if tripStop in self.userStops:
                        #compare the stop id to the userlist
                        print tripStop + " , " + time + " , " + headSign
    this code should be burned 
    """  

td = transdata()
td.init()
td.add_route("26")
td.add_route("39")
td.add_stopID("101414")
td.add_stopID("100666")
td.build_data()

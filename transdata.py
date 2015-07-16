import csv
import sqlite3 as sql
import sqlalchemy
import os
import time 

class transdata:

    def init(self, agency="1"):
        self.initdb()
        self.agency = agency
        self.agencyRoutes = {}
        self.routeTrips = {}
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
        # takes the self.userRoutes list and REPLACES it with their route_id's
        user_routes_string = ', '.join(self.userRoutes)
        sql = 'SELECT route_id FROM routes NATURAL JOIN agency WHERE route_short_name IN ({})'.format(user_routes_string)
        self.cur.execute(sql)
        self.userRoutes = [x[0] for x in self.cur.fetchall()]
        
    def get_user_trips(self):
        # take the self.userRoutes list of route_id's and return all of those routes' trips
        for routeid in self.userRoutes:
            self.cur.execute("SELECT trip_id                \
                                    FROM trips NATURAL JOIN routes             \
                                    WHERE route_id == '" + routeid + "';" )
            self.routeTrips[routeid] = [x[0] for x in self.cur.fetchall()]
        
    def get_times_for_trips_at_stops(self):
        for (route,trips) in self.routeTrips.iteritems():
            user_trips_string = ["'{}'".format(id) for id in trips]
            user_trips_string= ', '.join(user_trips_string)
            
            user_stopid_string = ', '.join(self.userStops)
          
            sql = 'SELECT departure_time,stop_id,trip_id FROM stop_times WHERE trip_id IN ({}) AND stop_id IN ({})'.format(user_trips_string,user_stopid_string)
            self.cur.execute(sql)
            self.routeTimes[route] = [x for x in self.cur.fetchall()]
            self.routeTimes[route].sort()
        
        
    def build_data(self, routenum):
        self.get_user_routes()
        self.get_user_trips()
        self.get_times_for_trips_at_stops()
        print self.routeTimes
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
td.add_stopID("101362")
td.build_data("26")

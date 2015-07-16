#So, this doesn't account for the date right now... it needs to.

import csv
import sqlite3 as sql
import sqlalchemy
import os
import datetime
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
        self.calendar_date = "" 
        self.service_ids = []
		
    def initdb(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
		# TO-DO: build the database if it's not built 
		#			1) import all the .txt to tables
		#			2) add indices to (stop_times, routes, and trips)
	
                
                
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
        service_string = time.strftime("%Y%m%d")
        weekday = datetime.datetime.today().weekday()
        if  weekday == 0:
            weekday = "monday"
        if  weekday == 1:
            weekday = "tuesday"
        if  weekday == 2:
            weekday = "wednesday"
        if  weekday == 3:
            weekday = "thursday"
        if  weekday == 4:
            weekday = "friday"
        if  weekday == 5:
            weekday = "saturday"
        if  weekday == 6:
            weekday = "sunday"
            
           
        
        user_routes_string = ["'{}'".format(id) for id in self.userRoutes]
        user_routes_string = ', '.join(user_routes_string)
#        print "SELECT service_id FROM calendar NATURAL JOIN trips WHERE start_date <= '{}' AND end_date > '{}' AND route_id IN ({}) AND {}== '1';".format(service_string, service_string, user_routes_string, weekday)

        self.cur.execute("SELECT DISTINCT service_id FROM calendar NATURAL JOIN trips WHERE start_date <= '{}' AND end_date > '{}' AND route_id IN ({}) AND {}== '1';".format(service_string, service_string, user_routes_string, weekday))
                            
        self.service_ids = self.cur.fetchone()[0]
        # TO-DO: Figure out if i ever need to handle more than one service_id
		
        for routeid in self.userRoutes:
            self.cur.execute("SELECT trip_id                \
                                    FROM trips NATURAL JOIN routes          \
                                    WHERE route_id == '" + routeid + "'	\
									AND service_id == '" + self.service_ids + "';")
										
            self.routeTrips[routeid] = [x[0] for x in self.cur.fetchall()]
        
    def get_times_for_trips_at_stops(self):
        for (route,trips) in self.routeTrips.iteritems():
            user_trips_string = ["'{}'".format(id) for id in trips]
            user_trips_string= ', '.join(user_trips_string)
            
            user_stopid_string = ', '.join(self.userStops)
          
            sql = 'SELECT departure_time FROM stop_times WHERE trip_id IN ({}) AND stop_id IN ({})'.format(user_trips_string,user_stopid_string)
            self.cur.execute(sql)
            self.routeTimes[route] = [x for x in self.cur.fetchall()]
            self.routeTimes[route].sort()
        
        
    def build_data(self, routenum):
        self.get_user_routes()
        self.get_user_trips()
        self.get_times_for_trips_at_stops()
        print self.routeTimes
        return 


td = transdata()
td.init()
td.add_route("26")
td.add_route("39")
td.add_stopID("100919")
td.build_data("26")

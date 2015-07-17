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

        #dictionary of {route:List<trip_id>
        self.routeTrips = {}
        
        #dictionary {route:List<time_strings>
        self.routeTimes = {}
        
        # list of routes (2 digits) given by user
        self.userRoutes = {}
        
        # list of stopids (6 digit) given by user
        self.userStops = {}
        
        # list of service_id's baesd on the routes and the dates
        self.lst_ServiceId = []
        
        self.weekday = -1
		
    def initdb(self):
        conn = sql.connect(os.getcwd() + "\\transdata\\bus_ticker.db")
        self.cur = conn.cursor()
		# TO-DO: build the database if it's not built 
		#			1) import all the .txt to tables
		#			2) add indices to (stop_times, routes, and trips)
	
    """  ------  Routes  -------- """ 
    # takes number and replaces with full route_id
    def add_route (self, newRouteNum):
        self.userRoutes[newRouteNum] = []
        
    def print_routes(self):
        print self.userRoutes

    def remove_route (self, newRouteNum):
        self.userRoutes.remove(RouteNum)
        
    """ ------  Stop IDs  -------- """ 

    def add_stopID (self,newStopId):
        self.userStops[newStopId] = []
          
    def print_stopIDs (self):
        print self.userStops
        
    def remove_stopID (self, stopID):
        self.userStops[stopID].delete()
        
    """------------BUILDING THE BUS TIMES ------------"""    
        
    def get_stops_for_trip(self, tripID):
        self.cur.execute("SELECT stop_ID, departure_time FROM stop_times WHERE trip_ID ='" + tripID + "';")
        return self.cur.fetchall()
        
    def	get_trip_IDs (self, routeID):
        self.cur.execute("SELECT trip_ID, trip_headsign FROM trips WHERE route_ID = '" + routeID + "';")
        return self.cur.fetchall()
        
        
    """ ------- Build DATA ----  """  
    
    def get_stop_locations (self):
        user_stops_string = ', '.join(self.userStops)
        self.cur.execute("SELECT stop_id , stop_name FROM stops WHERE stop_id in ({})".format(user_stops_string))
        for (id, loc) in self.cur.fetchall():
            self.userStops[id].append(loc)
        
    def set_date_string(self):    
        self.date_string = time.strftime("%Y%m%d")
        
    def set_weekday(self):    
        wkday = datetime.datetime.today().weekday()
        
        if  wkday == 0:
            wkday = "monday"
        elif wkday == 1:
            wkday = "tuesday"
        elif  wkday == 2:
            wkday = "wednesday"
        elif  wkday == 3:
            wkday = "thursday"
        elif  wkday == 4:
            wkday = "friday"
        elif  wkday == 5:
            wkday = "saturday"
        elif  wkday == 6:
            wkday = "sunday"
        else:
            print "INVALID DAY OF THE WEEK"
            exit(3)
        self.weekday = wkday    
            
    
    def get_user_routes (self):	
        # takes the self.userRoutes list and populates lst_RouteId
        user_routes_string = ', '.join(self.userRoutes)
        sql = 'SELECT route_id,route_short_name, route_long_name FROM routes NATURAL JOIN agency WHERE route_short_name IN ({})'.format(user_routes_string)
        self.cur.execute(sql)
        for (id, short, long) in self.cur.fetchall():
            self.userRoutes[short] = [id,long]
        
    def get_user_trips(self):

        # take the self.userRoutes list of route_id's and return all of those routes' trips
        user_routes_string = ["'{}'".format(val[0]) for val in self.userRoutes.values()]
        user_routes_string = ', '.join(user_routes_string)
        
        #get service_ids based on today's date, the routes selected and day of the week
        self.cur.execute("SELECT DISTINCT service_id FROM calendar NATURAL JOIN trips WHERE start_date <= '{}' AND end_date > '{}' AND route_id IN ({}) AND {}== '1';".format(self.date_string, self.date_string, user_routes_string, self.weekday))
        self.lst_ServiceId = [x[0] for x in self.cur.fetchall()]
            
        #get exceptions based on the date and it's an addition service
        self.cur.execute("SELECT service_id FROM calendar_dates WHERE date = '{}' AND exception_type == '1' ".format(self.date_string))
        self.lst_ServiceId += ([x[0] for x in self.cur.fetchall()])
        
        #TO-DO: handle calendar_dates table where there are special removals
        service_string = ["'{}'".format(id) for id in self.lst_ServiceId]
        service_string = ', '.join(service_string)
       # print service_string
        # TO-DO: (DONE) Figure out if i ever need to handle more than one service_id		
        for val in self.userRoutes.values():
            self.cur.execute("SELECT trip_id FROM trips NATURAL JOIN routes WHERE route_id == '{}' AND service_id IN ({});".format(val[0], service_string))
            self.routeTrips[val[0]] = [x[0] for x in self.cur.fetchall()]
        
    def get_times_for_trips_at_stops(self):
        for (route,trips) in self.routeTrips.iteritems():
            
            user_trips_string = ["'{}'".format(id) for id in trips]
            user_trips_string= ', '.join(user_trips_string)
            
            user_stopid_string = ', '.join(self.userStops)
          
            sql = 'SELECT departure_time, stop_id, trip_headsign FROM stop_times NATURAL JOIN trips WHERE trip_id IN ({}) AND stop_id IN ({})'.format(user_trips_string,user_stopid_string)
            self.cur.execute(sql)
            self.routeTimes[route] = self.cur.fetchall()
            self.routeTimes[route].sort()
        
        
    def build_data(self, routenum):
        self.get_stop_locations()
        self.set_weekday()
        self.set_date_string()
        self.get_user_routes()
        self.get_user_trips()
        self.get_times_for_trips_at_stops()
        #print self.routeTimes
        return 

    """ ----- INTERFACE ------ """ 
    def q_next_bus (self, routeNum):
        routeId = ''
        curTime = time.strftime("%H:%M:%S")
        
        for id in self.lst_RouteId:
            if id[:len(routeNum)] == routeNum:
                routeId = id

        if routeId is None:
            print "route not included in the build, add_route(routeNumber), build_data(): then try again"
            
        for stop_time in self.routeTimes[routeId]:
            if stop_time[:2] == "24":
                stop_time[:2] == "00"
            if stop_time[:2] == "25":
                stop_time[:2] == "01"
            if stop_time[:2] == "26":
                stop_time[:2] == "02"
            if stop_time[:2] == "27":
                stop_time[:2] == "03"
            if stop_time[0] > curTime:
                return "The next {} {} arrives at {} (#{})".format(routeNum,stop_time[2],stop_time[0], stop_time[1])
            
            
    def q_bus (self, routeNum, curTime = time.strftime("%H:%M:%S")):
        retval = []
        forwardCount = 1
        routeId = self.userRoutes[routeNum][0]
        if routeId is None:
            print "route not included in the build, add_route(routeNumber), build_data(): then try again"
        #print self.routeTimes[routeId]
        prevTime = ""        
        for (stop_time,stop_id,headsign) in self.routeTimes[routeId]:
            
            if stop_time[:2] == "24":
                stop_time[:2] == "00"
            if stop_time[:2] == "25":
                stop_time[:2] == "01"
            if stop_time[:2] == "26":
                stop_time[:2] == "02"
            if stop_time[:2] == "27":
                stop_time[:2] == "03"
                
            if (stop_time > curTime):
                #print retval
                if forwardCount == 1:
                    retval.append(prevTime)
                if forwardCount > 4:
                    return retval
                retval.append(stop_time)
                forwardCount = forwardCount + 1
            prevTime = stop_time
        return retval
        
        
if (__name__ == "__main__"):
            
    td = transdata()
    td.init("1") # 1 is agency ID of Victoria
    td.add_route("26")
    td.add_route("39")
    td.add_stopID("100919")
    td.add_stopID("101424")
    td.build_data("26")

#print td.q_next_bus("26")
    r = "39"
    print td.q_bus(r)




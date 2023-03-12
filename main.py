####################################################################
#
# Name: Jose Lara 
# UIN: 664072746
#
# Overview: This python and SQLite program is meant to give the 
# user an interface that will ultimately allow them to view certain
# information related to the database CTA2_L_daily_ridership. This 
# information comes down to number of riders per station
# over the course of a weekday or weekend, line colors and if it 
# has accecibility for those who have disabilities, plotting the stats
# of people riding the lines, etc. This is meant to analyze the 
# information that can be found in the database and give the user a general
# idea of the usage of the CTA stations over a period of time. 
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################  
#
# printPartialStationNames
#
# Given a connection to the CTA database, It executes an SQL query that searches
# For station names that have a partial resemblance to what the user wants to find.
#

def printPartialStationNames(dbConn):
  dbCursor = dbConn.cursor();
  
  UserInput = input("Enter partial station name (wildcards _ and %): ");
  
  sql = """SELECT Station_ID, Station_Name
             FROM Stations
             WHERE Station_Name LIKE ?
             ORDER BY Station_Name ASC;"""
  
  dbCursor.execute(sql,[UserInput])
  rows = dbCursor.fetchall()
  
  if(len(rows) > 0):
    for row in rows:
      print(row[0], ":", row[1])
  else:
    print("**No stations found...")

  dbCursor.close();


##################################################################  
#
# printRidershipInfo
#
# Given a connection to the CTA database, It executes an SQL query that prints out the number of riders 
# per station with percentages that show which station sees the most use over the year
#

def printRidershipInfo(dbConn):
  dbCursor = dbConn.cursor();
  
  print("** ridership all stations **");
  
  sql = """SELECT Station_Name, SUM(Num_Riders), SUM(Num_Riders)
           FROM Ridership JOIN Stations on Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY Station_Name ASC;"""
  
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  
  sql = """SELECT SUM(Num_Riders)
           FROM Ridership;"""
  dbCursor.execute(sql)
  total = dbCursor.fetchall()
  for row in rows:
    print(row[0], ":", f"{row[1]:,}", f"({(row[2] * 100)/total[0][0]:.2f}%)")

  dbCursor.close()


##################################################################  
#
# printTopTenBusiestStations
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out
# the Top 10 busiest stations.
#
  
def printTopTenBusiestStations(dbCursor):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **",end = "");
  print("")

  sql = """SELECT Station_Name, SUM(Num_Riders), SUM(Num_Riders)
           FROM Ridership JOIN Stations on Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY SUM(Num_Riders) DESC
           LIMIT 10;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  sql = """SELECT SUM(Num_Riders)
           FROM Ridership;"""
  dbCursor.execute(sql)
  total = dbCursor.fetchall()
  for row in rows:
     print(row[0], ":", f"{row[1]:,}", f"({(row[2] * 100)/total[0][0]:.2f}%)")

  dbCursor.close();


##################################################################  
#
# printTenLeastBusiestStations
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out
# the Ten least Busies Stations and outputs them to the user.
#
  
def printTenLeastBusiestStations(dbConn):
  dbCursor = dbConn.cursor()
  
  print("** least-10 stations **");
  
  sql = """SELECT Station_Name, SUM(Num_Riders), SUM(Num_Riders)
           FROM Ridership JOIN Stations on Ridership.Station_ID = Stations.Station_ID
           GROUP BY Station_Name
           ORDER BY SUM(Num_Riders) ASC
           LIMIT 10;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  sql = """SELECT SUM(Num_Riders)
           FROM Ridership;"""
  dbCursor.execute(sql)
  total = dbCursor.fetchall()
  for row in rows:
     print(row[0], ":", f"{row[1]:,}", f"({(row[2] * 100)/total[0][0]:.2f}%)")

  dbCursor.close();

  
##################################################################  
#
# printStationsByColor
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out
# the Stations that have that color designation alongside information about the direction they head,
# station name, and if they are accesible for people with disabilities.
#
  
def printStationsByColor(dbConn):
  dbCursor = dbConn.cursor()

  userInput = input("Enter a line color (e.g. Red or Yellow): ").lower().title();

  sql = """SELECT Stop_Name, Direction, ADA
           FROM Stops 
           JOIN StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           JOIN Lines on StopDetails.Line_ID = Lines.Line_ID
           WHERE Color == ?
           Order BY Stop_Name ASC;"""
  dbCursor.execute(sql,[userInput])
  rows = dbCursor.fetchall()

  if(len(rows) > 0):
      for row in rows:
        if row[2] == 1:
          print(row[0], ": Direction =", f"{row[1]}", "(Accessible? yes)")
        else: 
          print(row[0], ": Direction =", f"{row[1]}", "(Accessible? no)")
  else:
      print("**No such line...")
    
  dbCursor.close();

  
##################################################################  
#
# printRiderShipPerMonth
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the stats of riders per month 
# the user will have acess total riders per month over the corse of the year and will have the option to plot it so that they can 
# visualize it a bit better
#
  
def printRiderShipPerMonth(dbConn):
  dbCursor = dbConn.cursor()

  print("** ridership by month **");


  x = []
  y = []
  
  sql = """SELECT strftime('%m', Ride_Date), SUM(Num_Riders)
           FROM Ridership
           GROUP BY strftime('%m', Ride_Date)
           ORDER BY strftime('%m', Ride_Date) ASC;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  for row in rows:
    print(row[0], ":", f"{row[1]:,}")

  print("");
  print("Plot? (y/n)", end="");
  cmd = input().lower();

  if(cmd == "y"):
    for row in rows:
      x.append(row[0])
      y.append(row[1])
    plt.xlabel("month")
    plt.ylabel("number of riders(x * 10^8)")
    plt.title("monthly ridership")
    plt.plot(x,y)
    plt.show()
  dbCursor.close();


##################################################################  
#
# printRiderShipPerYear
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the stats of riders per year 
# from the years 2001-2021.
# the user will have acess total riders per year over the corse of 2001-2021 and will have the option to plot it so that they can 
# visualize it a bit better
#
  
def printRiderShipPerYear(dbConn):
  dbCursor = dbConn.cursor()

  print("** ridership by year **");

  x = []
  y = []

  sql = """SELECT strftime('%Y',Ride_Date), SUM(Num_Riders)
           FROM Ridership
           GROUP BY strftime('%Y',Ride_Date)
           ORDER BY strftime('%Y', Ride_Date) ASC;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  
  for row in rows:
    print(row[0], ":", f"{row[1]:,}")

  print();
  print("Plot? (y/n)",end = "");
  cmd = input().lower();

  if(cmd == "y"):
    for row in rows:
      x.append(row[0][2:4])
      y.append(row[1])
    plt.xlabel("year")
    plt.ylabel("number of riders(x * 10^8)")
    plt.title("yearly ridership")
    plt.plot(x,y)
    plt.show()

  dbCursor.close();

  
##################################################################  
#
# printOutFirstFiveDays
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the first five days of the 
# selected station followed by the amount of riders in that day.
#
  
def printOutFirstFiveDays(dbCursor,userYear,userStation):

  sql = """SELECT date(Ride_Date), Num_Riders
          FROM Stations
          JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
          WHERE strftime("%Y", Ride_Date) == ? AND Station_Name LIKE ?
          ORDER BY Ride_Date ASC
          LIMIT 5;"""
  
  dbCursor.execute(sql,[userYear,userStation]);
  rows = dbCursor.fetchall();

  for row in rows:
    print(row[0], f"{row[1]}")


  
##################################################################  
#
# printOutLastFiveDays
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the last five days of the 
# selected station followed by the amount of riders in that day.
#
  
def printOutLastFiveDays(dbCursor,userYear,userStation):

  sql = """SELECT date(Ride_Date), Num_Riders
          FROM Stations
          JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
          WHERE strftime("%Y", Ride_Date) == ? AND Station_Name LIKE ?
          GROUP BY Ride_Date
          ORDER BY Ride_Date DESC
          LIMIT 5;"""
  
  dbCursor.execute(sql,[userYear,userStation]);
  rows = dbCursor.fetchall();
  rows.reverse();
  
  
  for row in rows:
    print(row[0], f"{row[1]}")
 

  
##################################################################  
#
# printStationIDName
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the name of the station 
# alongside its ID 
#
  
def printStationIDName(dbCursor,userStation):
  sql = """SELECT Station_ID, Station_Name
          FROM Stations
          WHERE Station_Name LIKE ?
          LIMIT 5;"""
  
  dbCursor.execute(sql,[userStation])
  rows = dbCursor.fetchall();

  for row in rows:
    print("Station 1:", row[0], f"{row[1]}")


  
##################################################################  
#
# printStationIDName2
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies prints out the name of the station 
# alongside its ID 
#
  
def printStationIDName2(dbCursor,userStation):
  sql = """SELECT Station_ID, Station_Name
          FROM Stations
          WHERE Station_Name LIKE ?
          LIMIT 5;"""
  
  dbCursor.execute(sql,[userStation])
  rows = dbCursor.fetchall();

  for row in rows:
    print("Station 2:", row[0], f"{row[1]}")

  
##################################################################  
#
# checkIfExistantOrMultiple
#
# Given a connection to the CTA database, It executes an SQL query that as the name implies it checks if a query returns multiple
# stations. This is achieved by passing in the table from the query and then checking the size to make sure it has 365 or 366 entries
# this is related to the year. It is meant to find if we have multiple stations or if there is no data for that year or if you have the
# wrong station name input.
#
  
def checkIfExistantOrMultiple(returnToUser,rows):
  if(len(rows) <= 366 and len(rows) > 0):
    returnToUser = 1;
    return returnToUser;
  elif(len(rows) > 366):
    returnToUser = 0;
    return returnToUser;
  elif(len(rows) == 0):
    returnToUser = 2;
    return returnToUser;
  else:
    returnToUser = 3;
    return returnToUser;

    
##################################################################  
#
# compareTwoStationsPlot
#
# Given a connection to the CTA database, It executes 2 SQL queries related to the stations the user wants to compare.
# if at any point there is an issue with the station name not existing or we get multiple stations from one query then we will tell the
# user and or return a warning message depending on the infraction, they will then be able to launch the command again. 
# assuming both queries are valid then it will display the first and last 5 days of operation and the number of riders for that day
# this will be for each station that is being compared. The user will then get the option to plot it or to just take the data as is. 
#
    
def compareTwoStationsPlot(dbConn):
  dbCursor = dbConn.cursor()
  
  userYear = input("Year to compare against? ");
  print("")

  x = []
  y = []
  x1 = []
  y1 = []
  day = 1;
  day2 = 1;

  returnToUser = 0;
  returnToUser2 = 0;

  print("Enter station 1 (wildcards _ and %): ", end = "")
  userInputStaOne = input();
 

  sql = """SELECT Ride_Date, Num_Riders, Station_Name
          FROM Stations
          JOIN Ridership ON Stations.Station_ID = Ridership.Station_ID
          WHERE strftime("%Y", Ride_Date) == ? AND Station_Name LIKE ?
          ORDER BY Ride_Date ASC;"""
  
  dbCursor.execute(sql,[userYear,userInputStaOne]);
  rows = dbCursor.fetchall()

  returnToUser = checkIfExistantOrMultiple(returnToUser,rows);

  if(returnToUser == 1):
    print("");
    print("Enter station 2 (wildcards _ and %): ", end ="");
    userInputStaTwo = input();
    dbCursor.execute(sql,[userYear,userInputStaTwo]);
    rows2 = dbCursor.fetchall()
    returnToUser2 = checkIfExistantOrMultiple(returnToUser,rows2);
    if(returnToUser2 == 1):
      printStationIDName(dbCursor,userInputStaOne);
      printOutFirstFiveDays(dbCursor,userYear,userInputStaOne);
      printOutLastFiveDays(dbCursor,userYear,userInputStaOne);
      printStationIDName2(dbCursor,userInputStaTwo);
      printOutFirstFiveDays(dbCursor,userYear,userInputStaTwo);
      printOutLastFiveDays(dbCursor,userYear,userInputStaTwo);
      print("")
      plotInput = input("Plot? (y/n) ");
      if(plotInput == "y"):
        for row in rows:
          x.append(day)
          y.append(row[1])
          day += 1;
        for row2 in rows2:
          x1.append(day2)
          y1.append(row2[1])
          day2 += 1;
        plt.xlabel("day")
        plt.ylabel("number of riders")
        plt.title("riders each day of 2020")
        plt.plot(x,y)
        plt.plot(x1,y1)
        plt.legend([row[2],row2[2]])
        plt.show()
    elif(returnToUser2 == 0):
      print("**Multiple stations found...")
    elif(returnToUser2 == 2):
      print("**No station found...")
  elif(returnToUser == 0):
    print("**Multiple stations found...")
  elif(returnToUser == 2):
    print("**No station found...")
  
  print("");
  dbCursor.close();

  
##################################################################  
#
# outputStationNamePartOfLineColorPotentialPlot
#
# Given a connection to the CTA database, It executes 2 SQL queries related to the stations the user wants to compare.
# if at any point there is an issue with the station name not existing or we get multiple stations from one query then we will tell the
# user and or return a warning message depending on the infraction, they will then be able to launch the command again. 
# assuming both queries are valid then it will display the first and last 5 days of operation and the number of riders for that day
# this will be for each station that is being compared. The user will then get the option to plot it or to just take the data as is. 
#

def outputStationNamePartOfLineColorPotentialPlot(dbConn):
  dbCursor = dbConn.cursor()

  x = []
  y = []

  userInput = input("Enter a line color (e.g. Red or Yellow): ").lower().title();
  
  sql = """SELECT DISTINCT Station_Name, Latitude, Longitude
           FROM Stops 
           JOIN Stations on Stops.Station_ID = Stations.Station_ID
           JOIN StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           JOIN Lines on StopDetails.Line_ID = Lines.Line_ID
           WHERE Color == ?
           Order BY Station_Name ASC;"""
  dbCursor.execute(sql,[userInput])
  rows = dbCursor.fetchall()

  if(len(rows) > 0):
      for row in rows:
        print(row[0], ":", f"({row[1]},",f"{row[2]})");
      print("Plot? (y/n) ");
      plotInput = input();
      if(plotInput == "y"):
        for row in rows:
          x.append(row[2])
          y.append(row[1])
        image = plt.imread("chicago.png");
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868];
        plt.imshow(image,extent=xydims);
        plt.title(userInput.lower() + " line");
        if(userInput.lower() == "purple-express"):
          userInput = "Purple"
        plt.plot(x,y,"o",c = userInput);
        for row in rows:
          plt.annotate(row[0],(row[2],row[1]))
        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()
  else:
      print("**No such line...")
    
  dbCursor.close();

  
##################################################################  
#
# printNumberOfStops
#
# Given a connection to the CTA database, It executes an SQL query that will count how many possible stops (In stations)
# exist within the given database.
#
  
def printNumberOfStops(dbConn):
  dbCursor = dbConn.cursor() 
    
  dbCursor.execute("SELECT count(Stop_ID) From Stops;")
  row = dbCursor.fetchone();
  print("  # of stops:", f"{row[0]:,}")
  
  dbCursor.close();


##################################################################  
#
# printNumberOfRideEntries
#
# Given a connection to the CTA database, It executes an SQL query that will count and return to the user the number of ride entries 
# that exist within our given database.
#
  
def printNumberOfRideEntries(dbConn):
  dbCursor = dbConn.cursor()
  
  dbCursor.execute("SELECT count(Station_ID) From Ridership;")
  row = dbCursor.fetchone();
  print("  # of ride entries:", f"{row[0]:,}")
  
  dbCursor.close();

  
##################################################################  
#
# printDateRange
#
# Given a connection to the CTA database, It will execute two SQL queries to find the starting date from when the data began to be added
# all the way to the last date recorded for the CTA usage. This in turn is seen as a time frame that the user can see.
#
  
def printDateRange(dbConn):
  dbCursor = dbConn.cursor()

  sql = """SELECT Date(Ride_Date) 
           FROM Ridership
           ORDER BY Ride_Date ASC
           LIMIT 1;"""
  
  dbCursor.execute(sql)
  
  row = dbCursor.fetchone();

  sql2 ="""SELECT Date(Ride_Date) 
           FROM Ridership
           ORDER BY Ride_Date DESC
           LIMIT 1;"""
  
  dbCursor.execute(sql2);

  row2 = dbCursor.fetchone();

  print("  date range:", f"{row[0]}","-",f"{row2[0]}")

  dbCursor.close();


##################################################################  
#
# printTotalRiderShip
#
# Given a connection to the CTA database, It will execute a SQL query to print out the total number of riders within found within the data
# base starting from the 1st year of data being recorded to the last date recorded.
#
  
def printTotalRiderShip(dbConn):
  dbCursor = dbConn.cursor()
  
  dbCursor.execute("SELECT SUM(Num_Riders) From Ridership;")
  row = dbCursor.fetchone();
  print("  Total ridership:", f"{row[0]:,}")

  dbCursor.close();


##################################################################  
#
# printWeekdayRidership
#
# Given a connection to the CTA database, It will execute a SQL query that as the name implies print out the number of riders over the
# course of the weekdays. Will also give a user a percentage that will help them know how much traffic was seen on a weekday compared to 
# all the entries that exist in the database.
#
  
def printWeekdayRidership(dbConn):
  dbCursor = dbConn.cursor()

  sql = """SELECT SUM(Num_Riders)
           FROM Ridership
           WHERE Type_of_Day == "W";"""
  dbCursor.execute(sql);
  row = dbCursor.fetchone();

  dbCursor.execute("""SELECT SUM(Num_Riders) FROM Ridership""");
  total = dbCursor.fetchone();
  
  
  print("  Weekday ridership:", f"{row[0]:,}", f"({(row[0] * 100)/total[0]:.2f}%)")

  dbCursor.close();


##################################################################  
#
# printSaturdayRiderShip
#
# Given a connection to the CTA database, It will execute a SQL query that as the name implies print out the number of riders over the
# course of Saturday. Will also give a user a percentage that will help them know how much traffic was seen on a Saturday compared to 
# all the entries that exist in the database.
#
  
def printSaturdayRiderShip(dbConn):
  dbCursor = dbConn.cursor()

  sql = """SELECT SUM(Num_Riders)
           FROM Ridership
           WHERE Type_of_Day == "A";"""
  dbCursor.execute(sql);
  row = dbCursor.fetchone();

  dbCursor.execute("""SELECT SUM(Num_Riders) FROM Ridership""");
  total = dbCursor.fetchone();
  
  
  print("  Saturday ridership:", f"{row[0]:,}", f"({(row[0] * 100)/total[0]:.2f}%)")

  dbCursor.close();


##################################################################  
#
# printSundayHolidayRidership
#
# Given a connection to the CTA database, It will execute a SQL query that as the name implies print out the number of riders over the
# course of Sunday's and Holiday's. Will also give a user a percentage that will help them know how much traffic was 
# seen on Sunday's and Holiday's compared to all the entries that exist in the database.
#
  
def printSundayHolidayRidership(dbConn):
  dbCursor = dbConn.cursor()

  sql = """SELECT SUM(Num_Riders)
           FROM Ridership
           WHERE Type_of_Day == "U";"""
  dbCursor.execute(sql);
  row = dbCursor.fetchone();

  dbCursor.execute("""SELECT SUM(Num_Riders) FROM Ridership""");
  total = dbCursor.fetchone();
  
  
  print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({(row[0] * 100)/total[0]:.2f}%)")

  dbCursor.close();

##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#

def print_stats(dbConn):
  dbCursor = dbConn.cursor() 
    
  print("General stats:")
    
  dbCursor.execute("Select count(*) From Stations;")
  row = dbCursor.fetchone();
  print("  # of stations:", f"{row[0]:,}")
  printNumberOfStops(dbConn);
  printNumberOfRideEntries(dbConn);
  printDateRange(dbConn);
  printTotalRiderShip(dbConn);
  printWeekdayRidership(dbConn);
  printSaturdayRiderShip(dbConn);
  printSundayHolidayRidership(dbConn);

  print("")
  dbCursor.close();


##################################################################  
#
# main
#
 
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
print_stats(dbConn)

print("Please enter a command (1-9, x to exit): ", end ="")
cmd = input();
while(cmd != "x" or cmd != "X"):
  if cmd == "1":
    print("");
    printPartialStationNames(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "2":
    printRidershipInfo(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "3":
    printTopTenBusiestStations(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "4":
    printTenLeastBusiestStations(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "5":
    print("");
    printStationsByColor(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "6":
    printRiderShipPerMonth(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "7":
    printRiderShipPerYear(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "8":
    print("");
    compareTwoStationsPlot(dbConn);
    print("");
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "9":
    print("")
    outputStationNamePartOfLineColorPotentialPlot(dbConn);
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();
  elif cmd == "x":
    break;
  else:
    print("**Error, unknown command, try again...");
    print("")
    print("Please enter a command (1-9, x to exit): ", end ="")
    cmd = input();

#
# done
#

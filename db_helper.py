import mysql.connector

class DB:
    def __init__(self):
        # connect to the database server
        try:
            self.conn = mysql.connector.connect(
                host='', # Enter the DNS here
                user='', # Enter sql user name
                password='', # Enter MySql password
                database='' # Enter the database name here + update the queries below
                )
            self.my_cursor = self.conn.cursor()
            print('Connection established.....')
        except:
            print('Connection error.....')

    def fetch_city_names(self):

        cities = []
        self.my_cursor.execute("""
            SELECT DISTINCT(Source) from flights.flights
            UNION
            SELECT DISTINCT(Destination) from flights.flights
        """)

        data = self.my_cursor.fetchall()

        for city in data:
            cities.append(city[0])

        return cities
    
    def fetch_all_flights(self,source,destination):
        self.my_cursor.execute('''
            SELECT Airline,Route,Dep_Time,Duration,Price FROM flights.flights
            WHERE Source = '{}' and Destination = '{}';
        '''.format(source,destination))

        data = self.my_cursor.fetchall()

        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        self.my_cursor.execute('''
            SELECT Airline,Count(*) FROM flights.flights
            GROUP BY Airline;
        ''')
        data = self.my_cursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline,frequency
    
    def busy_airport(self):

        city = []
        frequency = []

        self.my_cursor.execute('''
            SELECT Source, COUNT(*) FROM (  SELECT Source FROM flights.flights
								union all
								SELECT Destination FROM flights.flights) t
            group by t.Source
            order by count(*) desc;
        ''')

        data = self.my_cursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city,frequency
    
    def daily_frequency(self):

        date = []
        frequency = []

        self.my_cursor.execute('''
            Select Date_of_Journey,Count(*) from flights.flights
            group by Date_of_Journey;
        ''')

        data = self.my_cursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date,frequency
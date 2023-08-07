from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase("user_query_results.db")

current_time = datetime.now()



class ModelBase(pw.Model):
	date_creation = pw.DateField(default=current_time.strftime("%Y-%m-%d"))
	command_name = pw.TextField()
	user_id = pw.IntegerField()
	user_name = pw.TextField(null=True)

	class Meta:
		database = db


class Airports(ModelBase):
	full_airport_address = pw.CharField(max_length=300)
	iata = pw.TextField()
	location_lat = pw.FloatField()
	location_lon = pw.FloatField()


class Airplanes(ModelBase):
	airline_name = pw.TextField()
	flight_number = pw.TextField()
	aircraft_reg_number = pw.TextField()
	iata_departure = pw.CharField(max_length=3)
	terminal_departure = pw.CharField(max_length=5)
	gate_departure = pw.CharField(max_length=5)
	revised_time_departure = pw.DateTimeField()
	fact_time_departure = pw.DateTimeField()
	iata_arrival = pw.CharField(max_length=3)
	terminal_arrival = pw.CharField(max_length=5)
	flight_status = pw.CharField(max_length=10)
	last_update_time = pw.DateTimeField()

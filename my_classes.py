import threading
import ctypes
import sqlite3
from sqlite3 import Error


class my_threads(threading.Thread):
	def get_id(self):
		# returns id of the respective thread
		if hasattr(self, '_thread_id'):
			return self._thread_id
		for id, thread in threading._active.items():
			if thread is self:
				return id
  
	def stop(self):
		self._is_stopped = True
		self.thread_id = self.get_id()
		self.res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, ctypes.py_object(SystemExit))
		if self.res > 1:
			ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, 0)

	def is_stopped(self):
		return self._is_stopped


#creating class to manage Database.
class DB:
	def __init__(self, DBFile):
		self.DBFile = DBFile
		self.conn = self.CreateConnection(self.DBFile)
		# Creating a cursor object using the  cursor() method
		self.cursor = self.conn.cursor()


		#create function to Connect to sqlite and create db file if not found.
	def CreateConnection(self, db_file):
		conn = None
		try:
			conn = sqlite3.connect(db_file)
		except Error:
			return False

		return conn

	# create function to create table
	def CreateTable(self, TableName, columns):
		table = f"""CREATE TABLE {TableName}{columns};"""
		#Creating table
		try:
			self.cursor.execute(table)
		except Error:
			return False

		return True

#create function to insert data to table
	def InsertData(self, TableName, Data):

#inserting data
		try:
			self.cursor.execute(f'''INSERT INTO {TableName} VALUES {Data};''')
		except sqlite3.OperationalError:
			return False

		# Commit your changes in the database	
		self.conn.commit()

	#create function to get data from table
	def GetData(self, TableName):
		# Query for the specified table
		try:
			data = self.cursor.execute(f'''SELECT * FROM {TableName}''')
		except sqlite3.OperationalError:
			return False

		return data.fetchall()

	# creating function to Search for specific data
	def SearchData(self, TableName, ColumnName, SearchText):
		# Query for the specified Value
		try:
			data = self.cursor.execute(f"SELECT * FROM {TableName} WHERE {ColumnName} LIKE '%{SearchText}%';")
		except sqlite3.OperationalError:
					return False

		return data.fetchall()

	# Creating function to delete the selected item in any table.
	def DeleteItem(self, TableName, ColumnName, Value):
		# Query for delete item
		data = self.cursor.execute(f"  DELETE FROM {TableName} WHERE {ColumnName} = '{Value}';")

		# Commit your changes in the database	
		self.conn.commit()
		# Clean the Database from the deleted items.
		self.cursor.execute(f'VACUUM;')


# Closing the connection
	def CloseConnection(self):
		self.conn.close()

#End of class

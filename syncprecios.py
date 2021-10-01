import os, os.path
import sys
#import sqlite3
#import qrcode as qr
import pandas as pd
from Control import Control

conexion = None
cursor   = None
codes    = {'Codigo':[], 'Turno':[], 'Pedido':[]}
data = []

connection_config = {
	'host'    	 : 'localhost',
	'database'	 : 'bt',
	'user'    	 : 'master',
	'password'	 : 'asd.123',
	'auth_plugin': 'mysql_native_password' 
					}

querys = {'testCon': "SHOW DATABASES;"}
def open_database():
	global conexion
	global cursor
	conexion = sqlite3.connect('/home/chls/Documentos/bt/productos.db')
	cursor = conexion.cursor()
	if not cursor:
		print('Error')

def close_database(save = False):
	global conexion
	global cursor

	if save:
		conexion.commit()
	cursor.close()
	conexion.close()
	cursor = None
	conexion = None

def open_file_sheet():
	global data
	temp   = []
	colums = []

	for colum in df:
		colums.append(colum)
	size = len(df[colums[0]].tolist())
	count = 0
	while count < size:
		for item in colums:
			temp.append(df[item][count])
		data.append(temp)
		del temp
		temp = []
		count += 1
	return True

def updater_(dataL):
	if not data: return
	kery = {'insertProd':"INSERT INTO Productos (Codigo, Nombre, PrecioCosto) VALUES ('{0}','{1}', {2})",
			'getIDProdu':"SELECT ID FROM Productos WHERE Codigo = '{0}'",
			'insertPrec':"INSERT INTO Precios (CodigoProducto, Precio, OrdenPrecio) VALUES ((SELECT ID FROM Productos WHERE Codigo = '{0}'),{1},{2})" }

	cursor.execute(kery['insertProd'].format(*dataL[:3]))
	conexion.commit()

	print(f'updater(dataL) >> {dataL[1]}')
	dataL.remove(dataL[1]), dataL.remove(dataL[1])
	cursor.execute(kery['insertPrec'].format(dataL[0], dataL[1],  1))
	cursor.execute(kery['insertPrec'].format(dataL[0], dataL[2],  2))

def updater(dataL):
	if not data: return
	kery = {'insertProd' : "INSERT INTO Productos (Codigo, Nombre, PrecioCosto) VALUES ('{0}','{1}', {2})",
			'getIDProdu' : "SELECT ID FROM Productos WHERE Codigo = '{0}'",
			'insertPrec' : "INSERT INTO Precios (CodigoProducto, Precio, OrdenPrecio) VALUES ((SELECT ID FROM Productos WHERE Codigo = '{0}'),{1},{2})",
			'checkCodigo': "SELECT Codigo FROM Productos WHERE Codigo = '{0}'" }

	exist_code = m_control.control_generic_consult(kery['checkCodigo'].format(dataL[0]),1,0)
	if len(exist_code) >= 1:
		print('this item exist!', exist_code)
		return
	m_control.control_generic_consult(kery['insertProd'].format(*dataL[:3]),1,1)

	print(f'updater(dataL) >> {dataL[1]}')
	dataL.remove(dataL[1]), dataL.remove(dataL[1])
	m_control.control_generic_consult(kery['insertPrec'].format(dataL[0], dataL[1],  1),0,1)
	m_control.control_generic_consult(kery['insertPrec'].format(dataL[0], dataL[2],  2),0,1)

def db_updater():
	m_control.open_data()
	print('Database is opened!')
	for item in data:
		updater(item)
	m_control.close_data(1)


if __name__ == '__main__':
	m_control = Control()
	print ("This is the name of the script: ", sys.argv[0])
	print ("Number of arguments: ", len(sys.argv))
	print ("The arguments are: " , str(sys.argv))
	if len(sys.argv) > 1:
		df = pd.read_excel(sys.argv[1])
		print('Database is opened!')
		open_file_sheet()
		db_updater()
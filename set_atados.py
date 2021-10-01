from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorBuffered, MySQLCursorBufferedDict, MySQLCursorBufferedNamedTuple
from mysql.connector.optionfiles import MySQLOptionsParser
import mysql.connector	 # required pip install mysql-connector-python
from mysql.connector import Error, errorcode
import pandas as pd
from blabel import LabelWriter
import sys


data   = []
file_name = None

connection_config = {
	'host'    	 : '192.168.1.51',
	'database'	 : 'nsr_starbusiness',
	'user'    	 : 'master',
	'password'	 : 'masterAwes.123',
	'auth_plugin': 'mysql_native_password'}

connection_config2 = {
	'host'    	 : 'localhost',
	'database'	 : 'starbusiness',
	'user'    	 : 'master',
	'password'	 : 'asd.123',
	'auth_plugin': 'mysql_native_password'}    


class Control_Server:
    def __init__(self, connection_config_parser) -> None:
        self.connection_config_parser = connection_config_parser
        self.conexion = None
        self.cursor = None

    def connect_server(self) -> MySQLConnection:
        if (self.conexion and self.cursor) != None:
            return True
        self.conexion = mysql.connector.connect(**self.connection_config_parser)
        self.cursor = self.conexion.cursor()
        

    def disconnect_server(self, commit_ = False) -> MySQLConnection:
        if commit_:
            self.conexion.commit()
        self.cursor.close()
        self.conexion.close()
        self.conexion = None
        self.cursor = None

    def insert_statement(self, query, *args) -> MySQLOptionsParser:
        self.cursor.execute(query.format(*args))


    def get_statement(self, query) -> list:
        self.cursor.execute(query)
        l = list(self.cursor.fetchall())
        return l

class Doc_Reader:
    def __init__(self, file_name = None) -> None:
        self.file_name = file_name
        self.headers = []
        self.list_   = []
        self.sheet = None
        self.xls = None

    def open_doc(self):
        self.xls = pd.ExcelFile(self.file_name)
        self.sheet = self.xls.parse(0)
        self.headers = [e for e in self.sheet]

class Store_DB_Elements:
    def __init__(self) -> None:
        self.laber_writer = LabelWriter("index.html", default_stylesheets=("syle.css",))
        self.record = []
        self.product  = 0
        self.cuantity = 1
        self.price    = 2
        self.nut      = 3

        self.orders = {'a1':'fulano_de_tal'}

        self.order_detail = {'a1':['producto', 'cantidad', 'precio', 'tuerca']
                            }
    def make_stiker(self) -> None:
        for order in self.orders:
            for item_l in self.order_detail[order]:
                self.record.append(dict(order_num=order, client_name=self.orders[order], product_name=item_l[self.product], 
                                        product_cuantity=item_l[self.cuantity], product_price=item_l[self.price], product_nut=item_l[self.nut]))
        self.laber_writer.write_labels(self.record, target='test.pdf')
    def show_order(self) -> dict:
        print("[Orden],     [Cliente],          [Producto],          [Cantidad],        [Precio],       [Tuerca]")
        for order in self.orders:
            for items in self.order_detail[order]:

                print(f"[{order}], [{self.orders[order]}], [{items[self.product]}], [{items[self.cuantity]}], [{items[self.price]}], [{items[self.nut]}]")
    
    'APPEND ORDER ADN CUSTOMER NAME IN SELF.ORDERS{}'
    def insert_order(self,order='', client='') -> None:
        if order in self.orders:
            return
        self.orders[order] = client

    'APPEND ORDER ADN CUSTOMER NAME IN SELF.ORDERS_DETAIL{}'
    def insert_order_detail(self, order, *args) -> list:
        if order in self.order_detail:
            return
        self.order_detail[order] = [l for l in args]

    'DELETE ANY ORDER AND CUSTOMER AND ORDER DETAILT FROM SELF.ORDERS AND SELF.ORDER_DETAIL'
    def delete_order(self, order='') -> None:
        if order in self.orders:
            del self.order_detail[order]
            del self.orders[order]

class Run_Objs(Doc_Reader, Control_Server, Store_DB_Elements):

    def __init__(self, file_name_ = None, conexion_config_parser_ = None) -> None:
        Doc_Reader.__init__(self, file_name =file_name_)
        Control_Server.__init__(self, connection_config_parser=conexion_config_parser_)
        Store_DB_Elements.__init__(self)
        self.label_writer_f = 'Pedido_{0}_template.html'
        self.label_writer = None
        self.querys = {'insert_atado' : "INSERT INTO productosatados (idprimary, idsecundary) VALUES ({0},{1});"}

    def make_stiker(self, order):
        self.label_writer = LabelWriter(self.label_writer_f.format(order), default_stylesheets='style.css')
        records = [
            dict(sample_id="s01", sample_name="sample 1"),
            dict(sample_id="s02", samble_name="sample 2")
        ]
        self.label_writer.write_labels(records, target='qrcode.pdf')

    def fuse_code(self) -> None:
        for n, x in enumerate(self.sheet[self.headers[0]]):
            self.list_.append([self.sheet[self.headers[0]][n], self.sheet[self.headers[3]][n]])

    def inser_data(self) -> None:
        self.connect_server()
        for item in self.list_:
            self.insert_statement(self.querys['insert_atado'], *item)
        self.disconnect_server(True)
    
    def exec_app(self, option):
        self.open_doc()
        self.fuse_code()
        self.inser_data()
if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = Run_Objs(sys.argv[1], connection_config2)
    else:
        pass
    #app.exec_app()

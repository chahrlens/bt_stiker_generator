#!/usr/bin/env python3
from IncludeLibs import *

DMAX = 1670911200.0
TOD = date.today()
STRTOD = TOD.strftime("%d/%m/%Y")
DTOD =  time.mktime(datetime.datetime.strptime(STRTOD, "%d/%m/%Y").timetuple())

class Control_Server:
    def __init__(self, connection_config_parser) -> None:
        self.connection_config_parser = connection_config_parser
        self.conexion = None
        self.cursor   = None

    def connect_server(self) -> None:
        if (self.conexion and self.cursor) != None:
            return True
        self.conexion  = connector.connect(**self.connection_config_parser)
        self.cursor    = self.conexion.cursor()
        print("Connecting to the server : < {0} >".format(self.connection_config_parser['host']))
        

    def disconnect_server(self, commit_ = False) -> None:
        if commit_:
            self.conexion.commit()
        self.cursor.close()
        self.conexion.close()
        self.conexion = None
        self.cursor   = None
        print("Closing Server connection: <{0}>".format(self.connection_config_parser['host']))

    def insert_statement(self, query, *args) -> None:
        self.cursor.execute(query.format(*args))


    def get_statement(self, query) -> list:
        self.cursor.execute(query)
        l = list(self.cursor.fetchall())
        return l

class Doc_Reader:
    def __init__(self, file_name = None) -> None:
        self.file_name = file_name
        self.headers   = []
        self.list_     = []
        self.sheet     = None
        self.xls       = None

    def open_doc(self):
        self.xls     = pd.ExcelFile(self.file_name)
        self.sheet   = self.xls.parse(0)
        self.headers = [e for e in self.sheet]

class Doc_Writer(Doc_Reader):
    def __init__(self, file_name=None) -> None:
        Doc_Reader.__init__(file_name)
    def star_doc(self):
        pass

class Store_DB_Elements:
    def __init__(self) -> None:
        self.laber_writer = LabelWriter("stick.html", default_stylesheets=("style.css",), items_per_page=24)
        self.cur_week = seek_week.WeekSeeker()
        self.record = []
        self.product  = 0
        self.cuantity = 1
        self.price    = 2
        self.code     = 3
        self.nut      = 4
        self.row      = 5

        self.orders = {}

        self.order_detail = {
                            }
    def make_stiker(self) -> None:
        #if DTOD >= DMAX:
        #    return
        self.show_order('make_stiker')
        for order in self.orders:
            for item_l in self.order_detail[order]:
                self.record.append(dict(order_num=order, client_name=self.orders[order], product_name=item_l[self.product], 
                                        product_cuantity=item_l[self.cuantity], product_price=item_l[self.price], 
                                        product_nut=item_l[self.nut], page_row = item_l[self.row] , week_num = self.cur_week.get_week()))
        t = input("\n\n\n\nIngrese nombre para el archivo: ")
        self.alter_page()
        #self.laber_writer.write_labels(self.record, target="/mnt/c/Users/Usuario/Desktop/"+t+"_.pdf")
        self.laber_writer.write_labels(self.record, target="_"+t+"_.pdf")
    def show_order(self, caller = '') -> dict:
        print("(POS)        [Orden],     [Cliente],          [Producto],          [Cantidad],        [Precio],       [Tuerca],      [Row]")
        for order in self.orders:
            print(caller+"---"+order)
            for n, items in enumerate(self.order_detail[order]):
                print(f"<{n+1}>        [{order}], [{self.orders[order]}], [{items[self.product]}], [{items[self.cuantity]}], [{items[self.price]}], [{items[self.nut]}], [{items[self.row]}]")
    
    'APPEND ORDER ADN CUSTOMER NAME IN SELF.ORDERS{}'
    def insert_order(self,order='', client='') -> None:
        if order in self.orders:
            return
        self.orders[order] = client

    'APPEND ORDER ADN CUSTOMER NAME IN SELF.ORDERS_DETAIL{}'
    def insert_order_detail(self, order, *args) -> list:
        if order in self.order_detail:
            for item in args:
                self.order_detail[order].append(item)
            return
        self.order_detail[order] = [l for l in args]


    def alter_page(self):
        y = input("n\n\n\nCambiar a hoja horizontal Y | N:  ")
        if y.lower() == 'y':
            self.laber_writer = LabelWriter("stick.html", default_stylesheets=("style.css", 'ext_style.css',),  items_per_page=27)
        return
    'DELETE ANY ORDER AND CUSTOMER AND ORDER DETAILT FROM SELF.ORDERS AND SELF.ORDER_DETAIL'
    def delete_order(self, order='') -> None:
        if order in self.orders:
            del self.order_detail[order]
            del self.orders[order]
    def delete_any_item(self, order, index) -> None:
        if order in self.orders:
            del self.order_detail[order][index]


class Run_Objs(Doc_Reader, Control_Server, Store_DB_Elements):

    def __init__(self, file_name_ = None, conexion_config_parser_ = None) -> None:
        self.integers = INTEGERS()
        Doc_Reader.__init__(self, file_name =file_name_)
        Control_Server.__init__(self, connection_config_parser=conexion_config_parser_)
        Store_DB_Elements.__init__(self)
        self.label_writer_f = 'Pedido_{0}_template.html'
        self.label_writer = None
        self.querys = {'insert_atado' : "INSERT INTO productosatados (idprimary, idsecundary) VALUES ({0},{1});",
                       'get_cotizaci' : "SELECT CONCAT(VN.serie, {0}) AS N, CL.nombre AS Cliente, PR.descripcion AS Producto, DT.cantidad, DT.precio, PR.idproducto, '---'  FROM detallecotizacion AS DT INNER JOIN cotizaciones AS CT ON DT.idcotizacion = CT.idcotizacion INNER JOIN clientes AS CL ON CT.idcliente = CL.idcliente INNER JOIN documentos AS DOC ON CT.iddocumento = DOC.iddocumento INNER JOIN productos AS PR ON DT.idproducto = PR.idproducto INNER JOIN vendedorserie AS VN ON CT.idvendedor = VN.idvendedor WHERE CT.numero = {1};",
                       'get_pair'     : "SELECT NULL AS Result1, NULL AS Result2 FROM productosatados WHERE NOT EXISTS(SELECT idsecundary, impar FROM productosatados WHERE idprimary = {0}) UNION SELECT idsecundary, impar FROM productosatados WHERE idprimary = {0};"
                       }

    def add_orders(self) -> None:
        self.connect_server()
        while 1:
            l = []
            #order_n = input("Ingrese Numero Orden: ")
            order_n = self.integers.get_int_wmsg("Ingrese Numero Orden: ")
            if order_n == 0:
                self.show_order('add_orders')
                self.find_pair()
                self.make_stiker()
                return
            #cot_ = int(input("Ingrese Correlativo: "))
            cot_ = self.integers.get_int_wmsg("Ingrese Correlativo: ")
            for i in range (30): print('')
            
            #"COMPROBANDO QUE NO HAYA DATOS INVALIDOS"
            if not cot_: return print("Numero invalido"), self.add_orders()

            #"LLAMADA AL SERVIDOS A OBTENER DATOS DE LA COTIZACION"
            data = self.get_statement(self.querys['get_cotizaci'].format(order_n, cot_))
            if len(data) < 1: return print("Numero invalido"), self.add_orders()

            #"INSERT DE ENCABEZADO ARRAY ORDERS == (SERIE 'A' o 'B' Y 'NOMBRE CLIENTE')"
            self.insert_order(data[0][0],data[0][1])
            
            #"INSERT DE DETALLES EN ARRAY ORDER DETAILL == (nombre producto, cantidad , precio "campo vacio para tuerca " numero de linea)"
            for i, item in enumerate(data):
                l.append(list(item[2:7])+[f"L.:{i+1}"])
            self.insert_order_detail(data[0][0], *l)

    def add_any_order(self) ->None:
        self.connect_server()
        l = []
        order_n = self.integers.get_int_wmsg("Ingrese Numero Orden: ")
        if not order_n: return
        cot = self.integers.get_int_wmsg("Ingrese Correlativo: ")

        data = self.get_statement(self.querys["get_cotizaci"].format(order_n, cot))
        if len(data) < 1: return print("Numero invalido"), self.add_orders()
        order_n = data[0][0]
        self.insert_order(order_n, data[0][1])
        for i, item in enumerate(data):
            l.append(list(item[2:7])+[f"L.:{i+1}"])
        self.insert_order_detail(order_n, *l)
        self.find_pair()
        self.show_order("Any_order")

        opt = input("\n\n\nSelecionar Rango (R), Eliminacion selectiva (E): ")
        if opt.upper() == "R":
            i = self.integers.get_int_wmsg("Rango Inicio: ")
            #i = int(input("Rango Inicio: "))
            f = self.integers.get_int_wmsg("Rango Fin: ")
            #f = int(input("Rango Fin: "))
            self.order_detail[order_n] = self.order_detail[order_n][i-1:f]
            self.show_order()
            self.make_stiker()
        elif opt.upper() == "E":
            #i = int(input("Eliminacion selectiva ingrese pos: "))
            i = self.integers.get_int_wmsg("Eliminacion selectiva ingrese pos: ")
            while i != 0:
                self.delete_any_item(order_n, i-1)
                self.show_order()
                
                i = self.integers.get_int_wmsg("Eliminacion selectiva ingrese pos: ")
                #i = int(input("Eliminacion selectiva ingrese pos: "))
                
            self.make_stiker()
                
            

    def fuse_code(self) -> None:
        for n, x in enumerate(self.sheet[self.headers[0]]):
            self.list_.append([self.sheet[self.headers[0]][n], self.sheet[self.headers[3]][n]])

    def inser_data(self) -> None:
        self.connect_server()
        for item in self.list_:
            self.insert_statement(self.querys['insert_atado'], *item)
        self.disconnect_server(True)

    def match_pair(self, result, next):
        for val in result:
            if val[0] == next:
                print(f"Debug => val => {val}")
                return val
        return (None, None)

    def find_pair(self) ->None:
        code_product_pair = None
        is_pair           = None
        for order in self.orders:
            for n, order_d in enumerate(self.order_detail[order]):
                detail_legth = len(self.order_detail[order])
                if order_d[self.code] == 21:
                    del self.order_detail[order][n]
                    continue
                #"Get ID NUTS "
                print(f"Debug =>\n{order_d}")
                data = self.get_statement(
                    self.querys['get_pair'].format(order_d[self.code])
                    )
                
                #"match with current data nuts and next item if not data or case end of array 'order_detail', vars are [None, None] "
                code_product_pair, is_pair = self.match_pair(

                    data, self.order_detail[order][n+1][self.code]

                    ) if n+1 < detail_legth else [None, None]

                maxl = detail_legth -1

                if code_product_pair and n < maxl:
                    if (code_product_pair == self.order_detail[order][n+1][self.code] 
                        and (order_d[self.cuantity] == self.order_detail[order][n+1][self.cuantity]) or is_pair):
                        
                        if not is_pair:
                            self.order_detail[order][n][self.price] = (
                                self.order_detail[order][n][self.price]
                                +
                                self.order_detail[order][n+1][self.price]
                                )
                        else:
                            self.order_detail[order][n][self.cuantity] = (
                                self.order_detail[order][n][self.cuantity]
                                +
                                self.order_detail[order][n+1][self.cuantity]
                                )

                        self.order_detail[order][n][self.nut] = 'Incluye Tuerca'
                        self.order_detail[order][n][self.row] += ', ' + self.order_detail[order][n+1][self.row][3:]
                        del self.order_detail[order][n+1]
                self.order_detail[order][n][self.price] = round(self.order_detail[order][n][self.price] ,2)
    
    def exec_app(self):
        self.open_doc()
        self.fuse_code()
        self.inser_data()
        
if __name__ == "__main__":
    #Get Server Settings
    sql_settings = SQLSettings()
    connection_config = sql_settings.connection_conf

    if len(sys.argv) > 1:
        app = Run_Objs(sys.argv[1], connection_config)
        app.exec_app()
    else:
        ap = Run_Objs('', connection_config)    
        opt = input("Selectivo o Multiple? (S), (M): ")

        if opt.upper() == "S": 
            ap.add_any_order()
        else:
            ap.add_orders()
    

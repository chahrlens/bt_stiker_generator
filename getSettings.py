import configparser
class SQLSettings:
    def __init__(self):
        self.file_name = "config.con"
        self.parser = configparser.ConfigParser()
        self.default = 'MYSQLCON'
        self.connection_conf = {
	                            'host'    	 : 'localhost',
	                            'database'	 : 'test',
	                            'user'    	 : 'user',
	                            'password'	 : 'password',
	                            'auth_plugin': 'mysql_native_password'}
        try:
            self.get_file()
        except:
            self.make_file()
            self.get_file()

    def make_file(self):
        self.parser[self.default] = self.connection_conf
        with open(self.file_name, 'w') as configfile:
            self.parser.write(configfile)

    
    def get_file(self):
        self.parser.read(self.file_name)
        self.connection_conf['host']        = self.parser[self.default]['host']
        self.connection_conf['database']    = self.parser[self.default]['database']
        self.connection_conf['user']        = self.parser[self.default]['user']
        self.connection_conf['password']    = self.parser[self.default]['password']
        self.connection_conf['auth_plugin'] = self.parser[self.default]['auth_plugin']
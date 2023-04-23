import sqlite3
import hashlib
import random
import string
import datetime
class DBSQlite:
    def __init__(self):
        self.conn = sqlite3.connect('spacial_exploration.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (usuario TEXT PRIMARY KEY UNIQUE NOT NULL,
                  hashpassword TEXT NOT NULL);''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS mission (mission_name TEXT UNIQUE NOT NULL, identificator TEXT PRIMARY KEY UNIQUE);''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS machine
                         (machine_name TEXT PRIMARY KEY UNIQUE NOT NULL,
                          ip TEXT NOT NULL, port1 INTEGER NOT NULL, port2 INTEGER NOT NULL, mission TEXT, owner TEXT,
                           FOREIGN KEY(owner) REFERENCES users(usuario), FOREIGN KEY(mission) REFERENCES mission(identificador));''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS portmap (id_map TEXT PRIMARY KEY, type TEXT NOT NULL, port TEXT NOT NULL, io BOOLEAN NOT NULL,micro TEXT,FOREIGN KEY(micro) REFERENCES machine(machine_name));''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS sensores (id_sample TEXT PRIMARY KEY, sensor_name TEXT NOT NULL, datetime_medition TEXT NOT NULL, categorie_sensor TEXT NOT NULL, value TEXT NOT NULL,micro TEXT,FOREIGN KEY(micro) REFERENCES machine(machine_name));''')



    def fechar(self):
        self.conn.commit()
        self.conn.close()

    def command(self,command):
        try:
            self.conn.execute(command)
            self.fechar()
            return True
        except:
            return False

    def autenticar(self,usr,hashpassword):
        try:
            command = 'SELECT * FROM USERS WHERE usuario="{}"'.format(usr)
            retorno = self.conn.execute(command).fetchall()
            print(retorno)
            comparation = (retorno[0][1])
            if hashpassword == comparation:
                return True
            else:
                return False
        except:
            return False

    def query(self,comando):
        return self.conn.execute(comando).fetchall()
class FirstLayerProtection:
    def __init__(self):
        self.sqlite = DBSQlite()

    def _command(self,command):
        a = self.sqlite.command(command)
        return a


    def _authentication(self,usr,hashpassword):
        aut2 = self.sqlite.autenticar(usr,hashpassword)
        if aut2 == True:
            return True
        else:
            return False
    def usrMethod(self,**kwargs):
        user = kwargs['user']
        hashpassword = kwargs['hashpassword']
        if kwargs['command'] == "insert":
            try:
                command = 'INSERT INTO users VALUES ("{}","{}");'.format(user,hashpassword)
                a = self._command(command)
                return a
            except:
                return False
        elif kwargs['command'] == "update":
            new_username = kwargs['new_username']
            try:
                new_hashpassword = kwargs['new_hashpassoword']
                command = 'UPDATE users SET usuario = "{}",hashpassword = "{}" WHERE usuario ="{}";'.format(new_username,new_hashpassword,user)
                self._command(command)
            except:
                command = 'UPDATE users SET usuario = "{}" WHERE usuario="{}";'.format(new_username,user)
                self._command(command)

        elif kwargs['command'] == "delete":
            command = 'DELETE FROM users WHERE usuario = "{}";'.format(user)
            self._command(command)


    def login(self,usr,hashpassword):
        a = self._authentication(usr,hashpassword)
        return a
    def query(self,comando):
        query = self.sqlite.query(comando)
        return query
    def maquinas(self,**kwargs):
        if kwargs['command'] == "insert":
            machine_name = kwargs['machine_name']
            ip = kwargs['ip']
            portsocks1 = kwargs['portsocks1']
            portsocks2 = kwargs['portsocks2']
            mission = kwargs['mission']
            owner = kwargs['owner']
            command = 'INSERT INTO machine VALUES ("{}","{}","{}","{}","{}","{}");'.format(machine_name, ip, portsocks1,portsocks2, mission, owner)
            self._command(command)
        elif kwargs['command'] == "update":
            machine_name = kwargs['machine_name']
            what_edit = kwargs['what_edit']
            new_value = kwargs['new_value']
            command = 'UPDATE machine SET "{}" = "{}" WHERE machine_name ="{}";'.format(what_edit,new_value,machine_name)
            self._command(command)
        elif kwargs['command'] == "delete":
            machine_name = kwargs['machine_name']
            command = 'DELETE FROM machine WHERE machine_name = "{}";'.format(machine_name)
            self._command(command)
    def missoes_list(self):
        command = 'SELECT * FROM mission'
        return self.query(command)
    def minhas_maquinas(self,usr):
        command = '''SELECT * FROM machine JOIN users ON users.usuario = machine.owner WHERE users.usuario = '{}';'''.format(usr)
        return self.query(command)

    def port_map(self,**kwargs):
        if kwargs['command'] == 'insert':
            id_map = str(kwargs['id_map'])
            port = str(kwargs['port'])
            io = str(kwargs['io'])
            micro = str(kwargs['micro'])
            type = str(kwargs['type'])
            test1 = self.query('SELECT * FROM portmap WHERE micro="{}";'.format(micro))
            try:
                for i in test1:
                    for j in i:
                        if port in j:
                            return False
            except:
                pass
            command = 'INSERT INTO portmap VALUES ("{}","{}","{}","{}","{}");'.format(id_map,type,port,io,micro)
            self._command(command)
        elif kwargs['command'] == 'update':
            id_map = kwargs['id_map']
            what_edit = kwargs['what_edit']
            new_value = kwargs['new_value']
            command = 'UPDATE portmap SET "{}" = "{}" WHERE id_map ="{}";'.format(what_edit, new_value,id_map)
            self._command(command)
        elif kwargs['command'] == 'delete':
            id_map = kwargs['id_map']
            command = 'DELETE FROM portmap WHERE id_map = "{}";'.format(id_map)
            self._command(command)
    ##daqui pra cima tá ok!
    def missao(self,**kwargs):
        if kwargs['command'] == "insert":
            random_str = ''
            random_l = range(random.randint(8, 12))
            elements = string.ascii_letters
            list_range = len(elements) - 1
            for i in random_l:
                position = random.randint(0, list_range)
                random_str += elements[position]
            mission_name = kwargs['mission_name']
            command = 'INSERT INTO mission VALUES ("{}","{}");'.format(random_str,mission_name)
            comando = self._command(command)
            return comando
        elif kwargs['command'] == "delete":
            identificator = kwargs['identificator']
            command = 'DELETE FROM mission WHERE identificator = "{}";'.format(identificator)
            comando = self._command(command)
            return comando

    def valueSensor(self,**kwargs):
        sensor_name = kwargs['sensor_name']
        date_time = datetime.datetime.now()
        categorie_sensor = kwargs['categorie_sensor']
        value = kwargs['value']
        micro = kwargs['micro']
        random_str = ''
        random_l = range(random.randint(20, 35))
        elements = string.ascii_letters
        list_range = len(elements) - 1
        for i in random_l:
            position = random.randint(0, list_range)
            random_str += elements[position]
        command = 'INSERT INTO sensores VALUES("{}","{}","{}","{}","{}","{}");'.format(random_str,sensor_name,date_time,categorie_sensor,value,micro)
        self._command(command)
    
    def returnValuesSensor(self,micro):
        command = '''SELECT * FROM sensores WHERE micro = '{}';'''.format(micro)
        return self.query(command)

class DataManipulation:
    def __init__(self):
        self.prompt = FirstLayerProtection()

    ##métodos de usuário:
    def loginUsr(self,usr,password):
        hashpassword = hashlib.sha256(password.encode()).hexdigest()
        a = self.prompt.login(usr,hashpassword)
        return a

    def addUsr(self,usr,password):
        hashpassword = hashlib.sha256(password.encode()).hexdigest()
        self.prompt.usrMethod(command="insert",user=usr,hashpassword=hashpassword)

    def editUsrName(self,usr,password,newUsername):
        hashpassword = hashlib.sha256(password.encode()).hexdigest()
        self.prompt.usrMethod(command="update",user=usr,hashpassword=hashpassword,new_username=newUsername)
    def editUsrPassword(self,usr,password,newpassword,newuser=None):
        hashpassword = hashlib.sha256(password.encode()).hexdigest()
        hashnewpassword = hashlib.sha256(newpassword.encode()).hexdigest()
        if newuser == None:
            self.prompt.usrMethod(command="update",user=usr,hashpassword=hashpassword,new_hashpassoword=hashnewpassword)
        else:
            self.prompt.usrMethod(command="update",user=usr,hashpassword=hashpassword,new_hashpassoword=hashnewpassword,new_username=newuser)

    def removeUsr(self,usr,password):
        if self.loginUsr(usr,password) == True:
            hashpassword = hashlib.sha256(password.encode()).hexdigest()
            self.prompt.usrMethod(command="delete",user=usr,hashpassword=hashpassword)
            return True
        else:
            return False


    def adicionarMissao(self,nome_missao):
        a = self.prompt.missao(command="insert",mission_name=nome_missao)
        return a

    def removerMissao(self,mission_code):
        self.prompt.missao(command="delete",identificator=mission_code)

    def adicionarMaquina(self,machine_name,ip, port_socket1,port_socket2, mission,owner):
       a = self.prompt.maquinas(command="insert",machine_name=machine_name,ip=ip,portsocks1=port_socket1,portsocks2=port_socket2,mission=mission,owner=owner)
       return a
    def editarMaquina(self,machine_name,what_edit,new_value):
        self.prompt.maquinas(command="update",machine_name=machine_name,what_edit=what_edit,new_value=new_value)


    def removerMaquina(self,machine_name):
        self.prompt.maquinas(command="delete",machine_name=machine_name)

    def adicionarPortMap(self,id_map,port,io,micro,type):
        self.prompt.port_map(command="insert",id_map=id_map,port=port,io=io,micro=micro,type=type)

    def editarPortMap(self,what_edit,new_value,id_map):
        self.prompt.port_map(command="update",what_edit=what_edit,new_value=new_value,id_map=id_map)

    def removerPortMap(self,id_map):
        self.prompt.port_map(command="delete",id_map=id_map)


    def sensor(self,sensor_name,categorie_sensor,value,micro):
        self.prompt.valueSensor(sensor_name=sensor_name,categorie_sensor=categorie_sensor,value=value,micro=micro)

    def retornSensor(self,micro):
        return self.prompt.returnValuesSensor(micro)
    def minhas_maquinas(self,usr):
        return self.prompt.minhas_maquinas(usr)

    def missoes(self):
        return self.prompt.missoes_list()
    def portas(self,micro):
        return self.prompt.query('SELECT * FROM portmap WHERE micro="{}";'.format(micro))



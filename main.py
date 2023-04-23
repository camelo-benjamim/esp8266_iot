import time
import socket
import json
from controller import Controler
from matplotlib.dates import DateFormatter
from local_db import DataManipulation
controller = Controler()
from sockets import Socket1, Socket2
s = True
import datetime
import pandas as pd
import statistics as estatistica
import matplotlib.pyplot as plt
import os
while s == True:
    if controller.menu == '':
        print(" ---------------- HOVER JÄGER ---------------------- ")
        print(" MENU PRINCIPAL: ")
        print(" 1 - USUÁRIOS ")
        print(" 2 - MÁQUINAS ")
        print(" 3 - ADICIONAR MISSÕES ")
        print(" 4 - ANÁLISE DE DADOS ")
        choose = False
    if controller.menu == '':
        while controller.menu == '':
            try:
                x = int(input(" Escolha entre os Menus: "))
                controller.menu = x
                if x >=1 and x<= 6:
                    choose = True
            except:
                print(" Tente novamente! ")
    if controller.menu == 1:
        print(" MENU DE USUÁRIOS:")
        if controller.usuario == '':
            print(" 1 - CADASTRAR ")
            print(" 2 - FAZER LOGIN ")
            c = False
            while c == False:
                try:
                    w = int(input(" Escolha: "))
                    if w == 1 or w == 2:
                        c = True
                        controller.menu = ''
                except:
                    pass
            if w == 1:
                while controller.usuario == '':
                    try:
                        print(" MENU DE CADASTRO: ")
                        username = input("Digite seu nome de usuário: ")
                        password = input(" Digite sua senha: ")
                        d = DataManipulation()
                        d.addUsr(username,password)
                        time.sleep(1)
                        a = True
                        if a == True:
                            controller.usuario = username
                            controller.menu = ''
                    except:
                        pass

            else:
                while controller.usuario == '':
                    username = input(" Digite seu nome de usuário: ")
                    password = input(" Digite sua senha: ")
                    mkl = DataManipulation()
                    a = mkl.loginUsr(username,password)
                    if a == True:
                        controller.usuario = username
                        controller.menu = ''


        else:
            try:
                os.system('clear')
            except:
                os.system('cls')

            print(" MENU DE USUÁRIO: ")
            print(" 1 - LOGOUT ")
            print(" 2 - EDITAR ")
            print(" 3 - APAGAR ")
            q = False
            while q == False:
                try:
                    n = int(input(" Escolha: "))
                    if n >= 1 and n <= 3:
                        q = True
                    else:
                        print(" Tente novamente! ")
                except:
                    pass
            
            if n == 1:
                controller.usuario = ''
                controller.menu = ''
            elif n == 2:
                print(" Digite 1 para alterar username: ")
                print(" Digite 2 para alterar senha: ")
                o = False
                while o == False:
                    k = int(input(" Escolha: "))
                    if k == 1 or k == 2 or k == 3:
                        o = True
                if k == 1:
                    p = False
                    while p == False:
                        try:
                            username = input(" Digite seu nome de usuário: ")
                            password = input(" Digite sua senha: ")
                            newusername = input(" Digite seu novo nome de usuário: ")
                            pkl = DataManipulation()
                            a = pkl.editUsrName(username,password,newusername)
                            p = True
                        except:
                            print(" Tente novamente: ")
                else:
                    p = False
                    while p == False:
                        username = input(" Digite seu nome de usuário: ")
                        password = input(" Digite sua senha: ")
                        newpassword = input(" Digite sua nova senha de usuário : ")
                        bw = DataManipulation()
                        bw.editUsrPassword(username,password,newpassword)

            elif n == 3:
                print(" Essa tela requer atenção, caso ocorra um erro seu usuário não será deleteado")
                print(" Digite os dados e verifique antes de teclar ENTER: ")
                username = input(" Digite seu username: ")
                password = input(" Digite sua senha: ")
                kul = DataManipulation()
                kul.removeUsr(username,password)
                controller.menu = ''

    elif controller.menu == 2:
        if not controller.usuario == '':
            try:
                os.system('clear')
            except:
                os.system('cls')
            escolhido = False
            while escolhido == False:
                print(" --------- MENU DE MÁQUINAS ------")
                print(" 1 - ESCOLHER MÁQUINA")
                print(" 2 - ADICIONAR MÁQUINAS ")
                print(" 3 - EDITAR MÁQUINAS ")
                print(" 4 - REMOVER MÁQUINAS")
                escolher = int(input(" Escolha: "))
                if escolher >= 1 and escolher <= 4:
                    if escolher == 1:
                        print(" ESCOLHENDO MÁQUINA: ")
                        print(" LISTA DE MÁQUINAS: ")
                        f = DataManipulation()
                        maquinas = f.minhas_maquinas(controller.usuario)
                        if len(maquinas) == 0:
                            print(" Você não adicionou máquinas, escolha adicionar máquinas ")
                        else:
                            contador = 0 
                            for i in maquinas: 
                                contador += 1
                                print(" {} - {}".format(str(contador),i[0]))
                            c = False
                            while c == False:
                                y = int(input(" Escolha: "))
                                controller.maquina = maquinas[y-1]
                                c = True
                                escolhido = True
                                controller.menu = "o"
                    
                    elif escolher == 2:
                        print(" ADICIONANDO MÁQUINAS: ")
                        print("")
                        print(" ESCOLHA A MISSÃO: ")
                        dm = DataManipulation()
                        missoes = dm.missoes()
                        contador = 0
                        for i in missoes:
                            contador += 1
                            print("{} - {}".format(str(contador),i[1]))
                        j = False
                        contador = 0
                        while j == False:
                            try:
                                x = int(input(" Escolha: "))
                                x = x - 1
                                missao = missoes[x][1]
                                usr = controller.usuario
                                nome = input(" Digite um nome para o micrcontrolador: ")
                                ip = input(" Digite o IP do microcontrolador: ")
                                port1 = int(input(" Digite a porta do primeiro socket: "))
                                port2 = int(input(" Digite a porta do segundo socket:  "))
                                dm.adicionarMaquina(nome,ip,port1,port2,missao,usr)
                                controller.maquina = nome
                                j = True
                                escolhido = True
                                controller.menu = 'o'
                            except Exception as erro:
                                print(erro)
                                print(" Tente novamente")


                    elif escolher == 3:
                        print(" EDIÇÃO DE MÁQUINAS ")
                        print("")
                        dn = DataManipulation()
                        maquinas = dn.minhas_maquinas(controller.usuario)
                        contador = 1
                        for i in maquinas:
                            print("{} - {}".format(str(contador),i))
                            contador += 1
                        contador = 0
                        f = False
                        while f == False:
                            x = int(input(" Escolha: "))
                            x = x - 1
                            maquina = maquinas[x][0]
                            print(" O que editar? ")
                            print(' 1 - IP ')
                            print(' 2 - port socks1 ')
                            print(' 3 - port socks2')
                            p = int(input(" Escolha: "))
                            if p == 1 or p == 2 or p ==3:
                                try:
                                    if p == 1:
                                        new_value = input(" Digite o novo valor: ")
                                        dn.editarMaquina(maquina,'ip',new_value)
                                    elif p == 2:
                                        portsocks1 = input(" Digite o novo valor: ")
                                        dn.editarMaquina(maquina,'´port1',portsocks1)
                                    else:
                                        portsocks2 = input(" Digite o novo valor: ")
                                        dn.editarMaquina(maquina,'´port2',portsocks2)
                                    
                                    f = True
                                    controller.menu = ''
                                    escolhido = True
                                except:
                                    print(" Tente novamente! ")
                    
                    elif escolher == 4:
                        print(" DELETAR MÁQUINAS ")
                        print("")
                        dkl = DataManipulation()
                        maquinas = dkl.minhas_maquinas(controller.usuario)
                        contador = 1
                        for i in maquinas:
                            print("{} - {}".format(str(contador),i))
                            contador += 1
                        contador = 0
                        f = False
                        while f == False:
                            try:
                                x = int(input(" Escolha: "))
                                x = x - 1
                                maquina = maquinas[x][0]
                                dkl.removerMaquina(maquina)
                                f = True
                                controller.menu = ''
                                escolhido = True
                            except:
                                print(" Tente novamente!")

        else:
            print(" Faça login para utilizar! ")
    elif controller.menu == 3:
        try:
            os.system('clear')
        except:
            os.system('cls')
        print(" ------- MENU DE MISSÃO -------")
        print(" ")
        print(" ADICIONAR MISSÃO: ")
        try:
            djk = DataManipulation()
            nome = input(" Digite o nome da missão que deseja adicionar: ")
            djk.adicionarMissao(nome)
            controller.menu = ''
        except:
            print(' Tente novamente! ')

    elif controller.menu == 'o':
        print(" Iniciando operação: ")
        print(" 1 - CONTROLE ")
        print(" 2 - SENSORES E ATUADORES ")
        jl = False
        while jl == False:
            x = int(input(" Escolha: "))
            if x == 1 or x == 2:
                option = x
                jl = True
        if x == 1:
            print(" INICIANDO... ")
            valid_ans = False
            first = True
            while valid_ans == False:
                if first == True:
                    a = input(" Deseja fazer alterações no Io do microcontrolador? (s/n) ")
                    first = False
                if (a == "s"):
                    do = DataManipulation()
                    ports = do.portas(controller.maquina[0])
                    machine = controller.maquina
                    ip = machine[1]
                    port1 = machine[2]
                    for u in ports:
                        try:
                            tipo = u[1]
                            port = u[2]
                            io = u[3]
                            a = Socket1(ip,port1,port,io,0,tipo)
                            print(" alteração concluída")
                            time.sleep(1)
                            
                        except Exception as erro:
                            print('erro')
                            print(erro)

                print(" 1 - RECOLHER DADOS: ")
                print(" 2 - ALTERAÇÃO NOS ATUADORES: ")
                print(" 3 - MENU PRINCIPAL")
                try:
                    x = int(input(" Escolha: "))
                except:
                    print(" Tente novamente! ")
                if x == 1:
                    print(" Defina o tempo da execução em segundos: ")
                    c = False
                    while c == False:
                        tempo = int(input(" t/s: "))
                        c = True
                    hora_atual = datetime.datetime.now()
                    hora_parar = hora_atual + datetime.timedelta(seconds=tempo)
                    djlk = DataManipulation()
                    print(" -------- RESULTADO DAS ANÁLISES --------")
                    while not datetime.datetime.now() > hora_parar:
                        machine_p = controller.maquina
                        portas = djlk.portas(machine_p[0])
                        list_p = []
                        for i in portas:
                            if i[3] == 'INPUT':
                                list_p.append(i)
                        print("--------------------------------------")
                        print(' Hora da leitura: {}'.format(str(datetime.datetime.now())))
                        print(" ")
                        for i in list_p:
                            try:
                                porta = i[2]
                                s  = Socket2(machine_p[1],machine_p[3],porta)
                                djlkj = DataManipulation()
                                djlkj.sensor(str(i[0]),str(i[1]),str(s.resposta.decode('utf-8')),machine[0])
                            except:
                                pass
                            print(" {} - {}".format(str(i[0]),str(s.resposta.decode('utf-8'))))
                        print(" LEITURA FINALIZADA")
                        print("")
                        print("")
                        list_p = []
                elif x == 3:
                    valid_ans = True
                    controller.menu = ''
                elif x == 2:
                    nome  = input(" Nome atuador: ")
                    porta = ''
                    d = DataManipulation()
                    e = d.portas(controller.maquina[0])
                    for i in e:
                        if nome == i[0]:
                            porta = i[2]
                            io = i[3]
                            
                    print("Alteração nos atuadores: ")
                    atuador_porta = porta
                    valor = int(input("Valor: "))
                    if ('D' in atuador_porta):
                        tipo = 'DIGITAL'
                    else:
                        tipo = 'ANALOG'
                    machine = controller.maquina
                    ip = machine[1]
                    port1 = machine[2]
                    l = Socket1(ip,port1,atuador_porta,io,valor,tipo)

        elif x == 2:
            print(" CONFIGURANDO SENSORES E ATUADORES")
            print("")
            print(" LISTANDO CONFIRAÇÃO ATUAL DO PORTMAP: ")
            print(" ")
            print(" ")
            u = DataManipulation()
            portmap = u.portas(controller.maquina[0])
            contador = 0
            for i in portmap:
                contador += 1
                print('{} - {} - {}'.format(str(contador),str(i[2]),str(i[3])))
            contador = 0
            print(" ")
            print(" PREPARANDO PARA ATUALIZAÇÃO NO BANCO DE DADOS: ")
            time.sleep(1)
            print(" ESCOLHA A OPERAÇÃO QUE DESEJA REALIZAR: ")
            print("")
            m = False
            while m == False:
                print(" 1 - para adicionar ")
                print(" 2 - para editar ")
                print(" 3 - para remover ")
                x = int(input(" Escolha: "))
                if x == 1 or x == 2 or x == 3:
                    if x == 1:
                        try:
                            nome = input("Digite o nome: ")
                            porta = input(" Digite a porta: ")
                            io = input(" INPUT/OUTPUT: ")
                            tipo = input(" DIGITAL/ANALOG: ")
                            k= DataManipulation()
                            k.adicionarPortMap(nome,porta,io,controller.maquina[0],tipo)
                            m = True
                        except Exception as erro:
                            print(" tente novamente")
                            print(erro)
                    elif x == 2:
                        lk = DataManipulation()
                        portmap = lk.portas(controller.maquina[0])
                        contador = 0
                        for i in portmap:
                            contador += 1
                            print('{} - {} - {}'.format(str(contador),str(i[2]),str(i[3])))
                        contador = 0
                        try:
                            escolha = int(input(" Escolha: "))
                            escolha = escolha - 1
                            l = portmap[escolha]
                            input(" O que editar?")
                            print(" 1 - TIPO")
                            print(" 2 - PORTA")
                            print(" 3 - IO")
                            what_edit = int(input("Escolha: "))
                            if what_edit == 1:
                                what_edit="type"
                            elif what_edit == 2:
                                what_edit = "port"
                            elif what_edit == 3:
                                what_edit = "io"
                            new_value = input(" Digite o novo valor: ")
                            lk.editarPortMap(what_edit,new_value,l[0])
                            m = True
                        except:
                            print(" tente novamente! ")
                        
                    elif x == 3:
                        j = DataManipulation()
                        print(" SELECIONE DA LISTA QUAL GOSTARIA DE REMOVER: ")
                        print(" printando controller")
                        portmap = j.portas(controller.maquina[0])
                        contador = 0
                        for i in portmap:
                            contador += 1
                            print('{} - {} - {}'.format(str(contador),str(i[2]),str(i[3])))
                        contador = 0
                        try:
                            x = int(input(" Escolha: "))
                            x = x - 1
                            pm = portmap[x][0]
                            print(" pritando portmap: ")
                            print(pm)
                            j.removerPortMap(pm)
                            m = True
                        except:
                            print(" tente novamente! ")

    

    elif controller.menu == 4:
        try:
            os.system('clear')
        except:
            os.system('cls')
        print(" ANÁLISE DE DADOS: ")
        print(" 1 - VISUALIZAR ANÁLISE DOS DADOS: ")
        print(" 2 - VISUALIZAR GRÁFICOS: ")
        print(" 3 - EXPORTAR CSV ")

        escolher = False
        while escolher == False:
            x = int(input("Escolha: "))
            if x == 1 or x == 2 or x == 3:
                if x == 3:
                    controller.menu = "csv"
                escolher = True
                if x == 1:
                    controller.menu ='analisys'
                
                if x == 2:
                    controller.menu = "graphics"
    if controller.menu == "graphics":
        print(" PARA ESTA ANÁLISE SERÁ FEITO A LEITURA DO SENSOR ANALÓGICO DA ESP: ")
        print(" A ANÁLISE IRÁ OCERRER APENAS SE EXISTIR UM SENSOR ANALÓGICO NO DB ")
        print(" ")
        print(" Escolha qual microcontrolador você quer o relatório: ")
        lkl = DataManipulation()
        maquinas = lkl.minhas_maquinas(controller.usuario)
        contador = 0 
        for i in maquinas:
            contador  += 1
            print("{} - {}".format(str(contador),i[0]))
        contador = 0
        x = int(input("Escolha: "))
        x = x - 1
        maquina = maquinas[x][0]
        controller.maquina = maquina
        print("PEGANDO SENSORES ANALÓGICOS: ")
        print(" ")
        dfgl = DataManipulation().retornSensor(controller.maquina)
        analogicos = []
        for i in dfgl:
            if i[3] == "ANALOG":
                analogicos.append(i)
        t_res = []
        v_res = []
        for u in analogicos:
            p = t_medicao = u[2]
            t_res.append(p)
            w = v_medicao = u[4]
            v_res.append(w)

        t_res = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f') for d in t_res]

        # Plotar o gráfico de dispersão
        plt.scatter(t_res, v_res)

        # Configurar o eixo x para exibir as datas com minutos e segundos como rótulos
        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S.%f'))
        plt.gcf().autofmt_xdate()

        # Configurar os rótulos dos eixos
        plt.xlabel('Data (minutos e segundos)')
        plt.ylabel('Valor')
        plt.subplots_adjust(bottom=0.2, left=0.1)
        # Mostrar o gráfico
        plt.show()

        controller.menu = 4
    elif controller.menu == "analisys":
        print("INICIANDO ANALÍSE DOS DADOS: ")
        print("")
        print(" MODA, MÉDIA E MEDIANA DOS RESULTADOS: ")
        print(" Escolha qual microcontrolador você quer o relatório: ")
        lkl = DataManipulation()
        maquinas = lkl.minhas_maquinas(controller.usuario)
        contador = 0 
        for i in maquinas:
            contador  += 1
            print("{} - {}".format(str(contador),i[0]))
        contador = 0
        x = int(input("Escolha: "))
        x = x - 1
        maquina = maquinas[x][0]
        controller.maquina = maquina
        try:
            dados_por_sensor = {}
            dados = DataManipulation().retornSensor(controller.maquina)
            estruturados = []
            for i in dados:
                estruturar = []
                for j in i:
                    estruturar.append(j)
                estruturados.append(estruturar)
            print("meus dados: ")
            print(estruturados)
            controller.menu = 4
            sensores = []
            for f in estruturados:
                if not f[1] in sensores:
                    sensores.append(f[1])
            
            print(" ANALISANDO DADOS DE ACORDO COM OS SENSORES: ")
            for i in sensores:
                analise_atual = []
                for j in estruturados:
                    if j[1] == i:
                        try:
                            analise_atual.append(int(j[4]))
                        except:
                            pass
                print(" ")
                print(" RESULTADOS DOS DADOS VÁLIDOS : ")
                print(" ANÁLISE DO SENSOR {}".format(i))
                print("")
                media = estatistica.mean(analise_atual)
                mediana = estatistica.median(analise_atual)
                moda = estatistica.mode(analise_atual)

                print(" MÉDIA DOS RESULTADOS DO SENSOR: ")
                print(" " + str(media))
                print(" ")
                print(" MEDIANA DOS RESULTADOS DO SENSOR: ")
                print(" " + str(mediana))
                print("")
                print(" MODA DOS RESULTADOS DO SENSOR: ")
                print(" " + str(moda))
                print("")
                time.sleep(2)

        except Exception as erro:
            print(erro)
    elif controller.menu == "csv":
        print(" Escolha qual microcontrolador você quer o relatório: ")
        lkl = DataManipulation()
        maquinas = lkl.minhas_maquinas(controller.usuario)
        contador = 0 
        for i in maquinas:
            contador  += 1
            print("{} - {}".format(str(contador),i[0]))
        contador = 0
        x = int(input("Escolha: "))
        x = x - 1
        maquina = maquinas[x][0]
        controller.maquina = maquina
        try:
            leitura = DataManipulation().retornSensor(controller.maquina)
            ids = []
            nomes = []
            horarios = []
            valores = []
            for dado in leitura:
                id_amostra = dado[0]
                nome_sensor = dado[1]
                hora_medicao = dado[2]
                categoria_sensor = dado[3]
                valor = dado[4]
                ids.append(id_amostra)
                nomes.append(nome_sensor)
                horarios.append(hora_medicao)
                valores.append(valor)
            dados = {'Ids das amostras': ids,'Sensor': nome_sensor, 'Horários das amostras': hora_medicao, 'Categorias dos sensores': categoria_sensor,'Resultados': valores}
            df = pd.DataFrame(dados)
            df.to_excel('relatório {}.xlsx'.format(controller.maquina),sheet_name="Dados",index=True)
            print("Gerado com sucesso ")
            controller.menu = 4
            try:
                os.system('clear')
            except:
                os.system('cls')
        except Exception as erro:
            print(erro)
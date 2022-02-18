from fileinput import filename
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.tix import Tree

class Analizador:

    def __init__(self):
        self.texto = ""
        self.id_data = 1
        self.id_instr = 1
        self.data = dict()
        self.instr = dict()

    def Leer(self, extension):
        x = ""
        y= ""
        Tk().withdraw()
        try:
            filename = askopenfilename(title='Selecciona un archivo',
                                       filetypes=[('Archivos', f'*{extension}'),  # -> concatena -> *.data o *.lfp
                                                  ('All Files', '*')])
            #print(filename)
            with open(filename, encoding='utf-8') as infile:
                x = infile.read().strip()
            #print(str(x))
        except:
            print('Error, no se ha seleccionado ningun archivo')
            return

        x = x.upper() # -> MAYUSCULAS
        #x = x.lower()  # -> minusculas
        #print(str(x))

        com = False
        for letra in x:
            if letra != '\"':
                if(letra != " " and letra != "\n" and letra != "\t" or com):
                    y += letra
            elif not com:
                y += letra
                com = True
            else:
                y += letra
                com = False
        #print(y)
        self.texto = y

    def Analizar_Data(self):
        cadena = self.texto
        nombre = False
        anio = False
        par = 0
        datos = False

        nombre_n = ""
        anio_n = ""
        data = ""
        data_list = []

        cori = False
        cord = False
        caso = 0
        error = False

        for letra in cadena:
            if nombre == False:
                if letra != ':':
                    nombre_n += letra
                else:
                    nombre = True
            elif anio == False:
                if letra != "=":
                    anio_n += letra
                else:
                    anio = True
            elif letra == '(' and nombre == True and anio == True:
                    par += 1

            elif letra == ')' and nombre == True and anio == True and par == True:
                par += 1
                print("Archivo leido correctamente")
                break
            elif datos == False:
                if letra == '[':
                    cori = True
                elif letra == ']' and cori == True:
                    cord = True
                elif cori == True and cord == False:
                    if letra == "\"":
                        caso += 1
                    else:
                        data += letra
                elif letra == ";":
                    if cori == True and cord == True and caso == 2:
                        lista = data.split(',')
                        if len(lista) != 3:
                            error = True
                            print("Error, no se puede leer este archivo")
                            break
                        try:
                            lista[1] = float(lista[1])
                            lista[2] = float(lista[2])
                        except:
                            error = True
                            print("Error, no se puede leer este archivo")
                            break
                        data_list.append(lista)
                        print(lista)
                        data = ""
                        cari = False
                        cord = False
                        caso = 0
            else:
                error = True
                print("Error, no se puede leer este Archivo")
                break

        if not error:
            anio_n = int(anio_n)
            if anio_n != 0 and nombre_n != "" and data_list != [] and par == 2:
                self.data[self.id_data] = {'anio': anio_n, 'mes': nombre_n, 'productos': data_list}
                self.id_data += 1
            else:
                print("Error, no se puede leer este archivo")
            print(self.data)

    def Analizador_Instr(self):
        cadena = self.texto
        ini = cadena[0:2]
        a = len(cadena) -3 #El termino de la lista (numero de datos)
        b = len(cadena)
        fin = cadena[a:b]

        caso = 0
        entry = False

        aux = dict()

        if ini == '<¿' and fin == '"?>':
            cadena = self.texto
            ini = cadena[0:2]
            a = len(cadena) - 3  # El tamanio de la lista (numero de datos)
            b = len(cadena)
            fin = cadena[a:b]

            caso = 0
            entry = False

            aux = {}
            if ini == "<¿" and fin == '"?>':
                cadena = cadena[2:]
                cadena = cadena[:-2]
                cadena += "$"
                comando = ""
                nombre = ""

                for letra in cadena:
                    if letra != ":" and caso == 0:
                        comando += letra
                    elif letra == ":":
                        caso = 1
                    elif letra == '"':
                        if entry:
                            entry = False
                        else:
                            entry = True
                    elif entry == True:
                        nombre += letra
                    elif (letra == "," and caso == 1) or letra == "$":
                        if comando == 'NOMBRE':
                            aux[comando] = nombre  # {'nombre': "cambio1"}
                        elif comando == 'GRAFICA':
                            aux[comando] = nombre
                        elif comando == 'TITULO':
                            aux[comando] = nombre
                        elif comando == 'TITULOX':
                            aux[comando] = nombre
                        elif comando == 'TITULOY':
                            aux[comando] = nombre
                        else:
                            print("Error, no se reconoce este comando")
                            aux = {}
                            break
                        nombre = ""
                        comando = ""
                        caso = 0
                    else:
                        print("Error, no se puede leer este archivo")
                        aux = {}
                        break

                if 'NOMBRE' in aux and 'GRAFICA' in aux:
                    self.instr[self.id_instr] = aux
                    self.id_instr += 1
                    print(self.instr)
                else:
                    print("Error, no se puede almacenar esta informacion, faltan datos")

            else:
                print("Error, no se puede leer este archivo")

    def EjeX(self, id):
        ejex = []
        if id in self.data:
            for p in self.data[id]['productos']:
                ejex.append(p[0])
        return ejex

    def EjeY(self, id):
        ejey = []
        if id in self.data:
            for p in self.data[id]['productos']:
                total_p = p[1] * p[2]
                ejey.append(total_p)
        return ejey

    def getData(self):
        for dato in self.data:
            nombre = self.data[dato]['mes']+" "+":"+" "+str(self.data[dato]['anio'])
        return nombre

    def getInstr(self, id):
        if id in self.instr:
            return self.instr[id]
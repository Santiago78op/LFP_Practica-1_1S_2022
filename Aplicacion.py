#Flujo del programa
from Analizador import Analizador
from Graficador import Graficador
a = Analizador()

class Aplicacion:

    def __init__(self):
        self.app()

    def app(self) ->bool:
        while True:
            res = input('''
    1. Cargar Data
    2. Cargar Instrucciones
    3. Analizar
    4. Reportes
    5. Salir
    -> Selecciona una opcion: ''')
            #switch
            if res == '1':
                a.Leer('.data')
                a.Analizar_Data()
            elif res == '2':
                a.Leer('.lfp')
                a.Analizador_Instr()
            elif res == '3':
                titulo = a.getData()
                instr = a.getInstr(1)
                nombre = instr['NOMBRE']
                grafica = instr['GRAFICA']
                titulox = instr['TITULOX']
                tituloy = instr['TITULOY']
                ejex = a.EjeX(1)
                ejey = a.EjeY(1)
                c = Graficador(nombre, grafica, titulo, titulox, tituloy, ejex, ejey)
                c.Analizar()
            elif res == '4':
                pass
            elif res == '5':
                print("Asta pronto")
                return False
            else:
                print("Seleccione un opcionvalida")

b = Aplicacion()
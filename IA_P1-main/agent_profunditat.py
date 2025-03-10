import joc
import estat
from practica.joc import Accions

class Viatger(joc.Viatger):
    def __init__(self, *args, mida_taulell=None, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)
        self.mida_taulell = mida_taulell
        self.visitats = set()  # Conjunt de posicions visitades
        self.stack = []  # Pila per realitzar la cerca
        self.solucio = []  # Emmagatzemarà el camí trobat
        self.moviment_actual = 0  # Controlarà en quin pas esteim

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        nom_agent = self.nom
        posicio_actual = percepcio["AGENTS"][nom_agent]

        if self.solucio:
            if posicio_actual == percepcio["DESTI"]:
                return Accions.ESPERAR

            accio, direccio = self.solucio[self.moviment_actual]

            resultado_movimiento = self.hay_obstaculo(percepcio, posicio_actual, direccio)

            match resultado_movimiento:
                case Accions.MOURE:
                    self.moviment_actual += 1
                    percepcio["AGENTS"][nom_agent] = estat.calcula_nova_posicio(posicio_actual, direccio)
                    #print(f"Movido a {percepcio['AGENTS'][nom_agent]} en dirección {direccio}")
                    return Accions.MOURE, direccio

                case Accions.BOTAR:
                    self.moviment_actual += 1
                    percepcio["AGENTS"][nom_agent] = estat.calcula_nova_posicio(
                        estat.calcula_nova_posicio(posicio_actual, direccio), direccio)
                    print(f"Saltado a {percepcio['AGENTS'][nom_agent]} en dirección {direccio}")
                    return Accions.BOTAR, direccio

                case _:
                    self.moviment_actual += 1
                    return Accions.ESPERAR, direccio

        desti = percepcio["DESTI"]

        if desti == posicio_actual:
            return print("S'ha arribat al destí automàticament")

        estat_inicial = estat.EstatRobot(posicio_actual, mida_taulell=self.mida_taulell)
        self.stack.append(estat_inicial)

        while self.stack:
            estat_actual = self.stack.pop()

            if estat_actual.posicio in self.visitats:
                continue

            if estat_actual.es_meta(desti):
                print(f"Hem arribat al destí! {estat_actual.cami}")
                self.solucio = estat_actual.cami
                self.moviment_actual = 0
                return self.solucio[self.moviment_actual]

            self.visitats.add(estat_actual.posicio)

            fills = estat_actual.genera_fill(percepcio)

            for fill in fills:
                if fill.posicio not in self.visitats:
                    self.stack.append(fill)

        return Accions.ESPERAR

    def hay_obstaculo(self, percepcio, posicio_actual, direccio):
        nova_posicio = estat.calcula_nova_posicio(posicio_actual, direccio)

        # Verificar límites del tablero
        if not estat.posicio_dins_limits(nova_posicio, percepcio):
            return False

        # Verificar paredes
        if estat.paret_aqui(nova_posicio, percepcio):
            # Verificar si podemos saltar
            pos_salt = estat.calcula_nova_posicio(posicio_actual, direccio, botar=True)
            if estat.posicio_dins_limits(pos_salt, percepcio) and not estat.paret_aqui(pos_salt, percepcio):
                return Accions.BOTAR
            else:
                return Accions.ESPERAR
        else:
            return Accions.MOURE

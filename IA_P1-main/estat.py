from practica.joc import Accions
import joc

def calcula_nova_posicio(posicio_actual, direccio, botar=False):
    direccions = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "O": (-1, 0)
    }

    if botar:
        return posicio_actual[0] + 2 * direccions[direccio][0], posicio_actual[1] + 2 * direccions[direccio][1]
    else:
        return posicio_actual[0] + direccions[direccio][0], posicio_actual[1] + direccions[direccio][1]


def posicio_dins_limits(posicio, percepcio):
    x, y = posicio
    return 0 <= x < len(percepcio["TAULELL"][1]) and 0 <= y < len(percepcio["TAULELL"][0])


# Verifica si hi ha una paret a la nova posició
def paret_aqui(posicio, percepcio):
    return posicio in percepcio["PARETS"]


class EstatRobot:
    def __init__(self, posicio, mida_taulell=None):
        self.posicio = posicio  # Posició actual del robot
        self.cami = []  # Cami d'accions fins arribar aquí
        self.mida_taulell = mida_taulell


    def es_meta(self, desti):
        """ Verifica si hem arribat a la destinació """
        return self.posicio == desti

    def genera_fill(self, percepcio):
        """ Genera todos los estados hijos a partir del estado actual """

        for direccio in joc.Laberint.MOVS:
            nova_posicio = calcula_nova_posicio(self.posicio, direccio)

            if not posicio_dins_limits(nova_posicio, percepcio):
                continue

            if not paret_aqui(nova_posicio, percepcio):
                yield self.crear_nou_estat(nova_posicio, direccio, Accions.MOURE)
            else:
                nova_posicio_botar = calcula_nova_posicio(nova_posicio, direccio)
                if posicio_dins_limits(nova_posicio_botar, percepcio) and not paret_aqui(nova_posicio_botar, percepcio):
                    yield self.crear_nou_estat(nova_posicio_botar, direccio, Accions.BOTAR)

    def crear_nou_estat(self, nova_posicio, moviment, accio):
        """ Crea un nuevo estado a partir de una nueva posición y movimiento """
        nou_estat = EstatRobot(nova_posicio, mida_taulell=self.mida_taulell)
        nou_estat.cami = self.cami.copy()  # Copiamos el camino actual
        nou_estat.cami.append((accio, moviment))  # Agregamos el nuevo movimiento
        return nou_estat


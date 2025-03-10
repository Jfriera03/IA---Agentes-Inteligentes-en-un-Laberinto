import copy
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

def posicio_dins_limits(posicio, mida_taulell):
    x, y = posicio
    return 0 <= x < mida_taulell[0] and 0 <= y < mida_taulell[1]

def paret_aqui(posicio, percepcio):
    return posicio in percepcio["PARETS"]

class EstatMinimax:
    def __init__(self, pos_jugador, pos_adversari, parets, mida_taulell, cami=None):
        self.pos_jugador = pos_jugador
        self.pos_adversari = pos_adversari
        self.parets = set(parets)
        self.mida_taulell = mida_taulell
        self.cami = cami if cami is not None else []

    def es_meta(self, desti):
        return self.pos_jugador == desti

    def generar_fills(self, percepcio, maximitzant=True):
        pos_actual = self.pos_jugador if maximitzant else self.pos_adversari
        posiciones_generadas = set()

        # Generar movimientos normales y de salto
        for direccio in joc.Laberint.MOVS:
            # Movimiento normal (MOURE)
            nova_posicio = calcula_nova_posicio(pos_actual, direccio)
            if posicio_dins_limits(nova_posicio, self.mida_taulell) and not paret_aqui(nova_posicio, percepcio):
                if nova_posicio not in posiciones_generadas:
                    posiciones_generadas.add(nova_posicio)
                    yield self.crear_nou_estat(nova_posicio, direccio, Accions.MOURE, maximitzant)

            # Movimiento de salto (BOTAR) - solo verificar posición final de salto
            nova_posicio_botar = calcula_nova_posicio(pos_actual, direccio, botar=True)  # posición final de salto

            # Condiciones para el salto
            if (posicio_dins_limits(nova_posicio_botar, self.mida_taulell) and
                not paret_aqui(nova_posicio_botar, percepcio) and  # No hay pared en la posición final
                nova_posicio_botar != self.pos_adversari):  # La posición final no está ocupada por el adversario

                if nova_posicio_botar not in posiciones_generadas:
                    posiciones_generadas.add(nova_posicio_botar)
                    yield self.crear_nou_estat(nova_posicio_botar, direccio, Accions.BOTAR, maximitzant)

        # Intentar colocar paredes
        for direccio in joc.Laberint.MOVS:
            nova_posicio_paret = calcula_nova_posicio(pos_actual, direccio, botar=True)

            if self.colocar_paret(percepcio, direccio, maximitzant):
                nou_estat = self.crear_nou_estat(pos_actual, direccio, Accions.POSAR_PARET, maximitzant)
                nueva_parets = self.parets.copy()
                nueva_parets.add(nova_posicio_paret)
                nou_estat.parets = nueva_parets
                yield nou_estat

    def crear_nou_estat(self, nova_posicio, moviment, accio, maximitzant):
        nou_estat = EstatMinimax(
            pos_jugador=nova_posicio if maximitzant else self.pos_jugador,
            pos_adversari=self.pos_adversari if maximitzant else nova_posicio,
            parets=self.parets,
            mida_taulell=self.mida_taulell,
            cami=self.cami + [(accio, moviment)]  # Añadir al camino actual
        )
        return nou_estat

    def colocar_paret(self, percepcio, direccio, maximitzant):
        pos_actual = self.pos_jugador if maximitzant else self.pos_adversari
        nova_posicio = calcula_nova_posicio(pos_actual, direccio, botar=True)

        return posicio_dins_limits(nova_posicio, self.mida_taulell) and not paret_aqui(nova_posicio, percepcio)

import heapq
from practica.joc import Accions
import joc

class NodeAEstrella:
    def __init__(self, posicio, g, f, cami=None):
        if cami is None:
            cami = []
        self.posicio = posicio   # Posición del nodo
        self.g = g               # Coste desde el inicio hasta este nodo
        self.f = f               # f = g + h (coste total estimado)
        self.cami = cami         # El camino seguido hasta este nodo

    def __lt__(self, other):
        return self.f < other.f  # Comparar nodos según el valor f para la cola de prioridad

class ViatgerAEstrella(joc.Viatger):

    PES_MOURE = 1    # Coste de moverse
    PES_BOTAR = 2    # Coste de botar

    def heuristica(self, pos_actual, desti):
        """ Heurística basada en la distancia Manhattan """
        return abs(pos_actual[0] - desti[0]) + abs(pos_actual[1] - desti[1])

    import heapq

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        """ Implementación del algoritmo A* para encontrar el mejor camino """

        # Obtener el estado actual
        pos_inicial = self.posicio
        desti = percepcio['DESTI']

        # Inicializar la cola de prioridad (frontera) y el conjunto de explorados
        frontier = []
        heapq.heappush(frontier, NodeAEstrella(pos_inicial, 0, self.heuristica(pos_inicial, desti)))

        # Diccionario para almacenar el costo de la ruta más barata a cada nodo
        cost_registrado = {pos_inicial: 0}
        explorats = set()

        millor_cami = None

        while frontier:
            # Sacar el nodo con el menor f (coste total estimado)
            node_actual = heapq.heappop(frontier)

            # Si llegamos al destino, terminamos
            if node_actual.posicio == desti:
                millor_cami = node_actual.cami
                break

            # Marcar como explorado
            explorats.add(node_actual.posicio)

            # Generar todos los movimientos posibles desde la posición actual
            moviments_possibles = ['N', 'S', 'E', 'O']  # Norte, Sur, Este, Oeste

            for moviment in moviments_possibles:
                # Calcular la nueva posición para el movimiento normal
                nova_posicio = self.calcula_nova_posicio(node_actual.posicio, moviment)

                if self.posicio_dins_limits(nova_posicio, percepcio) and not self.paret_aqui(nova_posicio, percepcio):
                    # Calcular coste del movimiento y f(n)
                    cost_moviment = self.PES_MOURE
                    g_nou = node_actual.g + cost_moviment
                    f_nou = g_nou + self.heuristica(nova_posicio, desti)

                    # Solo añadir el nodo si es un camino mejor o no explorado aún
                    if nova_posicio not in explorats or g_nou < cost_registrado.get(nova_posicio, float('inf')):
                        cost_registrado[nova_posicio] = g_nou
                        nou_cami = node_actual.cami + [(Accions.MOURE, moviment)]
                        heapq.heappush(frontier, NodeAEstrella(nova_posicio, g_nou, f_nou, nou_cami))

                # Intentar botar si es posible (coste 2)
                nova_posicio_botar = self.calcula_nova_posicio(node_actual.posicio, moviment, botar=True)
                if self.posicio_dins_limits(nova_posicio_botar, percepcio) and not self.paret_aqui(nova_posicio_botar,
                                                                                                   percepcio):
                    cost_botar = self.PES_BOTAR
                    g_nou = node_actual.g + cost_botar
                    f_nou = g_nou + self.heuristica(nova_posicio_botar, desti)

                    if nova_posicio_botar not in explorats or g_nou < cost_registrado.get(nova_posicio_botar,
                                                                                          float('inf')):
                        cost_registrado[nova_posicio_botar] = g_nou
                        nou_cami = node_actual.cami + [(Accions.BOTAR, moviment)]
                        heapq.heappush(frontier, NodeAEstrella(nova_posicio_botar, g_nou, f_nou, nou_cami))

        # Si encontramos el mejor camino, devolver el primer movimiento
        if millor_cami:
            return millor_cami[0]
        else:
            return Accions.ESPERAR

    def calcula_nova_posicio(self, posicio_actual, moviment, botar=False):
        """ Calcula la nueva posición dado un movimiento y si es un 'bot' """
        moviments = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0)
        }
        if botar:
            return (posicio_actual[0] + 2 * moviments[moviment][0], posicio_actual[1] + 2 * moviments[moviment][1])
        else:
            return (posicio_actual[0] + moviments[moviment][0], posicio_actual[1] + moviments[moviment][1])

    def posicio_dins_limits(self, posicio, percepcio):
        """ Verifica si la posición está dentro de los límites del tablero """
        x, y = posicio
        return 0 <= x < len(percepcio["TAULELL"]) and 0 <= y < len(percepcio["TAULELL"][0])

    def paret_aqui(self, posicio, percepcio):
        """ Verifica si hay una pared en la nueva posición """
        return posicio in percepcio["PARETS"]

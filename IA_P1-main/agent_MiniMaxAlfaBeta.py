import math
from practica.joc import Accions
import estatMiniMax
import joc


class ViatgerMinimax(joc.Viatger):
    def __init__(self, nom, mida_taulell):
        super().__init__(nom, mida_taulell)
        self.mida_taulell = mida_taulell
        self.max_depth = 3  # Profundidad máxima del árbol Minimax
        self.costo_mover = 1
        self.costo_saltar = 2
        self.costo_poner_pared = 4

    def heuristica(self, estat, desti, pos_adversari):
        # Calcula una puntuación basada en la distancia al objetivo y otros factores estratégicos
        dist_jugador = abs(estat.pos_jugador[0] - desti[0]) + abs(estat.pos_jugador[1] - desti[1])
        dist_adversari = abs(pos_adversari[0] - desti[0]) + abs(pos_adversari[1] - desti[1])

        puntuacio = -dist_jugador  # Penaliza estar lejos del objetivo
        puntuacio += dist_adversari  # Beneficio si el adversario está más lejos del objetivo

        return puntuacio

    def minimax(self, estat, profunditat, alpha, beta, maximitzant, percepcio, desti, pos_adversari, visitados):
        # Generar un identificador único para el estado actual
        estado_id = (estat.pos_jugador, estat.pos_adversari, frozenset(estat.parets))

        # Marcar el estado como visitado para evitar ciclos
        if estado_id in visitados:
            return self.heuristica(estat, desti, pos_adversari), estat.cami
        visitados.add(estado_id)  # Marcado en preorden para evitar ciclos

        # Condición de parada: profundidad máxima o estado meta alcanzado
        if profunditat == 0 or estat.es_meta(desti):
            return self.heuristica(estat, desti, pos_adversari), estat.cami

        if maximitzant:
            max_eval = -math.inf
            mejor_cami = None
            for hijo in estat.generar_fills(percepcio, maximitzant):
                eval_hijo, cami_hijo = self.minimax(hijo, profunditat - 1, alpha, beta, False, percepcio, desti,
                                                    pos_adversari, visitados)

                # Ajustar el puntaje de la evaluación en función de la acción
                if hijo.cami[-1][0] == Accions.MOURE:
                    eval_hijo -= self.costo_mover
                elif hijo.cami[-1][0] == Accions.BOTAR:
                    eval_hijo -= self.costo_saltar
                elif hijo.cami[-1][0] == Accions.POSAR_PARET:
                    eval_hijo -= self.costo_poner_pared

                if eval_hijo > max_eval:
                    max_eval = eval_hijo
                    mejor_cami = cami_hijo
                alpha = max(alpha, eval_hijo)
                if beta <= alpha:
                    break  # Poda beta
            return max_eval, mejor_cami
        else:
            min_eval = math.inf
            mejor_cami = None
            for hijo in estat.generar_fills(percepcio, maximitzant):
                eval_hijo, cami_hijo = self.minimax(hijo, profunditat - 1, alpha, beta, True, percepcio, desti,
                                                    pos_adversari, visitados)

                # Ajustar el puntaje de la evaluación en función de la acción
                if hijo.cami[-1][0] == Accions.MOURE:
                    eval_hijo += self.costo_mover
                elif hijo.cami[-1][0] == Accions.BOTAR:
                    eval_hijo += self.costo_saltar
                elif hijo.cami[-1][0] == Accions.POSAR_PARET:
                    eval_hijo += self.costo_poner_pared

                if eval_hijo < min_eval:
                    min_eval = eval_hijo
                    mejor_cami = cami_hijo
                beta = min(beta, eval_hijo)
                if beta <= alpha:
                    break  # Poda alfa
            return min_eval, mejor_cami

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        desti = percepcio["DESTI"]
        agents = percepcio.get("AGENTS", None)

        # Asegurarse de que hay al menos dos agentes en el entorno
        if not agents or len(agents) < 2:
            return Accions.ESPERAR

        # Posiciones del jugador y del adversario
        pos_jugador = agents[self.nom]
        pos_adversari = [pos for nom, pos in agents.items() if nom != self.nom][0]

        # Crear el estado inicial para el algoritmo Minimax
        estat_inicial = estatMiniMax.EstatMinimax(pos_jugador, pos_adversari, percepcio["PARETS"], self.mida_taulell)

        # Ejecutar el algoritmo Minimax con poda alfa-beta
        visitados = set()  # Conjunto para rastrear los estados visitados y evitar ciclos
        _, mejor_cami = self.minimax(estat_inicial, self.max_depth, -math.inf, math.inf, True, percepcio, desti,
                                     pos_adversari, visitados)

        # Si no hay un camino óptimo, espera
        if not mejor_cami:
            return Accions.ESPERAR

        # Devolver la mejor acción calculada
        accion, direccion = mejor_cami[0]
        return accion, direccion

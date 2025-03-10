from practica import agent, joc, agent_profunditat, agent_A_estrella, agent_MiniMaxAlfaBeta


def main():
    mida = (10,10)

    agents = [
        #agent_profunditat.Viatger("Agent 1", mida_taulell=mida),
        #agent_A_estrella.ViatgerAEstrella("Agent 2", mida_taulell=mida),
        agent_MiniMaxAlfaBeta.ViatgerMinimax("Agent 3", mida_taulell=mida),
        agent_MiniMaxAlfaBeta.ViatgerMinimax("Agent 4", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()

if __name__ == "__main__":
    main()

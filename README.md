# 🔍 Agentes Inteligentes en un Laberinto

## 🤝 Colaboradores

- [Jfriera03](https://github.com/Jfriera03)
- [MasoalM](https://github.com/MasoalM)

## 📌 Descripción

Este proyecto implementa agentes inteligentes que resuelven un laberinto mediante algoritmos de búsqueda. Se desarrollan estrategias como DFS, A*, y Minimax con poda alfa-beta para optimizar el recorrido.

## 🛠️ Tecnologías y Herramientas

- **Lenguaje:** Python 🐍
- **Librerías utilizadas:** `heapq`, `math`, `random`, `pygame`.
- **Estructuras de datos empleadas:**
  - Diccionarios para el estado del entorno.
  - Pilas para la búsqueda en profundidad.
  - Colas de prioridad para A*.
  - Árboles de decisión para MiniMax.

## 📌 Arquitectura del Código

El código está estructurado en los siguientes archivos:

- **`__main__.py`**: Punto de entrada del programa, inicializa el entorno y ejecuta la simulación.
- **`agent.py`**: Implementación básica de un agente.
- **`agent_profunditat.py`**: Implementación del agente con búsqueda en profundidad (DFS).
- **`agent_A_estrella.py`**: Implementación del agente con el algoritmo A*.
- **`agent_MiniMaxAlfaBeta.py`**: Implementación del agente con MiniMax y poda alfa-beta.
- **`estat.py`** y **`estatMiniMax.py`**: Definición de estados y funciones auxiliares para la simulación.
- **`joc.py`**: Define el tablero y las reglas del juego.

## 🚀 Instalación y Uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Jfriera03/agentes-laberinto.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd agentes-laberinto
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el código principal:
   ```bash
   python __main__.py
   ```

## 🎮 Funcionamiento del Algoritmo

El entorno es un tablero de tamaño configurable donde los agentes deben alcanzar su destino. Las acciones disponibles son:

- **Moverse** en las direcciones Norte, Sur, Este y Oeste.
- **Botar** sobre una casilla a dos distancias en cualquier dirección.
- **Colocar una pared** para bloquear el paso del oponente.

Los agentes implementan diferentes estrategias para decidir su próximo movimiento:

### 🔹 Búsqueda en Profundidad (DFS)
- Utiliza una **pila** para explorar caminos.
- No garantiza la solución más óptima.

### 🔹 Algoritmo A*
- Usa una **cola de prioridad** con heurística basada en distancia Manhattan.
- Encuentra la solución óptima si la heurística es admisible.

### 🔹 MiniMax con Poda Alfa-Beta
- Simula la estrategia de dos agentes compitiendo.
- Usa un **árbol de decisión** con profundidad limitada.
- Aplica **poda alfa-beta** para mejorar eficiencia.

## 🏗️ Implementación Técnica

### 📌 Estados y Percepción
Cada agente recibe información sobre el entorno en forma de diccionario:
- **`PARETS`**: Lista de coordenadas donde hay paredes.
- **`TAULELL`**: Matriz que representa el tablero.
- **`DESTI`**: Coordenadas del objetivo.
- **`AGENTS`**: Diccionario con la posición de cada agente.

### 📌 Clases Principales

- **`Viatger`** (Clase Base): Implementa la estructura básica del agente.
- **`Laberint`**: Controla la dinámica del tablero y gestiona movimientos.
- **`EstatRobot` y `EstatMinimax`**: Modelan los estados y transiciones de los agentes.

### 📌 Costes de Acciones
Las acciones tienen diferentes costos:
- **Moverse**: 1 unidad.
- **Botar**: 2 unidades.
- **Colocar una pared**: 4 unidades.

Los algoritmos consideran estos costos para optimizar sus decisiones.

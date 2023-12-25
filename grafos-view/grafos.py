import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json

def leer_nombres_desde_archivo(archivo):
    """
    Lee nombres de nodos desde un archivo de texto.

    Parameters:
        - archivo: Nombre del archivo de texto.

    Returns:
        - Lista de nombres de nodos.
    """
    with open(archivo, 'r') as file:
        nombres = [line.strip() for line in file]
    return nombres

def generar_grafo_aleatorio_conectado(num_nodos, probabilidad_reconexión):
    """
    Genera un grafo aleatorio conectado.

    Parameters:
        - num_nodos: Número de nodos en el grafo.
        - probabilidad_reconexión: Probabilidad de reconexión para la función watts_strogatz_graph.

    Returns:
        - Un objeto de grafo NetworkX.
    """
    G = nx.connected_watts_strogatz_graph(num_nodos, 4, probabilidad_reconexión)

    # Leer nombres de nodos desde el archivo
    nombres_nodos = leer_nombres_desde_archivo(archivo_nombres)

    # Verificar que hay suficientes nombres para los nodos
    if len(nombres_nodos) < num_nodos:
        raise ValueError("El archivo de nombres no contiene suficientes nombres para todos los nodos.")

    # Asignar nombres a los nodos
    nombres_nodos = {i: nombres_nodos[i] for i in range(num_nodos)}
    nx.set_node_attributes(G, nombres_nodos, 'nombre')

    return G,nombres_nodos

def mostrar_grafo(grafo):
    """
    Muestra el grafo en una imagen.

    Parameters:
        - grafo: Objeto de grafo NetworkX.
    """
    pos = nx.spring_layout(grafo)  # Algoritmo de disposición para organizar los nodos

    # Obtener etiquetas de nodos (nombres)
    etiquetas_nodos = nx.get_node_attributes(grafo, 'nombre')

    nx.draw(grafo, pos, with_labels=True, labels=etiquetas_nodos, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)
    plt.show()  

def profile_file(nombre_propio, info_connection, vecinos):

    # Crear el diccionario final
    data = {
        "myself": nombre_propio,
        "port": info_connection[1],
        "neighbors": vecinos
    }

    # Convertir el diccionario a formato JSON
    json_output = json.dumps(data, indent=4)

    # Guardar el JSON en un archivo llamado "user.pf"
    with open('../profiles/'+nombre_propio+".pf", "w") as file:
        file.write(json_output)

    print(f"El JSON se ha guardado en el archivo 'user.pf'.")
    
if __name__ == "__main__":
    # Parámetros para generar el grafo aleatorio conectado
    num_nodos = 30
    probabilidad_reconexión = 0.1
    archivo_nombres = 'nombres.txt'

    # Generar el grafo aleatorio conectado
    grafo_aleatorio_conectado,nombres = generar_grafo_aleatorio_conectado(num_nodos, probabilidad_reconexión)

    # Mostrar los nombres
    print("Nombres: ",nombres)

    # Obteniendo lista con data:
    vertices = {}

    for i in range(len(nombres)):
        vertices[nombres[i]] = ["127.0.0.1", (7000 + i)]

    print(vertices)

    # Imprimir la matriz de representación del grafo
    matriz_de_adyacencia = nx.to_numpy_matrix(grafo_aleatorio_conectado)
    f,_ = matriz_de_adyacencia.shape

    print("Matriz de Adyacencia:")
    print(matriz_de_adyacencia)

    for i in range(f):
        current_name = nombres[i]
        current_neighbours = np.ravel(matriz_de_adyacencia[i])
        #print(i,':',current_name,current_neighbours)

        print("Para el nodo:",current_name)
        print("Vecinos: ", end='')
        vecinos = {}
        for j in range(len(current_neighbours)):
            if current_neighbours[j] == 1:
                vecinos[nombres[j]] = vertices[nombres[j]]
                print(nombres[j]+', ', end='')
        print()
        print("Imprimiendo vecinos en lista", vecinos)
        # Generando los archivos:
        profile_file(current_name, vertices[current_name], vecinos)

    # Mostrar el grafo
    mostrar_grafo(grafo_aleatorio_conectado)

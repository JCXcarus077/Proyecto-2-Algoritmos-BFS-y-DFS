# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:02:30 2024

@author: Juan Carlos Perez Meneses
"""
import random
import math


"""NO SE USO 

def Color():    
    r = random.randrange(0, 254, 23)  # Función para generar colores aleatorios
    g = random.randrange(0, 254, 23)
    b = random.randrange(0, 254, 23)    
    return '"#{:02x}{:02x}{:02x}"'.format(r, g, b)

"""

class Nodo:
    
    def __init__(self, id): #Self se usa para hacer referencia
    
        self.id = id #Inicializa un nuevo nodo con un identificador
        
class Arista:
    
    def __init__(self, nodo_origen, nodo_destino):
        #inicializar una nueva arista con un origen, destino y un identificador
        
        self.arista = [nodo_origen, nodo_destino]
        
class Grafo:
    
    def __init__(self,dirigido = False):
        self.dirigido = dirigido
        self.nodos = []
        self.aristas = []
        
        
    
    def addNodo(self,nodo):
        if nodo not in self.nodos:
            nodo = Nodo(nodo)
            self.nodos.append(nodo.id)
            
    def addArista(self, n0, n1):
        A = Arista(n0, n1)
        if n0 in self.nodos and n1 in self.nodos:
            self.aristas.append([A.arista[0], A.arista[1]])
        if not self.dirigido:
            self.aristas.append([A.arista[1], A.arista[0]])
        
    
    def gen_archivo(self, T_grafo):
        
        grafo_files = {
        1: "Grafo de Malla.gv",
        2: "Grafo de Erdös y Rényi.gv",
        3: "Grafo de Gilbert.gv",
        4: "Grafo Geográfico Simple.gv",
        5: "Grafo Barabási-Albert.gv",
        6: "Grafo Dorogovtsev-Mendes.gv",
        7: "Arbol_BFS.gv",
        8: "Arbol_DFS_R.gv",
        9: "Arbol_DFS_I.gv"
        }
        
        filename = grafo_files.get(T_grafo)
        if filename is None:
            print("Tipo de grafo no válido.")
            return
        
        with open(filename, "w") as f:
            f.write("graph sample {\n")
            
            for arista in self.aristas:
                n0, n1 = str(arista[0]), str(arista[1])
                f.write(f"{n0} -- {n1};\n")
            
            for nodo in self.nodos:
                if not any(nodo in arista for arista in self.aristas):
                    f.write(f"{nodo};\n")
            
            f.write("}")
            
    def BFS(self, s):
        visitado = set() #Los set en Python son un tipo que permite almacenar varios elementos y acceder a ellos de una forma muy similar a las listas pero con ciertas diferencias: Los elementos de un set son único, lo que significa que no puede haber elementos duplicados.
        cola = [s]
        arbol_BFS = Grafo()
        visitado.add(s)

        while cola:
            nodo = cola.pop(0)
            arbol_BFS.addNodo(nodo)

            for vecino in self.obtenerVecinos(nodo):
                if vecino not in visitado:
                    visitado.add(vecino)
                    cola.append(vecino)
                    arbol_BFS.addNodo(vecino)
                    arbol_BFS.addArista(nodo, vecino)

        return arbol_BFS
    
    def DFS_R(self, s):
        visitado = set()
        arbol_DFS = Grafo()
        
        def dfs_recursivo(nodo):
            visitado.add(nodo)
            arbol_DFS.addNodo(nodo)

            for vecino in self.obtenerVecinos(nodo):
                if vecino not in visitado:
                    arbol_DFS.addArista(nodo, vecino)
                    dfs_recursivo(vecino)
                elif not arbol_DFS.aristas or [nodo, vecino] not in arbol_DFS.aristas:
                    arbol_DFS.addArista(nodo, vecino)
                    
            # print(nodo, "-->" ,vecino) #Crea linea negra, ya que se repite en ambas veces

        dfs_recursivo(s)
        return arbol_DFS

    def DFS_I(self, s):                             #stack --> Pila
        visitado = set()
        pila = [(s, None)] #Cada iteración en la pila es una tupla
        arbol_DFS = Grafo()

        while pila:
            nodo, origen = pila.pop()
            if nodo not in visitado:
                visitado.add(nodo)
                arbol_DFS.addNodo(nodo)
                
                if origen is not None: #Agrega arista solo si el nodo actual tiene un origen
                    arbol_DFS.addArista(origen, nodo)
                    #print("Añadiendo arista:", origen, "->", nodo)
                for vecino in self.obtenerVecinos(nodo):
                    if vecino not in visitado:
                        pila.append((vecino, nodo))  # Push neighbor and its parent to the stack

              
        return arbol_DFS

    def obtenerVecinos(self, nodo):
        vecinos = []
        for arista in self.aristas:
            if nodo in arista:
                vecinos.append(arista[1] if arista[0] == nodo else arista[0])
        return vecinos
    
"""
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
"""
def grafoMalla(m, n, dirigido = False):
    T_grafo = 1
    g = Grafo()
    
        # Crear nodos en la malla
    for i in range(m):
        for j in range(n):
            nodo_id = i * n + j  # Asignar un ID único para cada nodo
            g.addNodo(nodo_id)
    
    # Agregar aristas entre nodos adyacentes
    for i in range(m):
        for j in range(n):
            nodo_id = i * n + j
            if i < m - 1:
                g.addArista(nodo_id, nodo_id + n)  # Agregar arista hacia abajo
            if j < n - 1:
                g.addArista(nodo_id, nodo_id + 1)  # Agregar arista hacia la derecha
    
    g.gen_archivo(T_grafo)
    s = int(input("Nodo a iniciar en BFS: "))
    arbol_BFS = g.BFS(s)
    arbol_BFS.gen_archivo(7)
    
    t = int(input("Nodo a iniciar en DFS_R y DFS_I: "))
    arbol_DFS_R = g.DFS_R(t)
    arbol_DFS_R.gen_archivo(8)  # Output the recursive DFS tree to a file named "Árbol DFS Recursivo.gv"

    # Perform iterative DFS starting from node 1
    arbol_DFS_I = g.DFS_I(t)
    arbol_DFS_I.gen_archivo(9)  # Output the iterative DFS tree to a file named "Árbol DFS Iterativo.gv"

    return g 


"""
  Genera grafo aleatorio con el modelo Erdos-Renyi
  :param n: número de nodos (> 0)
  :param m: número de aristas (>= n-1)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
"""
def grafoErdosRenyi(n, m, dirigido=False):
    T_grafo = 2
    if m < n - 1:
        raise ValueError("El número de aristas debe ser al menos n - 1")
        
    g1 = Grafo()
    
    # Agregar nodos
    for nodo_id in range(1, n + 1):
        g1.addNodo(nodo_id)
    
    # Generar aristas aleatorias
    contador_aristas = 0
    while contador_aristas < m:
        nodo1 = random.randint(1, n)
        nodo2 = random.randint(1, n)
        
        # Verificar si la arista ya existe o si es un bucle
        #if nodo1 != nodo2 and not aristas(nodo1, nodo2):
        if nodo1 != nodo2 and (nodo1, nodo2) not in g1.aristas:
            g1.addArista(nodo1, nodo2)
            contador_aristas += 1
    
    g1.gen_archivo(T_grafo)
    arbol_BFS = g1.BFS(50)
    arbol_BFS.gen_archivo(7)
    
    arbol_DFS_R = g1.DFS_R(11)
    arbol_DFS_R.gen_archivo(8)  # Output the recursive DFS tree to a file named "Árbol DFS Recursivo.gv"

    # Perform iterative DFS starting from node 1
    arbol_DFS_I = g1.DFS_I(11)
    arbol_DFS_I.gen_archivo(9)  # Output the iterative DFS tree to a file named "Árbol DFS Iterativo.gv"
    
    return g1


"""
  Genera grafo aleatorio con el modelo Gilbert
  :param n: número de nodos (> 0)
  :param p: probabilidad de crear una arista (0, 1)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """
def grafoGilbert(n, p, dirigido=False):
    T_grafo = 3
    
    g2 = Grafo()
    
    
    # Agregar nodos
    for nodo_id in range(1, n + 1):
        g2.addNodo(nodo_id)
    
    # Generar aristas aleatorias
    for nodo1 in g2.nodos: #Lista de nodos 
        for nodo2 in range(nodo1 + 1, n + 1):  # Iterate from nodo1 + 1 to n
            if random.random() < p:  # Comprobamos si se debe agregar una arista entre estos dos nodos
                g2.addArista(nodo1, nodo2)
                    
                    
    # print(g2.aristas) #Imprime los datos dentro de la lista aristas
    # print(g2.nodos)
    g2.gen_archivo(T_grafo)
    
    arbol_BFS = g2.BFS(19)
    arbol_BFS.gen_archivo(7)
    
    arbol_DFS_R = g2.DFS_R(11)
    arbol_DFS_R.gen_archivo(8)  

   
    arbol_DFS_I = g2.DFS_I(11)
    arbol_DFS_I.gen_archivo(9)  
    return g2


"""
Genera grafo aleatorio con el modelo geográfico simple
:param n: número de nodos (> 0)
:param r: distancia máxima para crear un nodo (0, 1)
:param dirigido: el grafo es dirigido?
:return: grafo generado
"""

def grafoGeografico(n, r, dirigido=False):
    T_grafo = 4
    g = Grafo()
    coor = []
    # Agregar nodos
    for nodo_id in range(n):
        g.addNodo(nodo_id)    # añadir el nodo con sus coordenadas
        x = random.random()  # coordenada x aleatoria
        y = random.random()  # coordenada y aleatoria
        coor.append([x,y])
    for i in g.nodos:
        for j in g.nodos:
            distancia = math.sqrt((coor[j-1][0]-coor[i-1][0])**2 + (coor[j-1][1]-coor[i-1][1])**2)
            if distancia <= r and [i,j] not in g.aristas and [j,i] not in g.aristas and i!=j:
                g.addArista(i, j)
                g.aristas.append([i,j])
            
    
    g.gen_archivo(T_grafo)
    
    arbol_BFS = g.BFS(12)
    arbol_BFS.gen_archivo(7)
    
    arbol_DFS_R = g.DFS_R(198)
    arbol_DFS_R.gen_archivo(8)  

   
    arbol_DFS_I = g.DFS_I(198)
    arbol_DFS_I.gen_archivo(9) 
    
    return g


"""
  Genera grafo aleatorio con el modelo Barabasi-Albert
  :param n: número de nodos (> 0)
  :param d: grado máximo esperado por cada nodo (> 1) --> número de vertices en c/nodo.
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """

def grafoBarabasiAlbert(n, d, dirigido=False):
    T_grafo = 5
    g = Grafo()
    
    
    # Agregar los primeros d nodos (aristas)
    for nodo_id in range(1, d+1): #Grado mas 1
        g.addNodo(nodo_id)  #El nodo se inicia a enumerar en 1
    
    # Conectar los primeros d nodos entre sí
    for i in range(1, d + 1):
        for j in range(i + 1, d + 1):
            g.addArista(i, j)
    
    # Generar el resto de los nodos
    for nodo_id in range(d + 1, n + 1):
        nuevos_enlaces = [] 
        while len(nuevos_enlaces) < d: #longitud de nuevos enlaces es menor a d
            total_aristas = sum(len(g.aristas[nodo]) for nodo in g.nodos) #suma el numero de aristas
            probabilidad = [len(g.aristas[nodo]) / total_aristas for nodo in g.nodos]
            nodo_destino = random.choices(g.nodos, weights=probabilidad)[0]
            if nodo_destino not in nuevos_enlaces:
                nuevos_enlaces.append(nodo_destino)
                g.addArista(nodo_id, nodo_destino)
                g.addArista(nodo_destino, nodo_id)  # Si no es dirigido, también se debe agregar la arista en la otra dirección
    
    
    g.gen_archivo(T_grafo)
    
    arbol_BFS = g.BFS(15)
    arbol_BFS.gen_archivo(7)
    
    arbol_DFS_R = g.DFS_R(356)
    arbol_DFS_R.gen_archivo(8)  

   
    arbol_DFS_I = g.DFS_I(356)
    arbol_DFS_I.gen_archivo(9) 
    
    return g


"""
  Genera grafo aleatorio con el modelo
  :param n: número de nodos (≥ 3)
  :param dirigido: el grafo es dirigido?
  :return: grafo generado
  """

def grafoDorogovtsevMendes(n, dirigido=False):
    if n < 3:
        raise ValueError("El número de nodos debe ser al menos 3 para crear un triángulo inicial")
    T_grafo = 6
    g = Grafo(dirigido)
    
    # Agregar los primeros 3 nodos formando un triángulo
    for nodo_id in range(1, 4):
        g.addNodo(nodo_id)
    
    g.addArista(1, 2)
    g.addArista(2, 3)
    g.addArista(3, 1)
    
    # Generar el resto de los nodos
    for nodo_id in range(4, n + 1):
        arista_seleccionada = random.choice(g.aristas)
        nodo1, nodo2 = arista_seleccionada[0], arista_seleccionada[1]
        
        g.addNodo(nodo_id)
        g.addArista(nodo_id, nodo1)
        g.addArista(nodo_id, nodo2)
    g.gen_archivo(T_grafo)
    
    
    arbol_BFS = g.BFS(200)
    arbol_BFS.gen_archivo(7)
    
    arbol_DFS_R = g.DFS_R(250)
    arbol_DFS_R.gen_archivo(8)  

   
    arbol_DFS_I = g.DFS_I(250)
    arbol_DFS_I.gen_archivo(9) 
    
    return g


if __name__ == "__main__":
   
    #grafoMalla(20, 25) 
    #grafoErdosRenyi(500, 500) 
    #grafoGilbert(500, 0.04) #0.15
    # grafoGeografico(500, 0.09) #Variar radio
    #grafoBarabasiAlbert(500, 5)
    #grafoDorogovtsevMendes(500)
    pass
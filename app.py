from flask import Flask, render_template, request
from collections import defaultdict
import json
app = Flask(__name__)

# algorithm for Euler cycles
class EulerGraph:
  
    def __init__(self, vertices):
        self.V= vertices # number of vertices
        self.graph = defaultdict(list) # stores graph
  
    def addEdge(self, u, v):
        '''
        Method that adds edges to a graph.
        '''
        self.graph[u].append(v)
        self.graph[v].append(u)
  
    def DFSUtil(self, visited, v):
        '''
        Depth-first search method used later.
        '''
        visited[v]= True # marks the current vertex as visited
 
        # repeat for all adjacent vertices
        for j in self.graph[v]:
            if visited[j]==False:
                self.DFSUtil(visited, j)
  
    def isConnected(self):
        '''
        Method that checks if all vertices (not zero degree) are
        connected using Depth-first search.
        '''

        visited =[False]*(self.V) # mark all vertices as not visited
 
        #  find a vertex that is connected to at least one other vertex
        for i in range(self.V):
            if len(self.graph[i]) > 1:
                break
 
        # returns True if the graph has no edges
        if i == self.V-1:
            return True
 
        # begin traversing from a vertex that is connected to at least one other vertex
        self.DFSUtil(visited, i)
 
        # are all non-empty vertices visited?
        for i in range(self.V):
            if visited[i]==False and len(self.graph[i]) > 0:
                return False
        return True
 
    def isEulerian(self):
        '''
        Returns 2 if the graph has an Euler Circuit,
        1 if the graph has an Euler Path,
        0 if the graph is not Eulerian.
        '''
        # are all (non-empty) vertices connected?
        # if not, it cannot be Eulerian
        if self.isConnected() == False:
            return 0
        # otherwise, count vertices with odd degree
        else:
            odd = 0
            for i in range(self.V):
                if len(self.graph[i]) % 2 != 0:
                    odd += 1
            # if the count is 0 then the graph has an Euler Circuit.
            if odd == 0:
                return 2
            # if the count is 2 then the graph has an Euler Path.
            elif odd == 2:
                return 1
            # otherwise, the graph is not Eulerian
            # the count can't be exactly 1 for an undirected graph
            elif odd > 2:
                return 0
 
    def returnIsEulerian(self):
        '''
        Method that runs the above algorithm and returns whether the graph is
        Eulerian, semi-Eulerian, or neither.
        '''
        result = self.isEulerian()
        if result == 0:
            return "Graph is not Eulerian"
        elif result == 1 :
            return "Graph has an Euler path"
        else:
            return "Graph has an Euler cycle"
 
# algorithm for Hamiltonian circuit
class HamGraph():

    def __init__(self, vertices):
        self.graph = [[0 for column in range(vertices)]\
                            for row in range(vertices)]
        self.V = vertices
 
    def isOkay(self, path, v, position):
        ''' 
        Method that checks if the current vertex is adjacent
        to the previous vertex and isn't already in the path
        we're traversing.
        '''
        # return False if current vertex and previous vertex
        # are adjacent
        if self.graph[ path[position-1] ][v] == 0:
            return False
 
        # return False if current vertex is already in path
        for vertex in path:
            if vertex == v:
                return False
        # otherwise, return True
        return True
 
    def hamCycle(self, position, path):
        '''
        Method that returns True if the graph has a Ham Circuit,
        False otherwise.
        '''

        # first assume all vertices are included in the path
        if position == self.V:
            # are the last and first vertices adjacent?
            # this must be true to form a circuit
            if self.graph[path[position-1]][path[0]] == 1:
                return True
            else:
                return False
 
        # now try other vertices as candidates in Ham Circuit path
        for v in range(1,self.V):
            if self.isOkay(path, v, position) == True:
                path[position] = v
 
                if self.hamCycle(position+1, path) == True:
                    return True
                # remove current vertex if it isn't a potential Ham Circuit
                path[position] = -1
 
        return False
 
    def isHamiltonian(self):
        '''
        Method that returns whether a graph has a Hamiltonian Circuit
        or not.
        '''
        path = [-1] * self.V
 
        # try starting the Hamiltonian circuit from vertex 0 arbitrarily
        path[0] = 0
 
        if self.hamCycle(1, path) == False:
            return "Graph does not have a Hamiltonian Circuit"
        else:
            return "Graph has a Hamiltonian Circuit"
 
# algorithm for Bipartite graph checking
class BipGraph():
 
    def __init__(self, V):
        self.V = V
        self.graph = [[0 for column in range(V)] \
                                for row in range(V)]

    def isBipartite(self, src):
        '''
        Method returns True if graph is bipartite 
        using Breadth-First Search and coloring algorithm, otherwise False.
        '''
 
        # -1 means vertex has no color. Initially no vertices have color
        colorArray = [-1] * self.V
 
        # 1 means first color
        # so if a vertex has value 0 that means it has a second color
        colorArray[src] = 1
 
        # create a queue of vertices and add the source to it
        queue = []
        queue.append(src)
 
        # run BFS while the queue is non-empty
        while queue:
            u = queue.pop()
            # if we ever encounter a self-loop, graph can't be bipartite!
            if self.graph[u][u] == 1:
                return False;
            for v in range(self.V):
                # if edge u-v exists and v isn't colored,
                # assign different color to v
                # then append v to the queue
                if colorArray[v] == -1 and self.graph[u][v] == 1:
                    colorArray[v] = 1 - colorArray[u]
                    queue.append(v)
                # if edge u-v exists and v is colored
                # the same as u, graph isn't bipartite
                elif self.graph[u][v] == 1 and colorArray[v] == colorArray[u]:
                    return "Graph is not Bipartite"
        # otherwise, the graph is bipartite
        return "Graph is Bipartite"

# finally, get the necessary data from each graph,
# put it into a form that's readable by the algorithm,
# run the algorithm and return the result
@app.route('/', methods=['GET', 'POST'])
def my_page():
    result = ''
    if request.method == 'POST':
        raw_json = request.form.get('stuff', '')
        obj = json.loads(raw_json) # contains raw python object
        type = request.form.get('algorithm', '')
        # set up the 
        A = [li['nodeA'] for li in obj['links']]
        B = [li['nodeB'] for li in obj['links']]
        C = A
        D = B
        Y = A + D
        Z = B + C
        N = [li['x'] for li in obj['nodes']]
        vertices = len(N)
        # if the user is checking for Euler paths
        if type == 'eulerian':
            # zip the nodes together
            g1 = EulerGraph(vertices)
            for a, b in zip(A, B):
                g1.addEdge(a, b)
            # and run the algorithm
            result = g1.returnIsEulerian()
        # if the user is checking for Hamiltonian cycle
        if type == 'hamilton':
            # create an adjacency matrix
            adjMatrix = [[0 for i in range(vertices)] for k in range(vertices)]
            for i in range(len(Y)):
                u = Y[i]
                v = Z[i]
                adjMatrix[u][v] = 1
            g2 = HamGraph(vertices)
            g2.graph = adjMatrix
            # run the algorithm
            result = g2.isHamiltonian()
        # if the user is checking whether the graph is bipartite
        if type == 'bipartite':
            # create an adjacency matrix
            adjMatrix = [[0 for i in range(vertices)] for k in range(vertices)]
            for i in range(len(Y)):
                u = Y[i]
                v = Z[i]
                adjMatrix[u][v] = 1
            g3 = BipGraph(vertices)
            g3.graph = adjMatrix
            # run the algorithm
            result = g3.isBipartite(0)
    # return the result of the algorithm
    return render_template('index.html', result=result)

@app.route('/about/')
def about():
    return render_template('about.html')
class Graph_CGWM:

    def __init__(self):
        '''
        initializer for the directed graph
        the list of vertices is a normal list
        the list of edges is a dictionary with the key a tuple consisting of the vertexes and the value its cost
        '''
        self.__number_of_vertices = 16
        self.__number_of_edges = 30
        self.__adjacency_list_in = {"Cabbage-Goat-Wolf-Man" : [], "Cabbage-Goat-Wolf": [], "Cabbage-Goat-Man" : [],
                                    "Cabbage-Wolf-Man" : [], "Goat-Wolf-Man" : [], "Cabbage-Goat" : [], "Wolf-Man" : [],
                                    "Cabbage-Wolf" : [], "Goat-Wolf" : [], "Goat-Man" : [], "Cabbage-Man" : [], "Man" : [],
                                    "Wolf" : [], "Cabbage" : [], "Goat": [], "Nobody" : []}
        self.__adjacency_list_out = {"Cabbage-Goat-Wolf-Man" : [], "Cabbage-Goat-Wolf": [], "Cabbage-Goat-Man" : [],
                                    "Cabbage-Wolf-Man" : [], "Goat-Wolf-Man" : [], "Cabbage-Goat" : [], "Wolf-Man" : [],
                                    "Cabbage-Wolf" : [], "Goat-Wolf" : [], "Goat-Man" : [], "Cabbage-Man" : [], "Man" : [],
                                    "Wolf" : [], "Cabbage" : [], "Goat": [], "Nobody" : []}
        self.__list_of_vertices = []

    def read_from_file(self, filename):
        '''
        param filename:
        function which reads a graph from a text file and modifies the internal representation
        '''
        with open(filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                line = line.split()

                v1 = line[0]
                v2 = line[1]

                #temp = self.__adjacency_list_out[v1]
                #self.__adjacency_list_out[v1] = []
                self.__adjacency_list_out[v1].append(v2)
                #self.__adjacency_list_out[v1] = temp + self.__adjacency_list_out[v1]

                #temp = self.__adjacency_list_in[v2]
                #self.__adjacency_list_in[v2] = []
                self.__adjacency_list_in[v2].append(v1)
                #self.__adjacency_list_in[v2] = temp + self.__adjacency_list_in[v2]

            self.__list_of_vertices = self.__adjacency_list_out.keys()

        f.close()


    def print_vertices(self):
        for i in self.__list_of_vertices:
            print(i)

    def get_nr_of_vertices(self):
        return self.__number_of_vertices

    def get_nr_of_edges(self):
        return self.__number_of_edges

    def get_adjacency_list_out_vertex(self, vertex):
        return self.__adjacency_list_out[vertex]


D = Graph_CGWM()
D.read_from_file("CGWM.txt")

def breadth_first_minimum_path(graph, v1, v2):
    '''
        Function which calculates the minimum path between two vertices for a given graph
        :param graph: graph
        :param v1: vertex given as integer
        :param v2: vertex given as integer
        :return: the minimum path dictionary and the a dictionary prev with which we build the road
                 false if there is no path between them
    '''
    queue = []
    prev = {}
    dist = {}
    visited = []
    queue.append(v1)
    visited.append(v1)
    dist[v1] = 0
    while len(queue) != 0:
        x = queue.pop(-1)
        for y in graph.get_adjacency_list_out_vertex(x):
            if y not in visited:
                queue.append(y)
                visited.append(y)
                dist[y] = dist[x] + 1
                prev[y] = x
                if y == v2:
                    return prev,dist


p = breadth_first_minimum_path(D,"Cabbage-Goat-Wolf-Man","Nobody")[0]
string = "Nobody"[::-1] + " >- "
r = p["Nobody"]
while r != "Cabbage-Goat-Wolf-Man":
    string += r[::-1] + " >- "
    r = p[r]
string += r[::-1]
print(string[::-1])

print(breadth_first_minimum_path(D,"Cabbage-Goat-Wolf-Man","Nobody")[1]["Nobody"])





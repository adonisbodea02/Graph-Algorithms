import math
sup = math.inf

class Vertex:

    def __init__(self, number, time):
        '''
        param number
        creates a list of inbound vertexes and one of outbound vertexes, as well as iterators for each one
        '''
        self.number = number
        self.in_edges = []
        self.in_iterator = Iterator()
        self.out_edges = []
        self.out_iterator = Iterator()
        self.time = time
        self.earliest_start_time = 0
        self.earliest_finish_time = 0
        self.latest_start_time = 0
        self.latest_finish_time = 0

    def __str__(self):
        return str(self.number)

    def get_number(self):
        return self.number

    def set_earliest_start_time(self, time):
        self.earliest_start_time = time

    def set_latest_start_time(self, time):
        self.latest_start_time = time

    def set_earliest_finish_time(self, time):
        self.earliest_finish_time = time

    def set_latest_finish_time(self, time):
        self.latest_finish_time = time

class Iterator:
    """
    generic iterator which holds the current position and the maximum position
    """
    def __init__(self):
        self.n = 0
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration

class DirectedGraph:

    def __init__(self):
        '''
        initializer for the directed graph
        the list of vertices is a normal list
        the list of edges is a dictionary with the key a tuple consisting of the vertexes and the value its cost
        '''
        self.__number_of_vertices = 0
        self.__number_of_edges = 0
        self.__list_vertices = []
        self.__list_edges = {}
        self.__matrix = []

    def read_from_file(self, filename):
        '''
        param filename:
        function which reads a graph from a text file and modifies the internal representation
        '''
        with open(filename, "r") as f:
            lines = f.readlines()
            # the first consists of the numbers of vertices and edges
            line = lines[0]
            line = line.split()
            self.__number_of_vertices = int(line[0])
            self.__number_of_edges = int(line[1])
            self.__matrix = [[sup for i in range(self.__number_of_vertices)] for j in range(self.__number_of_vertices)]
            for i in range(self.__number_of_vertices):
                self.__matrix[i][i] = 0
            lines.pop(0)

            #create the vertices
            for i in range(self.__number_of_vertices):
                line = lines[0]
                line = line.split()
                time = int(line[0])
                v = Vertex(i,time)
                self.__list_vertices.append(v)
                lines.pop(0)


            for line in lines:
                line = line.split()
                #get the edges
                v1 = int(line[0])
                v2 = int(line[1])
                cost = int(line[2])
                self.__matrix[v1][v2] = cost
                #record them for the vertices such that we can iterate through the neighbours
                self.__list_vertices[v1].out_edges.append(self.__list_vertices[v2])
                self.__list_vertices[v2].in_edges.append(self.__list_vertices[v1])
                tpl = (v1,v2)
                #add the edge to the dictionary
                self.__list_edges[tpl] = cost

            #set the maximum length for iterators
            for i in self.__list_vertices:
                i.in_iterator.n = len(i.in_edges)
                i.out_iterator.n = len(i.out_edges)

        f.close()


    def get_vertex(self, v):
        return self.__list_vertices[v]

    def print_vertices(self):
        for i in self.__list_vertices:
            print(i.number, i.time)

    def print_edges(self):
        for key, values in self.__list_edges.items():
            print(key, values)

    def get_nr_of_vertices(self):
        return self.__number_of_vertices

    def get_nr_of_edges(self):
        return self.__number_of_edges

    def verify_edge(self, v1, v2):
        #check if the (v1,v2) is an edge by verifying if it is a key
        return (v1,v2) in self.__list_edges.keys()

    def get_in_degree(self, v):
        return len(self.__list_vertices[v].in_edges)

    def get_out_degree(self, v):
        return len(self.__list_vertices[v].out_edges)

    def get_cost(self, v1, v2):
        #return the value associated to a key if it exists
        if (v1,v2) in self.__list_edges.keys():
            return self.__list_edges[(v1,v2)]
        return "No edge between these edges!"

    def set_cost(self, v1, v2, new_cost):
        # sets the value associated to a key if it exists
        if (v1,v2) in self.__list_edges.keys():
            self.__list_edges[(v1, v2)] = new_cost
            return "Change made!"
        return "No edge between these vertices!"


    def get_first_in_bound(self, vertex):
        # with the iterator associated to the in_bound list of a vertex, we get the first neighbour of this kind
        i = self.__list_vertices[vertex].in_iterator.next()
        if i == 0:
            return self.__list_vertices[vertex].in_edges[i]
        else:
            self.__list_vertices[vertex].in_iterator.i -= 1
            return False

    def get_next_in_bound(self, vertex):
        # with the iterator associated to the in_bound list of a vertex, we get the next neighbour of this kind
        i = self.__list_vertices[vertex].in_iterator.next()
        if i == 0:
            self.__list_vertices[vertex].in_iterator.i -= 1
            return False
        else:
            return self.__list_vertices[vertex].in_edges[i]

    def get_first_out_bound(self, vertex):
        # with the iterator associated to the out_bound list of a vertex, we get the first neighbour of this kind
        i = self.__list_vertices[vertex].out_iterator.next()
        if i == 0:
            return self.__list_vertices[vertex].out_edges[i]
        else:
            self.__list_vertices[vertex].out_iterator.i -= 1
            return False

    def get_next_out_bound(self, vertex):
        # with the iterator associated to the out_bound list of a vertex, we get the next neighbour of this kind
        i = self.__list_vertices[vertex].out_iterator.next()
        if i == 0:
            self.__list_vertices[vertex].out_iterator.i -= 1
            return False
        else:
            return self.__list_vertices[vertex].out_edges[i]

    def get_matrix(self):
        return self.__matrix

    def get_vertices(self):
        return self.__list_vertices


D = DirectedGraph()
D.read_from_file("DirectedGraph4.txt")
print(max(-sup, -12))

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
        v = graph.get_vertex(x)
        for y in v.out_edges:
            if y.get_number() not in visited:
                queue.append(y.get_number())
                visited.append(y.get_number())
                dist[y.get_number()] = dist[x] + 1
                prev[y.get_number()] = x
                if y.get_number() == v2:
                    return prev,dist
    return False


def pseudo_matrix_multiplication(m1, m2):
    n = len(m1)
    m3 = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            m3[i][j] = sup
            for k in range(n):
                m3[i][j] = min(m3[i][j],m1[i][k]+m2[k][j])
    return m3


def apsp(graph):
    n = graph.get_nr_of_vertices()
    A = graph.get_matrix()
    B = [[sup for i in range(n)] for j in range(n)]
    for i in range(n):
        B[i][i] = 0
    i = 0
    while i <= n-2:
        B = pseudo_matrix_multiplication(A, B)
        #for j in range(n):
        #    print(B[j])
        #print("\n")
        i += 1
    return B

def topo_sort_dfs(g, x, sorted_list, fully_processed, in_process):
    in_process.append(x)
    for y in x.in_edges:
        if y in in_process:
            return False
        elif y not in fully_processed:
            ok = topo_sort_dfs(g, y, sorted_list, fully_processed, in_process)
            if not ok:
                return False
    in_process.remove(x)
    sorted_list.append(x)
    fully_processed.append(x)
    return True

def actual_topo_sort_dfs(g):
    sorted_list = []
    fully_processed = []
    in_process = []
    for x in g.get_vertices():
        if x not in fully_processed:
            ok = topo_sort_dfs(g, x, sorted_list, fully_processed, in_process)
            if not ok:
                sorted_list = []
                return sorted_list
    return sorted_list

def compute_times(g):
    ls = actual_topo_sort_dfs(g)

    for v in ls:
        if len(v.in_edges) == 0:
            v.set_earliest_finish_time(v.time)

    for v in ls:
        if len(v.in_edges) != 0:
            time = 0
            for t in v.in_edges:
                time = max(t.earliest_finish_time, time)
            v.set_earliest_start_time(time)
            v.set_earliest_finish_time(time + v.time)

    p1 = 0
    for v in ls:
        if len(v.out_edges) == 0:
            p1 = max(p1, v.earliest_finish_time)
            #v.set_latest_finish_time(v.earliest_finish_time)
            #v.set_latest_start_time(v.earliest_start_time)

    for v in ls:
        if len(v.out_edges) == 0:
            v.set_latest_finish_time(p1)
            v.set_latest_start_time(p1 - v.time)


    ls.reverse()
    for v in ls:
        if len(v.out_edges) != 0:
            time = v.out_edges[0].latest_start_time
            for t in v.out_edges:
                time = min(t.latest_start_time, time)
            v.set_latest_finish_time(time)
            if v.latest_finish_time != 0:
                v.set_latest_start_time(time - v.time)


    ls.reverse()

    return ls

# st = compute_times(D)
# if len(st) == 0:
#     print("Cycle found!")
# for i in range(len(st)):
#     print(st[i])
#     print(st[i].get_number(), st[i].time, st[i].earliest_start_time, st[i].latest_start_time)

class UI:

    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def printMenu():
        string = 'Available commands:\n'
        string += '\t 1. List all edges \n'
        string += '\t 2. Get the numbers of vertices \n'
        string += '\t 3. Get the number of edges \n'
        string += '\t 4. Check if there is a edge between two vertices  \n'
        string += '\t 5. Get the in-degree of a vertex \n'
        string += '\t 6. Get the out-degree of a vertex \n'
        string += '\t 7. Get the cost of an edge \n'
        string += '\t 8. Set the cost of an edge \n'
        string += '\t 9. Get the next outbound edge of a vertex \n'
        string += '\t 10. Get the next inbound edge of a vertex \n'
        string += '\t 11. Get the minimum path between 2 vertices \n'
        string += '\t 12. Get the minimum cost path between 2 vertices \n'
        string += '\t 13. List all vertices \n'
        string += '\t 14. Sort the graph topologically \n'
        string += '\t 15. Print the earliest and the latest starting time for each activity and the total time of the project \n'
        string += '\t 16. Print the critical path \n'
        string += '\t 0. Exit \n'
        print(string)

    @staticmethod
    def ValidInputCommand(command):
        """
        checks if the given command is a valid one
        Input: command - the given command - string
        Output: True - if the command is a valid ID command
                False - otherwise
        """
        availableCommands = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '0']
        return command in availableCommands

    @staticmethod
    def readPositiveInteger(msg):
        """
        reads a positive integer
        Input: msg - what message will be displayed to the user
        Output: A positive integer
        """
        res = 0
        while True:
            try:
                res = int(input(msg))
                if res < 0:
                    raise ValueError()
                break
            except ValueError:
                print("The value introduced is not a positive integer. ")
        return res

    def print_edges(self):
        self.graph.print_edges()

    def print_vertices(self):
        self.graph.print_vertices()

    def print_nr_of_edges(self):
        print(self.graph.get_nr_of_edges())

    def print_nr_of_vertices(self):
        print(self.graph.get_nr_of_vertices())

    def edge_between(self):
        v1 = self.readPositiveInteger("Give a vertex: ")
        v2 = self.readPositiveInteger("Give a vertex: ")
        print(self.graph.verify_edge(v1, v2))

    def inbound_degree_vertex(self):
        v = self.readPositiveInteger("Give a vertex: ")
        print(self.graph.get_in_degree(v))

    def outbound_degree_vertex(self):
        v = self.readPositiveInteger("Give a vertex: ")
        print(self.graph.get_out_degree(v))

    def get_cost_vertex(self):
        v1 = self.readPositiveInteger("Give a vertex: ")
        v2 = self.readPositiveInteger("Give a vertex: ")
        print(self.graph.get_cost(v1,v2))

    def set_cost_vertex(self):
        v1 = self.readPositiveInteger("Give a vertex: ")
        v2 = self.readPositiveInteger("Give a vertex: ")
        v = self.readPositiveInteger("Give a new value: ")
        print(self.graph.set_cost(v1, v2, v))

    def get_next_inbound_neighbour(self):
        v = self.readPositiveInteger("Give a vertex: ")
        res = self.graph.get_first_in_bound(v)
        if res != False:
            print(res)
        else:
            print(self.graph.get_next_in_bound(v))

    def get_next_outbound_neighbour(self):
        v = self.readPositiveInteger("Give a vertex: ")
        res = self.graph.get_first_out_bound(v)
        if res != False:
            print(res)
        else:
            print(self.graph.get_next_out_bound(v))

    def minimum_path(self):
        v1 = self.readPositiveInteger("Give a vertex: ")
        v2 = self.readPositiveInteger("Give a vertex: ")
        m = breadth_first_minimum_path(self.graph, v1, v2)
        if m != False:
            p = m[0]
            string = str(v2) + ">-"
            r = p[v2]
            while r != v1:
                string += str(r) + ">-"
                r = p[r]
            string += str(r)
            print(string[::-1])
        else:
            print("No path between these elements")

    def minimum_cost_path(self):
        v1 = self.readPositiveInteger("Give a vertex: ")
        v2 = self.readPositiveInteger("Give a vertex: ")
        m = apsp(self.graph)
        n = pseudo_matrix_multiplication(self.graph.get_matrix(), m)
        for i in range(self.graph.get_nr_of_vertices()):
            for j in range(self.graph.get_nr_of_vertices()):
                if m[i][j] != n[i][j]:
                    print("The graph contains negative cost cycles!")
                    return

        print(m[v1][v2])

    def topologic_sort(self):
        l = actual_topo_sort_dfs(self.graph)
        if len(l) == 0:
            print("Cycle found!")
        for i in range(len(l)):
            l[i] = l[i].get_number()
        print(l)

    def compute_times(self):
        st = compute_times(self.graph)
        if len(st) == 0:
            print("Cycle found!")
        m = 0
        for i in range(len(st)):
            print("Vertex: " + str(st[i].get_number()) + " Earliest start time: " + str(st[i].earliest_start_time) + " Latest start time: " + str(st[i].latest_start_time))
            m = max(m, st[i].earliest_finish_time)
        print("Total time of project: " + str(m))

    def critical_path(self):
        st = compute_times(self.graph)
        if len(st) == 0:
            print("Cycle found!")
        cp = []
        for i in st:
            if i.earliest_start_time == i.latest_start_time:
                cp.append(i.get_number())
        print(cp)


    def MainMenu(self):

        commandDict = {'1': self.print_edges,
                       '2': self.print_nr_of_vertices,
                       '3': self.print_nr_of_edges,
                       '4': self.edge_between,
                       '5': self.inbound_degree_vertex,
                       '6': self.outbound_degree_vertex,
                       '7': self.get_cost_vertex,
                       '8': self.set_cost_vertex,
                       '10': self.get_next_inbound_neighbour,
                       '9': self.get_next_outbound_neighbour,
                       '11': self.minimum_path,
                       '12': self.minimum_cost_path,
                       '13': self.print_vertices,
                       '14': self.topologic_sort,
                       '15': self.compute_times,
                       '16': self.critical_path
                       }

        while True:
            UI.printMenu()
            command = input("Please enter your command: ")
            while not UI.ValidInputCommand(command):
                print("Please enter a valid command!")
                command = input("Please enter your command: ")
            if command == '0':
                return
            commandDict[command]()

ui = UI(D)
ui.MainMenu()












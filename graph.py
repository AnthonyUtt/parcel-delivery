# C950 - Anthony Utt - autt3 - ID#000854797
from table import Table

class Node:
    # The Node class will hold each of our delivery points for 
    # any given city. The object contains an ID, the address 
    # information, and a list of other nodes that are connected 
    # to the current node.

    # init runs in O(1) time
    def __init__(self, id_, address, zip_):
        self.id = id_
        self.address = address
        self.zip = zip_

        # list of connections that extend from this node
        self.connections = []

    # Both add_connection() and get_distance() have a worst-case 
    # runtime of O(M), where M is the number of nodes in our city
    def add_connection(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)

    def get_distance(self, other):
        if other is None:
            return float('inf')
        for connection in self.connections:
            if connection.get_n1() == other or connection.get_n2() == other:
                return connection.get_weight()

    # get_connections and __str__ both have a runtime of O(1)
    def get_connections(self):
        return self.connections

    def __str__(self):
        return self.address + ' ' + self.zip


class Connection:
    # The Connection class is mainly meant to be a lightweight way of 
    # keeping track of the distance between any two nodes. Each of the 
    # methods in this class have a runtime of O(1).
    def __init__(self, n1, n2, weight):
        self.n1 = n1
        self.n2 = n2
        self.weight = weight

    def get_n1(self):
        return self.n1
    
    def get_n2(self):
        return self.n2
    
    def get_weight(self):
        return self.weight

    def __str__(self):
        return 'Between ' + str(self.n1) + ' and ' + str(self.n2) + ', the distance is ' + str(self.weight)


class Graph:
    # The Graph class will be what we use to map our deliveries for the 
    # day. It uses the hash table data structure that we created for this 
    # program to hold the nodes in an efficient and easily-accessible way.
    def __init__(self):
        # we will be re-using the Table class to hold our nodes, 
        # that way we can easily select a node by its ID

        self.nodes = Table()

    def add_node(self, node):
        # this function runs in O(1)
        self.nodes.insert(node.id, node)

    def remove_node(self, node_id):
        # This method won't actually be needed, but for future use, if 
        # we were to serialize the graph object and store it in a 
        # location that could be easily loaded into memory, and we 
        # needed to remove a node if we were no longer delivering 
        # to that address...

        # This function runs in O(1)
        self.nodes.remove(node_id)

    # This function runs in O(1)
    def get_node(self, node_id):
        # This will use the search in the table structure to return 
        # the node using only the node_id
        our_node = self.nodes.get(node_id)
        return our_node

    # This method runs in O(M), where M is the number of nodes in the 
    # graph.
    def get_node_by_address(self, address_, zip_):
        for node in self.nodes.items():
            if node.address == address_ and node.zip == zip_:
                return node
        return None

    # This function runs in O(1)
    def list_nodes(self):
        return self.nodes.items()
    
    # Because we are using a fully connected graph, this method has a 
    # worst-case runtime of approximately O(M^2).
    def list_connections(self):
        items = []
        for node in self.list_nodes():
            for connection in node.get_connections():
                items.append(connection)

        return items


def load(node_list, distance_list, graph):
    # If, in the future, the graph object was serialized to be loaded 
    # more efficiently, this could easily be changed to load the 
    # object directly into memory. For now, though, this method runs 
    # in O(M) time, where M is the number of nodes.

    f = open(node_list, 'r', encoding='utf-8')
    content = f.readlines()

    for i, line in enumerate(content):
        split = line.split(',')
        
        new_node = Node((i + 1), split[0], split[1].strip())

        graph.add_node(new_node)

    # After adding the nodes to the graph, we add connections to nodes
    f = open(distance_list, 'r', encoding='utf-8')
    content = f.readlines()

    for i, line in enumerate(content):
        node1 = graph.get_node((i + 1))
        #print('node1 = ' + str(node1))
        distances = line.split(',')
        for j, distance in enumerate(distances):
            if distance == '0':
                break
            else:
                node2 = graph.get_node(j + 1)
                #print('node2 = ' + str(node2))
                weight = float(distance)

                # Creating connection object and then linking that 
                # connection to each of the relevant nodes. Because 
                # all objects are passed by reference in python, we 
                # know we are modifying the original object and not 
                # copy of it.
                conn = Connection(node1, node2, weight)
                #print('connection created')
                node1.add_connection(conn)
                #print('added to node1')
                node2.add_connection(conn)
                #print('added to node2')
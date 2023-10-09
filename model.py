import numpy as np
from snap import TNEANet

class BaseModel():

    def __init__(self, states, state_strings, state_func_dict):
        self.states = states
        self.state_strings = state_strings
        self.state_func_dict = state_func_dict
        self.G = None
        
    def set_graph(self, G):
        self.G = G
        
    def setup(self, initial_state):
        self.node_states= np.full(self.G.n_nodes, initial_state)
        self.new_states = np.empty(self.G.n_nodes)
        
        
    def iterate(self):
        self.new_states[:] = self.node_states

        for state, func in self.state_func_dict.items():
            nodes = self.G.nodes[self.node_states == state]
            func(self, nodes)

        self.node_states[:] = self.new_states


    def inform(self):
        for state in self.states:
            num = (self.node_states == state).sum()
            print(f"{self.state_strings[state]} ..... {num}")
        print()
        
        
class Graph():
    
    def __init__(self, edges_file):
        nodes = set()
        num_edges = 0
        with open(edges_file, "r") as f:
            for line in f:
                a, b = map(int, line.split())
                nodes.add(a)
                nodes.add(b)
                num_edges += 1
            
        self.node_numbers = np.array(sorted(list(nodes)))
        self.n_nodes = len(self.node_numbers)
        self.nodes = np.arange(self.n_nodes)


        
        self.edges = np.arange(num_edges)
        self.in_nodes = np.empty(num_edges, dtype=int)
        self.out_nodes = np.empty(num_edges, dtype=int)


        id_dict = {self.node_numbers[i]: i  for i in range(self.n_nodes)}
        
        with open(edges_file, "r") as f:
            for i, line in enumerate(f):
                a, b = map(int, line.split())
                self.in_nodes[i] = id_dict[a]
                self.out_nodes[i] = id_dict[b]
                

                
    def get_dest_of_nodes(self, nodes):
        edges = np.isin(self.in_nodes, nodes)
        return self.out_nodes(edges)

    def get_source_of_nodes(self, nodes):
        edges = np.isin(self.out_nodes, nodes)
        return self.in_nodes(edges)
    
    def do_spread(self, nodes, prob):
        edges = np.isin(self.in_nodes, nodes)
        rand = np.random.randn(edges.sum()) < prob
        candidates = self.out_nodes[edges]
        return candidates[rand]

import numpy as np
import pandas as pd

import networkx as nx

class History():
    def __init__(self, model):
        self.model = model 
        self.state_history = [] 
        self.state_numbers = []


    def update(self):
        self.state_history.append(self.model.node_states.copy())
        state_numbers_dict = {
            s: (self.model.node_states == s).sum()
            for s in self.model.states 
        }
        self.state_numbers.append(state_numbers_dict)

    def to_df(self, include_node_states=False):
        df1 = pd.DataFrame(self.state_numbers)
        df1.columns = self.model.state_strings
        if not include_node_states:
            return df1
        
        df2 = pd.DataFrame(self.state_history, columns=self.model.G.node_numbers)
        return pd.concat([df1, df2], axis=1)
        
class BaseModel():

    def __init__(self, states, state_strings, state_func_dict):
        self.states = states
        self.state_strings = state_strings
        self.state_func_dict = state_func_dict
        self.G = None

        self.history = History(self)
        
    def set_graph(self, G):
        self.G = G
        
    def setup(self, initial_state):
        self.node_states= np.full(self.G.n_nodes, initial_state)
        self.new_states = np.empty(self.G.n_nodes)

        self.time_in_state = np.ones(self.G.n_nodes)

        self.history.update()
        
    def iterate(self):
        self.new_states[:] = self.node_states

        for state, func in self.state_func_dict.items():
            nodes = self.G.nodes[self.node_states == state]
            func(nodes)
            
        same_state = self.new_states == self.node_states
        self.node_states[:] = self.new_states
        self.time_in_state[same_state] += 1
        self.time_in_state[same_state == False] = 1
        self.history.update()

    def inform(self):
        for state in self.states:
            num = (self.node_states == state).sum()
            print(f"{self.state_strings[state]} ..... {num}")
        print()


    def history_to_df(self):
        return self.history.to_df()
    
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
        rand = np.random.rand(edges.sum()) < prob
        candidates = self.out_nodes[edges]
        return candidates[rand]

    def to_nx(self):
        graph = nx.MultiGraph()

        for node in self.nodes:
            graph.add_node(self.node_numbers[node])

        for a, b in zip(self.in_nodes, self.out_nodes):
            graph.add_edge(
                self.node_numbers[a],
                self.node_numbers[b]
            )

        return graph

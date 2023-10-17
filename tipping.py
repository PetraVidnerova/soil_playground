import numpy as np

from sir import S, I
from model import BaseModel


class TippingModel(BaseModel):

    states = [S, I]
    state_strings = ["S", "Active"]

    def process_S(self, nodes):

        active_nodes = self.G.nodes[self.node_states == I]

        
        m = self.G.matrix[active_nodes,:][:,nodes]
        
        counts = m.sum(axis=0)
        assert counts.shape[0] == 1
        assert counts.shape[1] == len(nodes)

        a = self.G.matrix[:, nodes]
        all_counts = a.sum(axis=0)
        assert all_counts.shape[0] == 1
        assert all_counts.shape[1] == len(nodes)

        # print(counts)
        # print(all_counts)
        # print()
        excitate = counts > self.threshold*all_counts
        excitate = np.squeeze(np.array(excitate), axis=0)
        
        self.new_states[nodes[excitate]] = I
        
    def __init__(self, threshold):
        self.threshold = threshold # float or numpy array of length number of nodes
        state_func_dict = {S: self.process_S}
        super().__init__(self.states, self.state_strings, state_func_dict)
    
        
    

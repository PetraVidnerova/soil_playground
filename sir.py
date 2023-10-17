import numpy as np

from model import BaseModel

S = 0
I = 1
R = 2

class SIR(BaseModel):

    states = [S, I, R]
    state_strings = ["S", "I", "R"]

    def process_S(self, nodes):
        infected_nodes = self.G.nodes[self.node_states == I]
        new_infected_nodes = self.G.do_spread(infected_nodes, self.beta)

        new_infected_nodes = np.intersect1d(nodes, new_infected_nodes)
        if new_infected_nodes.size > 0:
            self.new_states[new_infected_nodes] = I

    def process_I(self, nodes):
        if nodes.size > 0:
            self.new_states[nodes] = R


    def __init__(self, beta):
        self.beta = beta
        state_func_dict = {S: self.process_S, I: self.process_I}
        super().__init__(self.states, self.state_strings, state_func_dict)



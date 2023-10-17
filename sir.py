import numpy as np
from random import randrange

from model import Graph, BaseModel

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

    
        
def main():
    print("Creating graph .... ", end="", flush=True)
    g = Graph("twitter_data/twitter_combined.txt")
    print("ok", flush=True)
    print("Nodes:", g.n_nodes)
    print("Edges:", g.edges.size)

    beta = 0.1
    
    model = SIR(beta)
    model.set_graph(g)
    model.setup(S)
    model.node_states[randrange(g.n_nodes)] = I


    for i in range(200):
        print(f"Iteration {i}.")
        model.iterate()
        model.inform()


    print(model.history_to_df())

    
if __name__ == "__main__":
    main()

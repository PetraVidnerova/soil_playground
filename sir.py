import numpy as np
from random import randrange
from tqdm import tqdm 

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


def run(g, seed):
    beta = 0.1
    
    model = SIR(beta)
    model.set_graph(g)
    model.setup(S)
    model.node_states[seed] = I


    
    for i in range(100):
#        print(f"Iteration {i}.")
        model.iterate()
#        model.inform()


    df = model.history_to_df()
#    print(df)

    number_of_infected = df.loc[100, "R"]
    return number_of_infected
        
def main():
    print("Creating graph .... ", end="", flush=True)
    g = Graph("twitter_data/twitter_combined.txt")
    print("ok", flush=True)
    print("Nodes:", g.n_nodes)
    print("Edges:", g.edges.size)

    for _ in range(10):
        seed = randrange(g.n_nodes)
        number_of_infected = []
        for _ in tqdm(range(100)):
            number_of_infected.append(run(g, seed))
            
        print(g.node_numbers[seed],  ":", sum(number_of_infected)/len(number_of_infected))
    
if __name__ == "__main__":
    main()

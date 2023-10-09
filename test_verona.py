from datetime import datetime
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

from model import Graph, BaseModel

EMPTY = 0
INFORMED = 1
INFORMING = 2
DEAD = 3

states = [EMPTY, INFORMED, INFORMING, DEAD]

state_strings = ["EMPTY", "INFORMED", "INFORMING", "DEAD"]


def empty(model, nodes):

    informing_nodes = model.G.nodes[model.node_states == INFORMING]
    informed_nodes = model.G.do_spread(informing_nodes, 0.1)
    
    informed_nodes = np.intersect1d(nodes, informed_nodes)
    if informed_nodes.size > 0:
        model.new_states[informed_nodes] = INFORMED
    
def informed(model, nodes):

    informing_nodes = nodes[model.time_in_state[nodes] % 7 == 0]

    if informing_nodes.size > 0:
        model.new_states[informing_nodes] = INFORMING
       
def informing(model, nodes):
    model.new_states[nodes] = INFORMED

    
state_func_dict = {
    EMPTY: empty,
    INFORMED: informed,
    INFORMING: informing
}


g = Graph("data/edges.txt")

model = BaseModel(states, state_strings, state_func_dict)
model.set_graph(g)
model.setup(EMPTY)
model.node_states[0] = INFORMED

for i in range(200):
    model.iterate()
    model.inform()

df = model.states_to_df()

nx_graph = g.to_nx()
layout = nx.kamada_kawai_layout(nx_graph)

for i, row in df.iterrows():

    if i == 50:
        break
    nodes = g.node_numbers[np.where(
        np.logical_or(row == INFORMED, row == INFORMING)
    )[0]]
#    print(nodes)

    nx.draw_networkx(nx_graph, layout, node_color='blue',  node_size=20)
    nx.draw_networkx(nx_graph, layout, nodelist=list(nodes),node_color="red", node_size=20)
    plt.savefig(f"verona_postaru_{i:03d}.png", dpi=200)
    print(f"verona_postaru_{i:03d}.png saved.")

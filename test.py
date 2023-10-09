from datetime import datetime
import numpy as np

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
    flip_coin = np.random.rand(nodes.size) < 0.1

    informing_nodes = nodes[flip_coin]
    if informing_nodes.size > 0:
        model.new_states[informing_nodes] = INFORMING

    dead_nodes = nodes[model.time_in_state[nodes] > 7]
    if dead_nodes.size > 0:
        model.new_states[dead_nodes] = DEAD
        
def informing(model, nodes):
    model.new_states[nodes] = DEAD

    
state_func_dict = {
    EMPTY: empty,
    INFORMED: informed,
    INFORMING: informing
}


g = Graph("twitter_data/twitter_combined.txt")

model = BaseModel(states, state_strings, state_func_dict)
model.set_graph(g)
model.setup(EMPTY)
model.node_states[5] = INFORMED

for i in range(200):
    model.iterate()
    model.inform()


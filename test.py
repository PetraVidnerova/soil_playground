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
    """ Function that takes care of nodes that are in state EMPTY.
    List of EMPTY nodes is given by parameter nodes.
    EMPTY nodes may get the information from INFORMING node and become INFORMED. """    

    # find nodes that gets information from those in state INFORMING 
    informing_nodes = model.G.nodes[model.node_states == INFORMING]
    informed_nodes = model.G.do_spread(informing_nodes, 0.1)

    # those who are EMPTY (nodes) and got information (informed nodes) change state to INFORMED
    informed_nodes = np.intersect1d(nodes, informed_nodes)
    if informed_nodes.size > 0:
        model.new_states[informed_nodes] = INFORMED

def informed(model, nodes):
    """ Function that takes care of nodes that are in state INFORMED.
    List of INFORMED nodes is given by parameter nodes.
    INFORMED nodes decide if to change the state to INFORMING or to 
    stay INFORMED. After 7 days they become DIED. """ 

    # informed nodes flip a coin
    flip_coin = np.random.rand(nodes.size) < 0.1

    # those with possitive coin will become informing 
    informing_nodes = nodes[flip_coin]
    if informing_nodes.size > 0:
        model.new_states[informing_nodes] = INFORMING

    # those who are in this state more than 7 days will become DEAD
    dead_nodes = nodes[model.time_in_state[nodes] > 7]
    if dead_nodes.size > 0:
        model.new_states[dead_nodes] = DEAD
        
def informing(model, nodes):
    """ Function that takes care of nodes that are in state INFORMING.
    List of INFORMING nodes is given by parameter nodes.
    INFORMING may spread information and imediately next time step they become DIED.
    So they can spread the information only once. 
    """
    
    # nodes are INFORMING for only one time step,
    # then they become DEAD 
    model.new_states[nodes] = DEAD

    
state_func_dict = {
    EMPTY: empty,
    INFORMED: informed,
    INFORMING: informing
}

print("Creating graph .... ", end="", flush=True)
g = Graph("twitter_data/twitter_combined.txt")
print("ok", flush=True)
print("Nodes:", g.n_nodes)
print("Edges:", g.edges.size)


model = BaseModel(states, state_strings, state_func_dict)
model.set_graph(g)
model.setup(EMPTY)
model.node_states[5] = INFORMED

for i in range(200):
    print(f"Iteration {i}.")
    model.iterate()
    model.inform()


print(model.history_to_df())

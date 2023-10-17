
from random import randrange
from tqdm import tqdm 
import click

from model import Graph
from sir import SIR, S, I
from tipping import TippingModel


def run(g, seed, model, parameter, target_state):

    model = model(parameter)
    model.set_graph(g)
    model.setup(S)
    model.node_states[seed] = I

    iters = 150
    for i in range(iters):
        model.iterate()
#        model.inform()

    df = model.history_to_df()
    number_of_infected = df.loc[iters, target_state]
    
    return number_of_infected
        

@click.command()
@click.option("-m", "--model_type", default="SIR")
def main(model_type):
    
    print("Creating graph .... ", end="", flush=True)
    g = Graph("twitter_data/twitter_combined.txt")
    print("ok", flush=True)
    print("Nodes:", g.n_nodes)
    print("Edges:", g.edges.size)    


    if model_type == "SIR":
        model = SIR
        parameter = 0.1
        target_state = "R"
        repeat = 50
    elif model_type == "TippingModel":
        model = TippingModel
        parameter = 0.1
        target_state = "Active"
        repeat = 1
        
    for _ in range(15):
        seed = randrange(g.n_nodes)
        number_of_infected = []
        for _ in tqdm(range(repeat)):
            number_of_infected.append(run(g, seed, model, parameter, target_state))
            
        print(g.node_numbers[seed],  ":", sum(number_of_infected)/len(number_of_infected))

        
if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import soil
from soil import state

def load_verona_graph():
    nodes = pd.read_csv("data/raj-nodes.csv")
    
    G = nx.Graph()

    node_labels = {} 
    for i, row in nodes.iterrows():
        G.add_node(row["type"],
                   label=row["label"],
                   sex=row["sex"],
                   age=row["age"]
                   )
        node_labels[row["type"]] = row["label"]


    edges = pd.read_csv("data/raj-edges.csv")
    for i, row in edges.iterrows():
        G.add_edge(row["vertex1"], row["vertex2"])
        
    return G, node_labels

def draw_graph(G, node_labels=None):
    nx.draw_networkx(G, nx.spring_layout(G), node_color='red', labels=node_labels)
    plt.show()


class VeronaAgent(soil.Agent):
    is_romeo = False
    is_julie = False
    got_news = False
    
    @state(default=not is_romeo)
    def empty(self):
        if self.is_romeo:
            return self.informed
        
        if self.got_news:
            if self.is_julie:
                self.model.julie_informed = True
                print("JULIE ", id(self.model))
            self.model.informed_count += 1
            return self.informed
            
    @state(default=is_romeo)
    def informed(self):
        for neighbor in self.iter_neighbors(state_id=self.empty.id):
            if self.prob(self.model.prob_news_spread):
                neighbor.got_news = True
        return self.delay(7) 


class VeronaNetwork(soil.Environment):

    prob_news_spread = 0.01
    event_time = 1
    informed_count = 0
    julie_informed = False
    
    def init(self):
        
        self.G, self.node_labels = load_verona_graph()
        self.populate_network(VeronaAgent)
        self.agent(node_id=1).is_romeo = True
        self.agent(node_id=2).is_julie = True
        self.add_model_reporter('prob_news_spread')
        self.add_agent_reporter('state_id', lambda a: getattr(a, "state_id", None))
    

def main():
    # G, node_labels = load_verona_graph()
    # draw_graph(G, node_labels)

    model = VeronaNetwork()

    print("MODEL", id(model))
    
    it = model.run(max_time=200, name="Verona", dump=True, overwrite=True, iterations=1, matrix=dict())
    #    it[0].model_df()
    print(it[0].model_df())
    print(it)

    print(model.informed_count)
    print(model.julie_informed)
    
if __name__ == "__main__":
    main()

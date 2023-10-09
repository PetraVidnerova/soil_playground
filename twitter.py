import random 
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import soil
from soil import state

def load_edges():

    G = nx.Graph()

    with open("twitter_data/twitter_combined.txt", "r") as f:
        for line in f:
            a, b = map(int, line.split())

            G.add_edge(a, b)

    return G
            
    # node_labels = {} 
    # for i, row in nodes.iterrows():
    #     G.add_node(row["type"],
    #                label=row["label"],
    #                sex=row["sex"],
    #                age=row["age"]
    #                )
    #     node_labels[row["type"]] = row["label"]


    # edges = pd.read_csv("data/raj-edges.csv")
    # for i, row in edges.iterrows():
    #     G.add_edge(row["vertex1"], row["vertex2"])
        
    # return G, node_labels

def draw_graph(G, node_labels=None):
    nx.draw_networkx(G, nx.spring_layout(G), node_color='red', labels=node_labels)
    plt.show()


class TestAgent(soil.Agent):
    is_source = False
    got_news = False

    def init(self):
        self.news_sent = False

    @state(default=not is_source)
    def empty(self):
        if self.is_source:
            return self.informed
        
        if self.got_news:
            return self.informed
            
    @state(default=is_source)
    def informed(self):
        if not self.news_sent or self.is_source:
            for neighbor in self.iter_neighbors(state_id=self.empty.id):
                if self.prob(self.model.prob_news_spread):
                    neighbor.got_news = True
            self.news_sent = True
        return self.delay(7) 


class TestNetwork(soil.Environment):

    prob_news_spread = 0.1
    event_time = 1
    informed_count = 0
    
    def init(self):
        
        self.G  = load_edges()
        self.populate_network(TestAgent)
        random_node = random.choice(list(self.G.nodes()))
        self.agent(node_id=random_node).is_source = True
        self.add_model_reporter('prob_news_spread')
        self.add_agent_reporter('state_id', lambda a: getattr(a, "state_id", None))
    

def main():

    
    model = TestNetwork()

    # print("MODEL", id(model))
    
    it = model.run(max_time=200, name="Test", dump=True, overwrite=True, iterations=10, matrix=dict())
    it[0].model_df()
    print(it[0].model_df())
    # print(it)

    # print(model.informed_count)
    # print(model.julie_informed)
    
if __name__ == "__main__":
    main()

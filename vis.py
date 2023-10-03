from soil import analysis
import matplotlib.pyplot as plt 
import numpy as np
from verona import load_verona_graph
import networkx as nx

res = analysis.read_sql(name="Verona", include_agents=True)

print(res[3])


result = res[3]

result["informed"] = result["state_id"] != "empty"

num_informed = result.groupby("step")["informed"].sum()


# num_informed.plot()
# plt.show()


result = result.reset_index().drop(columns=["simulation_id", "params_id", "iteration_id", "state_id"])
print(result)


result = result.pivot(index=["step"], columns=["agent_id"], values="informed").astype(int)
print(result)


G, node_labels = load_verona_graph()
layout = nx.kamada_kawai_layout(G)

for i, row in result.iterrows():

    if i >= 50:
        break
    
    nodes = np.where(row == 1)[0]
    print(nodes)
    
    nx.draw_networkx(G, layout, node_color='blue',  node_size=20)
    nx.draw_networkx(G, layout, nodelist=list(nodes),node_color="red", node_size=20)
    plt.savefig(f"verona_{i:03d}.png", dpi=200)


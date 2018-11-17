import numpy as np
import snap
from LoadGraph import loadGraph


def createList(G, node_id_to_value):
	acquired_companies = set()

	for EI in G.Edges():
		acquired_companies.add(node_id_to_value[EI.GetDstNId()])

	acquired_companies = np.array(list(acquired_companies))

	np.save("acquired_companies", acquired_companies)



def main():
	path_to_graph = "../graphs/acquisitions_to_companies_directed/acquisitions_to_companies.txt"
	path_to_nodeId_to_value = "../graphs/acquisitions_to_companies_directed/node_id_to_value.npy"
	
	G = loadGraph(path_to_graph)
	node_id_to_value = np.load(path_to_nodeId_to_value)
	node_id_to_value = node_id_to_value.item()

	createList(G,  node_id_to_value)


if __name__ == "__main__":
	main()
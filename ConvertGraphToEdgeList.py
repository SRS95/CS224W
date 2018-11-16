from LoadGraph import loadGraph
import numpy as np
import argparse


def createAndSaveEdgeList(G, fname):
	# There will be one edge per row
	result = np.zeros((G.GetEdges(), 2), dtype=int)

	index = 0
	for EI in G.Edges():
		result[index, 0] = EI.GetSrcNId()
		result[index, 1] = EI.GetDstNId()
		index += 1


	output_name_tokens = fname.split('.')
	print output_name_tokens
	output_name = ""
	for i in range(len(output_name_tokens) - 1):
		curr_token = output_name_tokens[i]
		if curr_token == '': curr_token = '.'
		output_name = output_name + curr_token

	output_name = output_name + ".edgelist"
	np.savetxt(output_name, result, fmt='%i', delimiter="\t")



def main():
	parser = argparse.ArgumentParser(description='Convert a graph to a .edgelist file (for node2vec).')
	parser.add_argument('filename', type=str, help='Path to the .graph file containing the graph of the form ../graphs/graphname_graphtype/graphname')
	args = parser.parse_args()

	fname = args.filename
	G = loadGraph(fname)
	createAndSaveEdgeList(G, fname)

if __name__ == "__main__":
	main()
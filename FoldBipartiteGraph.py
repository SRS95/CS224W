'''
Fold a bipartite graph.
'''
import snap
import numpy as np
import pandas as pd
import sys
import os
import argparse


def foldGraph(G, source_class, dest_class, reverse):
	if reverse:
		source_class = dest_class.copy()
		dest_class = source_class.copy()

	G_folded = snap.TUNGraph.New()
	for nodeId in source_class: G_folded.AddNode(nodeId)

	for dest_node in dest_class:
		curr_NI = G.GetNI(nodeId)
		curr_deg = curr_NI.GetDeg()
		for neighborIndex1 in range(curr_deg):
			nbr1 = curr_NI.GetNbrNId(neighborIndex1)
			for neighborIndex2 in range(neighborIndex1 + 1, curr_deg):
				nbr2 = curr_NI.GetNbrNId(neighborIndex2)
				if not G.IsEdge(nbr1, nbr2): G.AddEdge(nbr1, nbr2)

	print "There are " + str(G_folded.GetNodes()) + " nodes in the folded graph."
	print "There are " + str(G_folded.GetEdges()) + " edges in the folded graph."
	
	return G_folded


def getBipartiteClasses(fname):
	fname_split = fname.split('/')
	folder_path = ""
	for path_elem in range(len(fname_split) - 1):
		folder_path = folder_path + fname_split[path_elem] + '/'

	source_class = np.load(folder_path + '/bipartite_source_class.npy')
	dest_class = np.load(folder_path + '/bipartite_dest_class.npy')

	return source_class, dest_class


def loadGraph(fname):
	file_check = fname.split('.')

	is_txt_file = file_check[len(file_check) - 1] == "txt"
	is_graph_file = file_check[len(file_check) - 1] == "graph"

	G = None

	if not is_txt_file and not is_graph_file:
		print "File must be a .txt or .graph file"
		return G

	if not os.path.isfile(fname):
		print "File does not exist"
		return G

	if is_txt_file:
		G = snap.LoadEdgeList(fname)

	else:
		FIn = snap.TFIn(fname)
		G = snap.TNEANet.Load(FIn)

	source_class, dest_class = getBipartiteClasses(fname)

	return G, source_class, dest_class


def main():
	parser = argparse.ArgumentParser(description='Fold a bipartite graph.')
	parser.add_argument('filename', type=str, help='Path to the .txt or .graph file containing the bipartite graph of the form ../graphs/graphname_graphtype/graphname')
	parser.add_argument('--reverse', type=bool, dest='reverse', default=False, help='Set to True if you want to fold in the reverse direction')
	args = parser.parse_args()

	G, source_class, dest_class = loadGraph(args.filename)
	
	if G == None: return
	else: foldGraph(G, source_class, dest_class, args.reverse)


if __name__ == "__main__":
	main()


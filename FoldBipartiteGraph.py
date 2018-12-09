'''
Fold a bipartite graph.

Resulting graph is a graph of just the destination nodes
in which there's an edge betweend dest nodes A and B if they 
have a source node in common
'''
import snap
import numpy as np
import pandas as pd
import sys
import os
import argparse
from tqdm import tqdm



def foldGraph(G, source_class, dest_class, reverse):
	if reverse:
		temp = source_class.copy()
		source_class = dest_class.copy()
		dest_class = temp.copy()

		for EI in G.Edges():
			curr_source = EI.GetSrcNId()
			curr_dest = EI.GetDstNId()

			G.DelEdge(curr_source, curr_dest)
			G.AddEdge(curr_dest, curr_source)


	G_folded = snap.TUNGraph.New()
	for nodeId in dest_class: 
		G_folded.AddNode(nodeId)

	for source_node in source_class:
		curr_NI = G.GetNI(source_node)
		curr_deg = curr_NI.GetOutDeg()

		for neighborIndex1 in range(curr_deg):
			nbr1 = curr_NI.GetOutNId(neighborIndex1)
			if nbr1 in source_class: continue  # Handle case where bipartite structure is violated
			for neighborIndex2 in range(neighborIndex1 + 1, curr_deg):
				nbr2 = curr_NI.GetOutNId(neighborIndex2)
				if nbr2 in source_class: continue # Handle case where bipartite structure is violated
				if not G_folded.IsEdge(nbr1, nbr2): 
					G_folded.AddEdge(nbr1, nbr2)

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
		G = snap.LoadEdgeList(snap.PNGraph, fname)

	else:
		FIn = snap.TFIn(fname)
		G = snap.TNEANet.Load(FIn)

	source_class, dest_class = getBipartiteClasses(fname)

	return G, source_class, dest_class


def saveGraph(G, fname, reverse):
	fname_split = fname.split('/')
	path = ""
	
	for path_elem in range(len(fname_split) - 1):
		path = path + fname_split[path_elem] + '/'

	if reverse: 
		path = path + fname_split[len(fname_split) - 2] + "_folded_reverse_order.graph"
	else: 
		path = path + fname_split[len(fname_split) - 2] + "_folded.graph"

	FOut = snap.TFOut(path)
	G.Save(FOut)
	FOut.Flush()


def main():
	parser = argparse.ArgumentParser(description='Fold a bipartite graph.')
	parser.add_argument('filename', type=str, help='Path to the .txt or .graph file containing the bipartite graph of the form ../graphs/graphname_graphtype/graphname')
	parser.add_argument('--reverse', type=bool, dest='reverse', default=False, help='Set to True if you want to fold in the reverse direction')
	args = parser.parse_args()

	fname = args.filename
	reverse = args.reverse
	G, source_class, dest_class = loadGraph(fname)

	if G == None: 
		return

	else: 
		G_folded = foldGraph(G, source_class, dest_class, reverse)
		saveGraph(G_folded, fname, reverse)


if __name__ == "__main__":
	main()


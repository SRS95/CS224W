import snap
import numpy as np
import os

def loadGraph(graph_name, ):
	file_check = graph_name.split('.')
	fname = "../graphs/" + file_check[0] + '/' + graph_name

	is_txt_file = file_check[len(file_check) - 1] == "txt"
	is_graph_file = file_check[len(file_check) - 1] == "graph"

	G = None

	if not is_txt_file and not is_graph_file:
		print "File must be a .txt or .graph file"
		return G

	if not os.path.isfile(fname):
		print "File does not exist"
		return G

	graph_check = fname.split('/')
	graph_check = graph_check[len(graph_check) - 2].split('_')
	is_directed = graph_check[len(graph_check) - 1] == "directed"

	if is_txt_file and is_directed:
		G = snap.LoadEdgeList(snap.PNGraph, fname)

	elif is_txt_file and not is_directed:
		G = snap.LoadEdgeList(snap.PUNGraph, fname)

	else:
		check_if_folded = graph_name.split('_')
		folded = False
		for token in check_if_folded:
			if token == "folded":
				folded = True
				break

		FIn = snap.TFIn(fname)
		if folded: G = snap.TUNGraph.Load(FIn)
		else: G = snap.TNEANet.Load(FIn)

	return G
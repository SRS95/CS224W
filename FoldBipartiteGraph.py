'''
Fold a bipartite graph.
'''


import snap
import numpy as np
import pandas as pd
import sys
import os
import argparse

def foldGraph(G):
	G_folded = snap.PUNGraph.New()

	progressCounter = 0

	for key, value in genesToDiseases.iteritems():
		# Report progress
		progressCounter += 1
		print "On gene " + str(progressCounter) + " of 17,074"

		#Update most common gene if necessary
		currGeneNumDiseases = len(value)
		if currGeneNumDiseases > mostCommonGene:
			mostCommonGene = currGeneNumDiseases

		# Add nodes and edges to HDN
		for diseaseId1 in value:
			diseaseId1 *= -1

			if not HDN.IsNode(diseaseId1):
				HDN.AddNode(diseaseId1)

			for diseaseId2 in value:
				diseaseId2 *= -1

				if diseaseId2 == diseaseId1:
					continue
				
				if not HDN.IsNode(diseaseId2):
					HDN.AddNode(diseaseId2)

				if not HDN.IsEdge(diseaseId1, diseaseId2):
					HDN.AddEdge(diseaseId1, diseaseId2)


	print "Folded graph has a total of " + str(HDN.GetNodes()) + " nodes"
	print "Folded graph has a total of " + str(HDN.GetEdges()) + " edges"

	return HDN


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

	return G

def main():
	parser = argparse.ArgumentParser(description='Fold a bipartite graph.')
	parser.add_argument('filename', type=str, help='Path to the .txt or .graph file containing the bipartite graph of the form ../graphs/graphname_graphtype/graphname')
	parser.add_argument('--reverse', type=bool, dest='reverse', default=False, help='Set to True if you want to fold in the reverse direction')
	args = parser.parse_args()


	G = loadGraph(args.filename)
	if G == None: return
	else: foldGraph(G, args.reverse)


if __name__ == "__main__":
	main()


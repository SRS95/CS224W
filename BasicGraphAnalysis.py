'''
Author: Sam Schwager
Last Modified: 11/6/2018

Read in a graph and perform some basic
analysis using built in snap functions
'''

import snap
import numpy as np
import pandas as pd
import sys
import os
import argparse


def analyzeGraph(G):
    nodeCount = G.GetNodes()
    edgeCount = G.GetEdges()
    print "Number of nodes in the network: ", nodeCount
    print "Number of Edges in the network: ", edgeCount
    print "Graph Density: ", (2.0*edgeCount)/(nodeCount*(nodeCount-1))
    print "Cluster Coefficient: ", snap.GetClustCf(G)
        
#            Components = snap.TCnComV()
#            snap.GetWccs(G, Components)
#            number_of_wccs = 0
#            for comp in Components: number_of_wccs+= 1
#            print "Number of weakly connected components: ", number_of_wccs
#            MaxWcc = snap.GetMxWcc(G)
#            print "Number of Nodes in the largest weakly connected component:", MaxWcc.GetNodes()
#            print "Number of Edges in the largest weakly connected component: ", MaxWcc.GetEdges()
#            print "Cluster Coefficient: ", snap.GetClustCf(G)
    return


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

	graph_check = fname.split('/')
	graph_check = graph_check[len(graph_check) - 2].split('_')
	is_directed = graph_check[len(graph_check) - 1] == "directed"

	if is_txt_file and is_directed:
		G = snap.LoadEdgeList(snap.PNGraph, fname)

	elif is_txt_file and not is_directed:
		G = snap.LoadEdgeList(snap.PUNGraph, fname)

	else:
		FIn = snap.TFIn(fname)
		G = snap.TNEANet.Load(FIn)

	return G


def main():
	if len(sys.argv) != 2:
		print "Must enter a valid .graph or .txt file name after the name of the Python script and nothing else"
	
	else:
		fname = sys.argv[1]

		G = loadGraph(fname)
		if G == None: return
		else: analyzeGraph(G)


if __name__ == "__main__":
	main()

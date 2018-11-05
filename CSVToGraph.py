import snap
import numpy as np
import pandas as pd
import sys
import os


def createTabSeparatedGraph(data, valueToNodeId):
	result = np.zeros(data.shape, dtype=int)

	for i in range(data.shape[0]):
		for j in range(data.shape[1]):
			result[i, j] = valueToNodeId[data[i, j]]

	return result


def createNodeIDs(data):
	result = {}
	currNodeId = 0

	for row in data:
		for value in row:
			if value not in result:
				result[currNodeId] = value
				currNodeId += 1

	return result
	

def loadData(fname, graph_name, undirected, weighted, weight_col, source_col, dest_col):
	# Make a folder to store all of the files for this graph
	os.mkdir(graph_name)

	cols = [source_col, dest_col]
	if weighted: cols.append(weight_col)

	df =  pd.read_csv(fname, usecols=cols, header=0)
	df = df.dropna()

	# Convert to numpy array
	data = df.values

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(data)
	np.save(graph_name + "/node_id_to_vale", nodeIdToValue)

	# Create a tab separated representation of the graph
	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems()}
	tabSeparatedGraph = createTabSeparatedGraph(data, valueToNodeId)

	# Save the graph to the folder so that it can be loaded in the future
	tabSeparatedGraphTitle = graph_name + '/' + graph_name + ".txt"
	np.savetxt(tabSeparatedGraphTitle, tabSeparatedGraph, fmt='%i', delimiter="\t")


def main():
	if len(sys.argv) == 1:
		print "Must enter a CSV file name"
	else:
		fname = sys.argv[1]

		graph_name = raw_input("What do you want to name this graph?")
		undirected = True if raw_input("Undirected? (y/n)") == 'y' else False
		weighted = True if raw_input("Weighted? (y/n)") == 'y' else False
		weight_col = None
		if weighted:
			weight_col = int(raw_input("Column index for the weights? (first column is index 0)"))
		source_col = int(raw_input("Column index for the source nodes? (first column is index 0)"))
		dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0)"))

		loadData(fname, graph_name, undirected, weighted, weight_col, source_col, dest_col)


if __name__ == "__main__":
	main()
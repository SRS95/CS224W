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
	

def createNormalGraph(fname, graph_name, undirected, source_col, dest_col):
	graph_type = "undirected" if undirected else "directed"
	# Make a folder to store all of the files for this graph
	os.mkdir("../" + graph_name + '_' + graph_type)

	cols = [source_col, dest_col]
	if weighted: cols.append(weight_col)

	df =  pd.read_csv(fname, usecols=cols, header=0)
	df = df.dropna()

	# Convert to numpy array
	data = df.values

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(data)
	np.save("../" + graph_name + "/node_id_to_vale", nodeIdToValue)

	# Create a tab separated representation of the graph
	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems()}
	tabSeparatedGraph = createTabSeparatedGraph(data, valueToNodeId)

	# Save the graph to the folder so that it can be loaded in the future
	tabSeparatedGraphTitle = "../" + graph_name + '/' + graph_name + ".txt"
	np.savetxt(tabSeparatedGraphTitle, tabSeparatedGraph, fmt='%i', delimiter="\t")


def createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs):
	os.mkdir("../" + graph_name + '_' + "TNEANet")

	G = snap.TNEANet.New()
	G.AddNode(0)
	G.AddNode(1)
	G.AddEdge(0, 1)
	G.AddEdge(0, 1)
	G.AddIntAttrN("test")
	G.AddIntAttrDatN(0, 10, "test")
	print G.GetIntAttrDatN(0, "test")
	return


def main():
	if len(sys.argv) == 1:
		print "Must enter a CSV file name"
	else:
		fname = sys.argv[1]

		print "We will now use the data in " + fname + " to form a graph"
		graph_name = raw_input("What do you want to name this graph? ")

		print "Now you need to choose a graph type"
		print "Enter 0 for TUNGraph"
		print "Enter 1 for TNGraph"
		print "Enter 2 for TNEANet"
		graph_type = int(raw_input("What type of graph do you want? "))

		if graph_type == 2:
			source_col = int(raw_input("Column index for the source nodes? (first column is index 0) "))
			dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0) "))

			edgeAttrs = {}
			sourceAttrs = {}
			destAttrs = {}

			print "Since you have chosen TNEANet, you now need to declare any node and edge attributes"
			print "Note that if this is a weighted graph you should declare an edge attribute named weight with the column index of the edge weights"
			print ""
			print "We will begin with edge attributes"
			print "First enter the name of the attribute"
			print "Then enter the column index of the attribute"
			while True:
				if raw_input("New edge attribute?(y/n) ") == 'n': break
				key = raw_input("Edge attribute name ")
				val = raw_input("Edge attribute column index (first column is index 0) ")
				edgeAttrs[key] = val


			print "Now moving on to source node attributes"
			while True:
				if raw_input("New source node attribute?(y/n) ") == 'n': break
				key = raw_input("Source node attribute name ")
				val = raw_input("Source node attribute column index (first column is index 0) ")
				sourceAttrs[key] = val


			print "Now moving on to destination node attributes"
			while True:
				if raw_input("New destination node attribute?(y/n) ") == 'n': break
				key = raw_input("Destination node attribute name ")
				val = raw_input("Destination node attribute column index (first column is index 0) ")
				destAttrs[key] = val

			createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs)


		else:
			undirected = True if graph_type == 0 else False
			source_col = int(raw_input("Column index for the source nodes? (first column is index 0) "))
			dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0) "))
			createNormalGraph(fname, graph_name, undirected, source_col, dest_col)

if __name__ == "__main__":
	main()
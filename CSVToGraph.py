'''
Author: Sam Schwager
Last Modified: 11/5/2018

This scipt generates arbitrarily complex graphs from CSV files,
giving users the flexibility to choose which columns from the
CSV they want to be incorporated into the graph. Graphs are
created using the SNAP.py library, and users are able to choose
among the TUNGraph, TNGraph, and TNEANet graph/network types.
'''


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

# Takes in a 2-column matrix of the objects
# we are treating as nodes in our graph.
# Generates IDs for all of them.
def createNodeIDs(data):
	result = {}
	visited = set()
	currNodeId = 0

	for row in data:
		for value in row:
			if value not in visited:
				result[currNodeId] = value
				currNodeId += 1
				visited.add(value)
				
	return result
	

def createNormalGraph(fname, graph_name, undirected, source_col, dest_col):
	graph_type = "undirected" if undirected else "directed"
	# Make a folder to store all of the files for this graph
	os.mkdir("../" + "graphs/" + graph_name + '_' + graph_type)

	cols = [source_col, dest_col]

	df =  pd.read_csv(fname, usecols=cols, header=0)
	df = df.dropna()

	# Convert to numpy array
	data = df.values

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(data)
	np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/node_id_to_value", nodeIdToValue)

	# Create a tab separated representation of the graph
	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems()}
	tabSeparatedGraph = createTabSeparatedGraph(data, valueToNodeId)

	# Save the graph to the folder so that it can be loaded in the future
	tabSeparatedGraphTitle = "../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".txt"
	np.savetxt(tabSeparatedGraphTitle, tabSeparatedGraph, fmt='%i', delimiter="\t")



def addNodeAttrs(G, attrs, data, col):
	for key, value in attrs.iteritems():
		attribute_type = value[1]
		if attribute_type == 0:
			G.AddIntAttrN(key)
		elif attribute_type == 1:
			G.AddIntAttrN(key)
		elif attribute_type == 2:
			G.AddIntAttrN(key)

		attribute_col_index = value[0]
		for row in data:
			curr_nodeId = valueToNodeId[row[col]]
			if attribute_type == 0:
				G.AddIntAttrDatN(curr_nodeId, row[attribute_col_index], key)
			elif attribute_type == 1:
				G.AddFltAttrDatN(curr_nodeId, row[attribute_col_index], key)
			elif attribute_type == 2:
				G.AddStrAttrDatN(curr_nodeId, row[attribute_col_index], key)

			

def addEdgeAttrs(G, attrs, data, edgeIdToDataRow):
	for key, value in attrs.iteritems():
		attribute_type = value[1]
		if attribute_type == 0:
			G.AddIntAttrE(key)
		elif attribute_type == 1:
			G.AddIntAttrE(key)
		elif attribute_type == 2:
			G.AddIntAttrE(key)

		attribute_col_index = value[0]
		for EI in G.Edges():
			curr_edgeId = EI.GetId()
			curr_row = data[edgeIdToDataRow[curr_edgeId]]

			if attribute_type == 0:
				G.AddIntAttrDatE(curr_edgeId, curr_row[attribute_col_index], key)
			elif attribute_type == 1:
				G.AddFltAttrDatE(curr_edgeId, curr_row[attribute_col_index], key)
			elif attribute_type == 2:
				G.AddStrAttrDatE(curr_edgeId, curr_row[attribute_col_index], key)

		


def createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs):
	graph_type = "TNEANet"
	os.mkdir("../" + "graphs/" + graph_name + '_' + graph_type)
	
	# Don't choose specific columns here because we may have node/edge attributes
	df =  pd.read_csv(fname, header=0)
	df = df.dropna()

	# Convert to numpy array
	data = df.values
	nodeData = np.concatenate((data[:, [source_col]], data[:, [dest_col]]), axis=1)

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(nodeData)
	np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/node_id_to_value", nodeIdToValue)

	# Create the graph
	G = snap.TNEANet.New()

	# Add the nodes
	for nodeId in nodeIdToValue.keys():
		G.AddNode(nodeId)

	# Add the edges
	# This data structure will be useful when adding edge attributes
	# Because otherwise we would need to loop over all rows until we
	# found the one corresponding to the current edge and we also
	# need to allow for multiedges
	edgeIdToDataRow = {}
	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems()}
	for rowIndex in range(data.shape[0]):
		currRow = data[rowIndex]
		currEdgeId = G.AddEdge(valueToNodeId[currRow[source_col]], valueToNodeId[currRow[dest_col]])
		edgeIdToDataRow[currEdgeId] = rowIndex

	# Add the edge attributes
	addEdgeAttrs(G, sourceAttrs, data, edgeIdToDataRow)

	# Add the source node attributes
	addNodeAttrs(G, sourceAttrs, data, source_col)
	
	# Add the destination node attributes
	addNodeAttrs(G, destAttrs, data, dest_col)

	# Save the graph
	FOut = snap.TFOut("../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".graph")
	G.Save(FOut)
	FOut.Flush()

	FIn = snap.TFIn("../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".graph")
	G = snap.TNEANet.Load(FIn)
	G.Dump()
	

def main():	
	if len(sys.argv) == 1:
		print "Must enter a CSV file name"
	
	else:
		fname = sys.argv[1]

		print "We will now use the data in " + fname + " to form a graph"
		graph_name = raw_input("What do you want to name this graph?: ")

		print "Now you need to choose a graph type"
		print "Enter 0 for TUNGraph"
		print "Enter 1 for TNGraph"
		print "Enter 2 for TNEANet"
		graph_type = int(raw_input("What type of graph do you want?: "))

		if graph_type == 2:
			source_col = int(raw_input("Column index for the source nodes? (first column is index 0): "))
			dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0): "))

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
				if raw_input("New edge attribute?(y/n): ") == 'n': break
				key = raw_input("Edge attribute name: ")
				val = [int(raw_input("Edge attribute column index (first column is index 0): "))]
				val.append(int(raw_input("Attribute type (Enter 0 for int, 1 for float, 2 for string): ")))
				edgeAttrs[key] = val


			print "Now moving on to source node attributes"
			while True:
				if raw_input("New source node attribute?(y/n): ") == 'n': break
				key = raw_input("Source node attribute name: ")
				val = [int(raw_input("Source node attribute column index (first column is index 0): "))]
				val.append(int(raw_input("Attribute type (Enter 0 for int, 1 for float, 2 for string): ")))
				sourceAttrs[key] = val


			print "Now moving on to destination node attributes"
			while True:
				if raw_input("New destination node attribute?(y/n): ") == 'n': break
				key = raw_input("Destination node attribute name: ")
				val = [int(raw_input("Destination node attribute column index (first column is index 0): "))]
				val.append(int(raw_input("Attribute type (Enter 0 for int, 1 for float, 2 for string): ")))
				destAttrs[key] = val

			createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs)


		else:
			undirected = True if graph_type == 0 else False
			source_col = int(raw_input("Column index for the source nodes? (first column is index 0): "))
			dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0): "))
			createNormalGraph(fname, graph_name, undirected, source_col, dest_col)

if __name__ == "__main__":
	main()
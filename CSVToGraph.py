'''
Author: Sam Schwager
Last Modified: 11/6/2018

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
import argparse


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
	

def getBipartiteClasses(data, valueToNodeId):
	source_class = set()
	dest_class = set()

	for row in data:
		source_class.add(valueToNodeId[row[0]])
		dest_class.add(valueToNodeId[row[1]])

	broken_indices = source_class.intersection(dest_class)
	if len(broken_indices) > 0:
		print "Bipartite violations found at the following indices:"
		print broken_indices

	return list(source_class), list(dest_class), list(broken_indices)



def createNormalGraph(fname, graph_name, undirected, source_col, dest_col, bipartite):
	graph_type = "undirected" if undirected else "directed"
	# Make a folder to store all of the files for this graph
	os.mkdir("../" + "graphs/" + graph_name + '_' + graph_type)

	df = pd.read_csv(fname, header=0)
	df_reduced = pd.concat([df.iloc[:, source_col], df.iloc[:, dest_col]], axis=1)
	df_reduced = df_reduced.dropna()

	# Convert to numpy array
	data = df_reduced.values

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(data)
	print nodeIdToValue
	np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/node_id_to_value", nodeIdToValue)

	# Create a tab separated representation of the graph
	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems}

	# If the graph is bipartite, then we want to save the two bipartite classes
	# We also want to be aware of any edges that violate the bipartite structure
	if bipartite:
		source_class, dest_class, broken_indices = getBipartiteClasses(data, valueToNodeId)
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/bipartite_source_class", np.array(source_class))
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/bipartite_dest_class", np.array(dest_class))
		if len(broken_indices) > 0:
			np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/data_indices_violating_bipartite_structure", np.array(broken_indices))

	tabSeparatedGraph = createTabSeparatedGraph(data, valueToNodeId)

	# Save the graph to the folder so that it can be loaded in the future
	tabSeparatedGraphTitle = "../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".txt"
	np.savetxt(tabSeparatedGraphTitle, tabSeparatedGraph, fmt='%i', delimiter="\t")



def addNodeAttrs(G, attrs, data, col, valueToNodeId, store_auxiliary_data):
	auxiliary_node_data = {}

	for key, value in attrs.iteritems():
		curr_auxiliary_node_data = {}

		attribute_type = value[1]
		if attribute_type == 0:
			G.AddIntAttrN(key)
		elif attribute_type == 1:
			G.AddFltAttrN(key)
		elif attribute_type == 2:
			G.AddStrAttrN(key)

		attribute_col_index = value[0]
		for row in data:
			curr_nodeId = valueToNodeId[row[col]]
			if attribute_type == 0:
				G.AddIntAttrDatN(curr_nodeId, int(row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_node_data[curr_nodeId] = int(curr_row[attribute_col_index])
			elif attribute_type == 1:
				G.AddFltAttrDatN(curr_nodeId, float(row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_node_data[curr_nodeId] = float(curr_row[attribute_col_index])
			elif attribute_type == 2:
				G.AddStrAttrDatN(curr_nodeId, str(row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_node_data[curr_nodeId] = str(row[attribute_col_index])

		if len(curr_auxiliary_node_data) > 0: auxiliary_node_data[key] = curr_auxiliary_node_data

	return auxiliary_node_data

			

def addEdgeAttrs(G, attrs, data, edgeIdToDataRow, store_auxiliary_data):
	auxiliary_edge_data = {}

	for key, value in attrs.iteritems():
		curr_auxiliary_edge_data = {}

		attribute_type = value[1]
		if attribute_type == 0:
			G.AddIntAttrE(key)
		elif attribute_type == 1:
			G.AddFltAttrE(key)
		elif attribute_type == 2:
			G.AddStrAttrE(key)

		attribute_col_index = value[0]
		for EI in G.Edges():
			curr_edgeId = EI.GetId()
			curr_row = data[edgeIdToDataRow[curr_edgeId]]

			if attribute_type == 0:
				G.AddIntAttrDatE(curr_edgeId, int(curr_row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_edge_data[curr_edgeId] = int(curr_row[attribute_col_index])
			elif attribute_type == 1:
				G.AddFltAttrDatE(curr_edgeId, float(curr_row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_edge_data[curr_edgeId] = float(curr_row[attribute_col_index])
			elif attribute_type == 2:
				G.AddStrAttrDatE(curr_edgeId, str(curr_row[attribute_col_index]), key)
				if store_auxiliary_data: curr_auxiliary_edge_data[curr_edgeId] = str(curr_row[attribute_col_index])

		if len(curr_auxiliary_edge_data) > 0: auxiliary_edge_data[key] = curr_auxiliary_edge_data

	return auxiliary_edge_data

		
'''
Load and view graphs as follows:

FIn = snap.TFIn("../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".graph")
G = snap.TNEANet.Load(FIn)
G.Dump()


Load and view dicts as follows:

source_node_data = np.load("../" + "graphs/" + graph_name + '_' + graph_type + '/' + "auxiliary_source_node_data.npy")
source_node_dict = source_data.item()
for key, val in source_node_dict:
	print key, val
'''

def createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs, bipartite, store_auxiliary_data):
	graph_type = "TNEANet"
	os.mkdir("../" + "graphs/" + graph_name + '_' + graph_type)
	
	# Don't choose specific columns here because we may have node/edge attributes
	df =  pd.read_csv(fname, header=0)
	df = df.fillna(-1)

	# Convert to numpy array
	# Delete invalid rows (i.e. rows missing a source or dest node)
	data = df.values
	row_index = 0
	while True:
		if row_index >= data.shape[0]: break
		curr_row = data[row_index]
		if curr_row[source_col] == -1 or curr_row[dest_col] == -1: 
			data = np.delete(data, row_index, axis=0)
		else:
			row_index += 1

	nodeData = np.concatenate((data[:, [source_col]], data[:, [dest_col]]), axis=1)

	# Keep a mapping from node ID to original value
	nodeIdToValue = createNodeIDs(nodeData)
	np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/node_id_to_value", nodeIdToValue)

	valueToNodeId = {v: k for k, v in nodeIdToValue.iteritems()}

	# If the graph is bipartite, then we want to save the two bipartite classes
	# We also want to be aware of any edges that violate the bipartite structure
	if bipartite:
		source_class, dest_class, broken_indices = getBipartiteClasses(nodeData, valueToNodeId)
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/bipartite_source_class", np.array(source_class))
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/bipartite_dest_class", np.array(dest_class))
		if len(broken_indices) > 0:
			np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/data_indices_violating_bipartite_structure", np.array(broken_indices))

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
	for rowIndex in range(data.shape[0]):
		currRow = data[rowIndex]
		currEdgeId = G.AddEdge(valueToNodeId[currRow[source_col]], valueToNodeId[currRow[dest_col]])
		edgeIdToDataRow[currEdgeId] = rowIndex

	# Add the edge attributes
	auxiliary_edge_data = addEdgeAttrs(G, edgeAttrs, data, edgeIdToDataRow, store_auxiliary_data)

	# Add the source node attributes
	auxiliary_source_node_data = addNodeAttrs(G, sourceAttrs, data, source_col, valueToNodeId, store_auxiliary_data)
	
	# Add the destination node attributes
	auxiliary_dest_node_data = addNodeAttrs(G, destAttrs, data, dest_col, valueToNodeId, store_auxiliary_data)

	# Save the graph
	FOut = snap.TFOut("../" + "graphs/" + graph_name + '_' + graph_type + '/' + graph_name + ".graph")
	G.Save(FOut)
	FOut.Flush()

	# If stipulated by the user, then we want to
	# save the auxiliary data that we have stored in dicts of dicts
	# We did this because there are issues with the snap implementation
	# regarding float and string edge/node attributes
	if store_auxiliary_data and len(auxiliary_edge_data) > 0:
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/auxiliary_edge_data", auxiliary_edge_data)

	if store_auxiliary_data and len(auxiliary_source_node_data) > 0:
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/auxiliary_source_node_data", auxiliary_source_node_data)

	if store_auxiliary_data and len(auxiliary_dest_node_data) > 0:
		np.save("../" + "graphs/" + graph_name + '_' + graph_type + "/auxiliary_dest_node_data", auxiliary_dest_node_data)
	

def main():	
	if len(sys.argv) != 2:
		print "Must enter a valid CSV file name after the name of the Python script and nothing else"
	
	else:
		fname = sys.argv[1]

		file_check = fname.split('.')

		if file_check[len(file_check) - 1] != "csv":
			print "File must be a .csv file"
			return

		if not os.path.isfile(fname):
			print "File does not exist"
			return 

		print "We will now use the data in " + fname + " to form a graph"
		graph_name = raw_input("What do you want to name this graph?: ")

		print "Now you need to choose a graph type"
		print "Enter 0 for TUNGraph"
		print "Enter 1 for TNGraph"
		print "Enter 2 for TNEANet"
		graph_type = int(raw_input("What type of graph do you want?: "))
		bipartite = raw_input("Is this graph bipartite?(y/n): ") == 'y'

		if graph_type == 2:
			print "We can store all of the information we need in the graph"
			print "But if you want to store auxiliary data for nodes and edges in numpy arrays we can do that too"
			store_auxiliary_data = raw_input("Store auxiliary data outside of graph?(y/n): ") == 'y'

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

			createComplexGraph(fname, graph_name, source_col, dest_col, edgeAttrs, sourceAttrs, destAttrs, bipartite, store_auxiliary_data)


		else:
			undirected = True if graph_type == 0 else False
			source_col = int(raw_input("Column index for the source nodes? (first column is index 0): "))
			dest_col = int(raw_input("Column index for the destination nodes? (first column is index 0): "))
			createNormalGraph(fname, graph_name, undirected, source_col, dest_col, bipartite)

if __name__ == "__main__":
	main()

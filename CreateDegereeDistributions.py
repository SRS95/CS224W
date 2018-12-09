import snap
import numpy as np
import pandas as pd
import sys
import os
import argparse
import matplotlib.pyplot as plt
import random as random
import operator

def ER_degree_distribution(N, E):

    Graph = snap.TNEANet.New()
    for index in range(1,N+1): Graph.AddNode(index)
    while (Graph.GetEdges() < E):
        SrcNId = random.randint(1,N)
        DstNId = random.randint(1, N)
        if Graph.IsEdge(SrcNId, DstNId) is False:
            Graph.AddEdge(SrcNId, DstNId)
    NodeItr = Graph.BegNI()
    distribution = {}
    for node in range(0, Graph.GetNodes()):
        nodeId = NodeItr.GetId()
        nodeDeg = NodeItr.GetDeg()
        if nodeDeg in distribution: distribution[nodeDeg] += 1
        else: distribution[nodeDeg] = 1
        NodeItr.Next()
        
    X, Y = [], []
    for key in distribution:
        X.append(key)
        Y.append(distribution[key])
        
    return X, Y


def calculate_degree_distribution(graph_name, G, node_name):
    NodeItr = G.BegNI()
    distribution = {}
    for node in range(0, G.GetNodes()):
        nodeId = NodeItr.GetId()
        nodeDeg = NodeItr.GetDeg()
        if nodeDeg in distribution: distribution[nodeDeg] += 1
        else: distribution[nodeDeg] = 1
        NodeItr.Next()

    X, Y = [], []
    y_norm = 0.0
    for key in distribution:
        X.append(key)
        Y.append(distribution[key]) 
        y_norm += distribution[key]
    for key in range(0, len(Y)): Y[key] = Y[key] / y_norm
    
    plt.scatter(X, Y, s = 5, color = 'g', label =  node_name + ' Distribution', alpha = 1)
    
    plt.scatter([.01], [.01], s = 5, color = 'g', alpha = 1)   
    plt.xlim(1, 3000)
    plt.ylim(0.00007, 0.1)                            
    plt.yscale('log')
    plt.xscale('log')
    
    plt.xlabel("Degree \"k\"")
    plt.ylabel("Probability Degree = \"k\"")
    plt.legend()
    plt.savefig(graph_name + " Distribution.pdf")
    plt.show()


def calculate_degree_distribution_directed(graph_name, G, node_name, set_attr):
	NodeItr = G.BegNI()
	distribution = {}
	for node in range(0, G.GetNodes()):
		nodeId = NodeItr.GetId()
		if nodeId in set_attr:
			nodeDeg = NodeItr.GetDeg()
			if nodeDeg in distribution: distribution[nodeDeg] += 1
			else: distribution[nodeDeg] = 1
		NodeItr.Next()

	X, Y = [], []
	y_norm = 0.0
	for key in distribution:
		X.append(key)
		Y.append(distribution[key]) 
		y_norm += distribution[key]
	for key in range(0, len(Y)): Y[key] = Y[key] / y_norm

	plt.scatter(X, Y, s = 5, color = 'r', label =  node_name + ' Distribution', alpha = 1)

	plt.scatter([.01], [.01], s = 5, color = 'g', alpha = 1)   
	plt.xlim(1, 3000)
	plt.ylim(0.001, 0.7)                            
	plt.yscale('log')
	plt.xscale('log')

	plt.xlabel("Out-Degree \"k\"")
	plt.ylabel("Probability Degree = \"k\"")
	plt.legend()
	plt.savefig(graph_name + " Distribution.pdf")
	plt.show()


def calculate_degree_distributions(G, set1, set2, set1_name, set2_name, graph_name):
    NodeItr = G.BegNI()
    set1_distribution, set2_distribution = {}, {}
    for node in range(0, G.GetNodes()):
        nodeId = NodeItr.GetId()
        nodeDeg = NodeItr.GetDeg()
        if nodeId in set1:
            if nodeDeg in set1_distribution: set1_distribution[nodeDeg] += 1
            else: set1_distribution[nodeDeg] = 1
        else:
            if nodeDeg in set2_distribution: set2_distribution[nodeDeg] += 1
            else: set2_distribution[nodeDeg] = 1
        NodeItr.Next()

    X_set1, Y_set1, X_set2, Y_set2 = [], [], [], []
    Y1_norm, Y2_norm = 0.0, 0.0
    for key in set1_distribution:
        X_set1.append(key)
        Y_set1.append(set1_distribution[key])
        Y1_norm += set1_distribution[key]
    for key in set2_distribution:
        X_set2.append(key)
        Y_set2.append(set2_distribution[key])
        Y2_norm += set2_distribution[key]
    for key in range(0, len(Y_set1)): Y_set1[key] = Y_set1[key] / Y1_norm
    for key in range(0, len(Y_set2)): Y_set2[key] = Y_set2[key] / Y2_norm

    plt.scatter(X_set1, Y_set1, s = 5, color = 'r', label = set1_name + ' Distribution', alpha = 1)
    plt.scatter(X_set2, Y_set2, s = 5, color = 'b', label = set2_name +' Distribution', alpha = 1)
                              
    plt.xscale('log')
    plt.yscale('log')

    plt.xlim(1, 1200)


    plt.ylim(0.00007, 0.8)
    plt.xlabel("Degree \"k\"")
    plt.ylabel("Probability Degree = \"k\"")
    plt.legend()
    plt.savefig(graph_name + " Distribution.pdf")
    plt.show()


def main():
	InvestToComp = snap.LoadEdgeList(snap.PNGraph, '../graphs/investors_to_companies_directed/investors_to_companies.txt', 0, 1)
	investors = np.load('../graphs/investors_to_companies_directed/bipartite_source_class.npy')
	companies = np.load('../graphs/investors_to_companies_directed/bipartite_dest_class.npy')
	calculate_degree_distributions(InvestToComp, investors, companies, "Investors", "Companies", "Investors-to-Companies")

	FIn = snap.TFIn('../graphs/investors_to_companies_directed/investors_to_companies_directed_folded_reverse_order.graph')
	InvestedComp = snap.TUNGraph.Load(FIn)
	calculate_degree_distribution("Investors-Investors", InvestedComp, 'Investors')


	FIn = snap.TFIn('../graphs/investors_to_companies_directed/investors_to_companies_directed_folded.graph')
	InvestedComp = snap.TUNGraph.Load(FIn)
	calculate_degree_distribution("Companies-Companies", InvestedComp, 'Companies')

	IndToComp = snap.LoadEdgeList(snap.PNGraph, '../graphs/industry_to_company_directed/industry_to_company.txt', 0, 1)
	industries = np.load('../graphs/industry_to_company_directed/bipartite_source_class.npy')
	print industries
	calculate_degree_distribution_directed("Industries-Companies", IndToComp, 'Industries', industries)


	RegToComp = snap.LoadEdgeList(snap.PNGraph, '../graphs/region_to_company_directed/region_to_company.txt', 0, 1)
	regions = np.load('../graphs/region_to_company_directed/bipartite_source_class.npy')
	calculate_degree_distribution_directed("Regions-Companies", RegToComp, 'Regions', regions)


if __name__ == "__main__":
	main()
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
    for key in distribution:
        if key == 1144: continue
        X.append(key)
        Y.append(distribution[key])    
    
    plt.scatter(X, Y, s = 5, color = 'g', label =  node_name + ' Distribution', alpha = 1)
    plt.scatter([1], [1], s = 5, color = 'g', alpha = 1)                               
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Degree (Log Scale)")
    plt.ylabel("Number of Nodes (Log Scale)")
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
    for key in set1_distribution:
        X_set1.append(key)
        Y_set1.append(set1_distribution[key])
    for key in set2_distribution:
        X_set2.append(key)
        Y_set2.append(set2_distribution[key])
    
    plt.scatter(X_set1, Y_set1, s = 5, color = 'r', label = set1_name + ' Distribution', alpha = 1)
    plt.scatter(X_set2, Y_set2, s = 5, color = 'b', label = set2_name +' Distribution', alpha = 1)
                              
    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel("Degree (Log Scale)")
    plt.ylabel("Number of Nodes (Log Scale)")
    plt.legend()
    plt.savefig(graph_name + " Distribution.pdf")
    plt.show()


def main():
	FIn = snap.TFIn('../graphs/investments-to-companies_TNEANet/investments-to-companies.graph')
	InvestToComp = snap.TNEANet.Load(FIn)
	investors = np.load('../graphs/investments-to-companies_TNEANet/bipartite_source_class.npy')
	companies = np.load('../graphs/investments-to-companies_TNEANet/bipartite_dest_class.npy')
	calculate_degree_distributions(InvestToComp, investors, companies, "Investors", "Companies", "Investors-to-Companies")

	FIn = snap.TFIn('../graphs/investments-to-companies_TNEANet/investments-to-companies_TNEANet_folded.graph')
	InvestedComp = snap.TUNGraph.Load(FIn)
	calculate_degree_distribution("Investors-Investors", InvestedComp, 'Investors')

	FIn = snap.TFIn('../graphs/investments-to-companies_TNEANet/investments-to-companies_folded_reverse.graph')
	InvestedComp = snap.TUNGraph.Load(FIn)
	calculate_degree_distribution("Companies-Companies", InvestedComp, 'Companies')

if __name__ == "__main__":
	main()
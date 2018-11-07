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
## TODO: Basic analysis code here

	return


def main():
	if len(sys.argv) != 2:
		print "Must enter a valid CSV file name after the name of the Python script and nothing else"
	
	else:
		fname = sys.argv[1]

		file_check = fname.split('.')

		is_txt_file = file_check[len(file_check) - 1] == "txt"
		is_graph_file = file_check[len(file_check) - 1] == "graph"

		if not is_txt_file and not is_graph_file:
			print "File must be a .txt or .graph file"
			return

		if not os.path.isfile(fname):
			print "File does not exist"
			return 

		G = None

		if is_txt_file:
			G = snap.LoadEdgeList(fname)

		else:
			FIn = snap.TFIn(fname)
			G = snap.TNEANet.Load(FIn)

		G.Dump()
		analyzeGraph(G)


if __name__ == "__main__":
	main()
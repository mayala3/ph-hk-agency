import snap
import numpy as np
import matplotlib.pyplot as plt

import random

def getDataPointsToPlot(Graph):

    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graph, DegToCntV)

    totalNodes = Graph.GetNodes()

    X, Y = [], []

    for output in DegToCntV:
        X.append(output.GetVal1())
        Y.append(output.GetVal2() / float(totalNodes))

    return X, Y

def basic_analysis():


	FIn = snap.TFIn("../graphs/ph_simple.graph")
	G = snap.TUNGraph.Load(FIn)

	numNodes = G.GetNodes()
	print "num nodes: ", numNodes
	numEdges = G.GetEdges()
	print "num edges: ", numEdges

	# clustering coefficient
	print "\nclustering coefficient"

	print "Clustering G: ", snap.GetClustCf(G)

	ER = snap.GenRndGnm(snap.PUNGraph, numNodes, numEdges)

	print "Clustering ER: ", snap.GetClustCf(ER)

	# degree distribution histogram

	print "\ndegree distribution histogram"

	x_erdosRenyi, y_erdosRenyi = getDataPointsToPlot(ER)
	plt.loglog(x_erdosRenyi, y_erdosRenyi, color = 'g', label = 'Erdos Renyi Network')

	x_smallWorld, y_smallWorld = getDataPointsToPlot(G)
	plt.loglog(x_smallWorld, y_smallWorld, linestyle = 'dashed', color = 'b', label = 'PH Agency Network')

	plt.xlabel('Node Degree (log)')
	plt.ylabel('Proportion of Nodes with a Given Degree (log)')
	plt.title('Degree Distribution of Erdos Renyi and PH Agency Network')
	plt.legend()
	plt.show()

	# degree
	print "\ndegree distribution"

	deg_sum = 0.0

	CntV = snap.TIntPrV()
	snap.GetOutDegCnt(G, CntV)
	for p in CntV:
		deg_sum += p.GetVal1() * p.GetVal2()

	max_node = G.GetNI(snap.GetMxDegNId(G))

	deg_sum /= float(numNodes)

	print "average degree: ", deg_sum # same for G and ER

	print "max degree: ", max_node.GetOutDeg(), ", id: ", max_node.GetId()

	deg_sum = 0.0
	
	max_node = ER.GetNI(snap.GetMxDegNId(ER))

	print "max degree: ", max_node.GetOutDeg(), ", id: ", max_node.GetId()

	# diameter
	print "\ndiameter"

	diam = snap.GetBfsFullDiam(G, 10)

	print "Diameter: ", diam

	print "ER Diameter: ", snap.GetBfsFullDiam(ER, 10)

	# triads
	print "\ntriads"

	print "Triads: ", snap.GetTriads(G)

	print "ER Triads: ", snap.GetTriads(ER)

	# centrality
	print "\ncentrality"

	max_dc = 0.0
	maxId = -1

	all_centr = []

	for NI in G.Nodes():
		DegCentr = snap.GetDegreeCentr(G, NI.GetId())
		all_centr.append(DegCentr)
		if DegCentr > max_dc:
			max_dc = DegCentr
			maxId = NI.GetId() 
	
	print "max"
	print "node: %d centrality: %f" % (maxId, max_dc)
	print "average centrality: ", np.mean(all_centr)

	print "ER"
	max_dc = 0.0
	maxId = -1

	all_centr = []

	for NI in ER.Nodes():
		DegCentr = snap.GetDegreeCentr(ER, NI.GetId())
		all_centr.append(DegCentr)
		if DegCentr > max_dc:
			max_dc = DegCentr
			maxId = NI.GetId() 
			
	print "max"
	print "node: %d centrality: %f" % (maxId, max_dc)
	print "average centrality: ", np.mean(all_centr)



basic_analysis()
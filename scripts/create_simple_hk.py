# import snap
import numpy as np
import matplotlib.pyplot as plt
import pdb

import random

from pymongo import MongoClient
import os
import csv

import networkx as nx
import json
from networkx.readwrite import json_graph

def shared_resource_array(agency):
	email = agency['sharedEmailAgencies']
	exact_a = agency['sharedAddressExactAgencies']
	sim_a = agency['addressTextSimilarityAgencies']
	phone = agency['sharedPhoneAgencies']
	fax = agency['sharedFaxAgencies']

	return np.unique(email + exact_a + sim_a + phone + fax)

def shared_resource_array_abr(agency):
	exact_a = agency['sharedAddressExactAgencies']
	phone = agency['sharedPhoneAgencies']
	email = agency['sharedEmailAgencies']

	return np.unique(exact_a + phone + email)


def create_graph():
	mongoUri = DATABASE_SECRET
	client = MongoClient(mongoUri)
	db = client['help']
	hkAgencies = db['employmentAgenciesHK-14-11-2018']

	allAgencies = hkAgencies.find({})
	print "initial count: ", hkAgencies.count()

	G = snap.TUNGraph.New()

	all_ids = []

	for agency in allAgencies: #add all nodes
		agency_id = int(agency['_id'])
		G.AddNode(agency_id)
		all_ids.append(agency_id)

	print "node count: ", G.GetNodes()

	allAgencies = hkAgencies.find({}) # need to move cursor back

	for agency in allAgencies: #add all edges

		agency_id = int(agency['_id'])
		
		all_shared = shared_resource_array(agency)

		for n_id_string in all_shared:
			n_id = int(n_id_string)
			if G.IsEdge(agency_id, n_id):
				continue
			G.AddEdge(agency_id, n_id)

	
	print "edge count: ", G.GetEdges()

	out = snap.TFOut("../graphs/hk_simple.graph")
	G.Save(out)
	out.Flush()

def create_nx_json(abr=False):
	mongoUri = DATABASE_SECRET
	client = MongoClient(mongoUri)
	db = client['help']
	hkAgencies = db['employmentAgenciesHK-14-11-2018']

	allAgencies = hkAgencies.find({})
	print "initial count: ", hkAgencies.count()

	G = nx.Graph()

	all_ids = [int(agency['_id']) for agency in allAgencies]

	G.add_nodes_from(all_ids, color='blue', country='hk')

	# for agency in allAgencies: #add all nodes
	# 	agency_id = int(agency['_id'])
	# 	G.AddNode(agency_id)
	# 	all_ids.append(agency_id)

	# print "node count: ", G.GetNodes()

	allAgencies = hkAgencies.find({}) # need to move cursor back

	for agency in allAgencies: #add all edges

		agency_id = int(agency['_id'])
		
		if abr:
			all_shared = shared_resource_array_abr(agency)
		else:
			all_shared = shared_resource_array(agency)

		for n_id_string in all_shared:
			n_id = int(n_id_string)
			if G.has_edge(agency_id, n_id):
				continue
			G.add_edge(agency_id, n_id)

	
	print len(G), G.size()
	data = json_graph.node_link_data(G)

	edge_path = "../edgelists/"

	json_path = "../json/"

	filebase = "simple_hk"
	
	if abr:
		filebase = filebase + "_abr"

	with open(json_path + filebase + ".json", "w") as write_file:
		json.dump(data, write_file)

	nx.write_edgelist(G, edge_path + filebase + ".edgelist")

# create_graph()


create_nx_json(True)
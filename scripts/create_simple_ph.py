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
	exact_a = agency['sharedAddressExactAgencies']
	phone = agency['sharedPhoneAgencies']
	email = agency['sharedEmailAgencies']

	return np.unique(exact_a + phone + email)

def create_graph():
	mongoUri = DATABASE_SECRET
	client = MongoClient(mongoUri)
	db = client['help']
	phAgencies = db['employmentAgenciesPH-09-11-2018']

	allAgencies = phAgencies.find({})
	print "initial count: ", phAgencies.count()

	G = snap.TUNGraph.New()

	all_ids = []

	for agency in allAgencies: #add all nodes
		agency_id = get_id(agency['_id'])
		G.AddNode(agency_id)
		all_ids.append(agency_id)

	print "node count: ", G.GetNodes()

	allAgencies = phAgencies.find({}) # need to move cursor back

	for agency in allAgencies: #add all edges

		agency_id = get_id(agency['_id'])
		
		all_shared = shared_resource_array(agency)

		for n_id_string in all_shared:
			n_id = get_id(n_id_string)
			if G.IsEdge(agency_id, n_id):
				continue
			G.AddEdge(agency_id, n_id)

	
	print "edge count: ", G.GetEdges()

	out = snap.TFOut("../graphs/ph_simple.graph")
	G.Save(out)
	out.Flush()

def create_nx_json():
	mongoUri = DATABASE_SECRET
	client = MongoClient(mongoUri)
	db = client['help']
	phAgencies = db['employmentAgenciesPH-09-11-2018']

	allAgencies = phAgencies.find({})
	print "initial count: ", phAgencies.count()

	G = nx.Graph()

	all_ids = [get_id(agency['_id']) for agency in allAgencies]

	G.add_nodes_from(all_ids, color='red', country='ph')

	# for agency in allAgencies: #add all nodes
	# 	agency_id = int(agency['_id'])
	# 	G.AddNode(agency_id)
	# 	all_ids.append(agency_id)

	# print "node count: ", G.GetNodes()

	allAgencies = phAgencies.find({}) # need to move cursor back

	for agency in allAgencies: #add all edges

		agency_id = get_id(agency['_id'])
		
		all_shared = shared_resource_array(agency)

		for n_id_string in all_shared:
			n_id = get_id(n_id_string)
			if G.has_edge(agency_id, n_id):
				continue
			G.add_edge(agency_id, n_id)

	
	print len(G), G.size()
	data = json_graph.node_link_data(G)

	with open("../json/simple_ph.json", "w") as write_file:
		json.dump(data, write_file)

	nx.write_edgelist(G, "../edgelists/simple_ph.edgelist")

def get_id(raw):
	return int(raw, 16) % (10 ** 8)

create_nx_json()
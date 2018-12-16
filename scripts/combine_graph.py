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

import pickle

mongoUriHK = DATABASE_SECRET
clientHK = MongoClient(mongoUriHK)
dbHK = clientHK['help']
hkAgencies = dbHK['employmentAgenciesHK-14-11-2018']

mongoUriPH = DATABASE_SECRET
clientPH = MongoClient(mongoUriPH)
dbPH = clientPH['help']
phAgencies = dbPH['employmentAgenciesPH-09-11-2018']

def get_sim_dict(agency):
	email = agency['sharedEmailAgencies']
	exact_a = agency['sharedAddressExactAgencies']
	phone = agency['sharedPhoneAgencies']

	all_sim = [email, exact_a, phone]

	edge_weights = {}

	for sim in all_sim:
		for entry in sim:
			if entry in edge_weights:
				edge_weights[entry] += 1
			else:
				edge_weights[entry] = 1

	return edge_weights

def add_ph_nodes(G):
	allAgencies = phAgencies.find({})
	print "initial count: ", phAgencies.count()

	all_ids = [get_id(agency['_id']) for agency in allAgencies]

	G.add_nodes_from(all_ids, color='red', country='ph')

	allAgencies = phAgencies.find({})

	for agency in allAgencies: #add all edges

		agency_id = get_id(agency['_id'])

		sim_dict = get_sim_dict(agency)

		if len(sim_dict) == 0:
			G.remove_node(agency_id)
			continue

		for n_id_string, weight in sim_dict.iteritems():
			n_id = get_id(n_id_string)
			if G.has_edge(agency_id, n_id):
				continue
			G.add_edge(agency_id, n_id, weight=weight, color='#FA8072')

def add_hk_nodes(G):
	allAgencies = hkAgencies.find({})
	print "initial count: ", hkAgencies.count()

	all_ids = [int(agency['_id']) for agency in allAgencies]

	G.add_nodes_from(all_ids, color='blue', country='hk')

	allAgencies = hkAgencies.find({})

	for agency in allAgencies: #add all edges

		agency_id = int(agency['_id'])
		
		sim_dict = get_sim_dict(agency)

		if len(sim_dict) == 0:
			G.remove_node(agency_id)
			continue

		for n_id_string, weight in sim_dict.iteritems():
			n_id = int(n_id_string)
			if G.has_edge(agency_id, n_id):
				continue
			G.add_edge(agency_id, n_id, weight=weight, color='#87CEFA')

def add_inter_edges(G):
	with open('../raw/responses.txt', 'r') as file:
		data = file.read()

		lines = data.split('\r')

		pairs = [line.split('\t') for line in lines]

		for pair in pairs:
			hk_name = pair[0]
			ph_name = pair[1]

			if pair[0] == None or pair[1] == None:
				print pair
				continue

			if hk_name_id(hk_name) == None:
				print hk_name
				continue

			hk_id = hk_name_id(hk_name)

			if ph_name_id(ph_name) == None:
				print ph_name
				continue

			ph_id = get_id(ph_name_id(ph_name))

			if G.has_node(hk_id) == False:
				G.add_node(hk_id, color='blue', country='hk')

			if G.has_node(ph_id) == False:
				G.add_node(ph_id, color='red', country='ph')

			if G.has_edge(hk_id, ph_id) == False:
				G.add_edge(hk_id, ph_id, weight=1, color='green')
			else:
				G[hk_id][ph_id]['weight'] += 1
		
def ph_name_id(name):
	agencies = phAgencies.find({"name": name})
	for agency in agencies:
		agency_id = agency['_id'] # 
		return agency_id

def hk_name_id(name):
	agencies = hkAgencies.find({"english_name": name})
	for agency in agencies:
		agency_id = int(agency['_id']) # 
		return agency_id


def process():
	G = nx.Graph()

	add_hk_nodes(G)
	print "After HK: ", len(G), G.size()
	add_ph_nodes(G)
	print "After PH: ", len(G), G.size()
	add_inter_edges(G)
	print "After Inter: ", len(G), G.size()

	print len(G), G.size()
	data = json_graph.node_link_data(G)

	edge_path = "../edgelists/"

	json_path = "../json/"

	filebase = "combined"

	with open(json_path + filebase + ".json", "w") as write_file:
		json.dump(data, write_file)

	nx.write_edgelist(G, edge_path + filebase + ".edgelist")


def main():
	edge_path = "../edgelists/"

	G=nx.read_edgelist(edge_path + "combined_sim.edgelist")
	compute_centrality_stats(G)

	compute_connectivity_stats(G)

	compute_cliques(G)

def compute_centrality_stats(G):

	s_in = open("../pickles/id2n.p","rb")
	id2n = pickle.load(s_in)

	top_eigen_w = get_top_5(nx.eigenvector_centrality_numpy(G, 'weight'))

	print "Eigenvector Centrality Numpy"

	for e in top_eigen_w:
		print id2n[int(e[0])], e[1]

	top_dc = get_top_5(nx.degree_centrality(G))

	print "Degree Centrality"
	for e in top_dc:
		print id2n[int(e[0])], e[1]

	top_bc = get_top_5(nx.betweenness_centrality(G))

	print "Betweenness Degree Centrality"
	for e in top_bc:
		print id2n[int(e[0])], e[1]

def get_top_5(dictionary):
	all_keys = dictionary.keys()

	all_keys.sort(key=lambda elem: dictionary[elem], reverse=True)

	return [(k, dictionary[k]) for k in all_keys[:10]]

def get_id(raw):
	return int(raw, 16) % (10 ** 8) + 4000

def create_helper_files():
	id2name = {}

	hk = set()

	ph = set()

	allPhAgencies = phAgencies.find({})

	for agency in allPhAgencies: #add all edges

		agency_id = get_id(agency['_id'])

		ph.add(agency_id)

		agency_name = agency['name']

		id2name[agency_id] = agency_name

	allHkAgencies = hkAgencies.find({})

	for agency in allHkAgencies: #add all edges

		agency_id = int(agency['_id'])

		hk.add(agency_id)

		agency_name = agency['english_name']

		id2name[agency_id] = agency_name
	pickle_path = "../pickles/"
	pickle.dump(id2name, open(pickle_path + "id2n.p", "wb" ))

	pickle.dump(ph, open(pickle_path +  "all_ph.p", "wb" ))

	pickle.dump(hk, open(pickle_path +  "all_hk.p", "wb" ))

def compute_connectivity_stats(G):
	pickle_path = "../pickles/"

	s_in = open(pickle_path + "id2n.p","rb")
	id2n = pickle.load(s_in)

def compute_cliques(G):
	s_in = open(pickle_path + "id2n.p","rb")
	id2n = pickle.load(s_in)

	clique = nx.make_max_clique_graph(G)

	print len(clique), clique.size()

main()

# create_helper_files()
# create_id_name()
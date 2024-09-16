import json
import sys
import numpy as np
from tabulate import tabulate

#
# args: the automated dataset and the manually refined dataset,
# they must refer to the exact same samples
#

class Node:
    def __init__(self, name, label, noun_type, attributes):
        self.attributes = attributes
        self.noun_type = noun_type
        self.label = label
        self.name = name

class Sample:
    def __init__(self, json_data):
        self.nodes = []
        for node in json_data['nodes']:
            self.nodes.append(Node(node['name'], node['label'], node['noun_type'], node['attributes']))

        self.edges = []
        for edge in json_data['edges']:
            self.edges.append(edge['relation'])

    def get_attribute_names(self):
        attribute_names = []
        for node in self.nodes:
            for attr in node.attributes.values():
                attribute_names.append(attr)

        return attribute_names

    def get_all_labels(self):
        labels = []
        for node in self.nodes:
            if node.noun_type == 'COMMON':
                labels.append(node.label.lower())

            for lbl in node.attributes.keys():
                labels.append(lbl.lower())

        return labels

def compute_ratio(auto_set, ref_set):
    if len(ref_set) == 0:
            return 1
    else:
        intersection = auto_set & ref_set
    return len(intersection) / len(ref_set)

statistics      = {}
count           = 0
node_percent    = []
excess_nodes    = []
edge_percent    = []
excess_edges    = []
attr_name_ratio = []
label_ratio     = []

with open(sys.argv[1]) as auto, open(sys.argv[2]) as ref:
    for auto_line, ref_line in zip(auto, ref):
        count += 1
        auto_sample = Sample(json.loads(auto_line))
        ref_sample  = Sample(json.loads(ref_line))

        # Nodes
        auto_nodes        = set([n.name for n in auto_sample.nodes])
        ref_nodes         = set([n.name for n in ref_sample.nodes])
        node_intersection = auto_nodes & ref_nodes

        node_percent.append(len(node_intersection) / len(ref_nodes))
        excess_nodes.append(len(auto_nodes - node_intersection))

        # Attributes
        auto_attr_names = set(auto_sample.get_attribute_names())
        ref_attr_names  = set(ref_sample.get_attribute_names())

        attr_name_ratio.append(compute_ratio(auto_attr_names, ref_attr_names))

        # Labeling
        auto_labels = set(auto_sample.get_all_labels())
        ref_labels  = set(ref_sample.get_all_labels())

        label_ratio.append(compute_ratio(auto_labels, ref_labels))

        # Edges
        auto_edges = set(auto_sample.edges)
        ref_edges  = set(ref_sample.edges)

        edge_intersection = auto_edges & ref_edges

        edge_percent.append(len(edge_intersection) / len(ref_edges))
        excess_edges.append(len(auto_edges - edge_intersection))

        statistics['AVG Nodes Identified (%)']      = round(np.mean(node_percent) * 100, 2)
        statistics['SD Nodes Identified (%)']       = round(np.std(node_percent) * 100, 2)
        statistics['AVG Excess Nodes Identified']   = round(np.mean(excess_nodes), 2)
        statistics['SD Excess Nodes Identified']    = round(np.std(excess_nodes), 2)
        statistics['AVG Attributes Identified (%)'] = round(np.mean(attr_name_ratio) * 100, 2)
        #statistics['SD Attributes Identified (%)']  = round(np.std(attr_name_ratio) * 100, 2)
        statistics['AVG Correct Labels (%)']        = round(np.mean(label_ratio) * 100, 2)
        # statistics['SD Correct Labels (%)']         = round(np.std(label_ratio) * 100, 2)
        statistics['AVG Edges Identified (%)']      = round(np.mean(edge_percent) * 100, 2)
        statistics['SD Edges Identified (%)']       = round(np.std(edge_percent) * 100, 2)

print('SOME STATISTICS')
print(tabulate(list(statistics.items()), tablefmt='grid'))

import sys
import json
from utils.utils import visualize_graph

#
# args: file_path.jsonl, number_of_entries (to visualize), default = 1
#

num_graphs = 1
if len(sys.argv) > 2:
    num_graphs = int(sys.argv[2])

with open(sys.argv[1]) as file:
    for i, line in enumerate(file):
        json_data = json.loads(line)

        visualize_graph(json_data)

        if i == num_graphs - 1:
            break

import sys
import json
from utils.utils import visualize_graph

#
# args: file_path.jsonl, number_of_entries (to visualize), default = 1
#

# num_graphs = 1
# if len(sys.argv) > 2:
#     num_graphs = int(sys.argv[2])
#
# with open(sys.argv[1]) as file:
#     for i, line in enumerate(file):
#         json_data = json.loads(line)
#
#         visualize_graph(json_data)
#
#         if i == num_graphs - 1:
#             break

json_data = {"doc_id": 10, "text": "Laura loved corn. So Laura decided to grow some in Laura's backyard. The whole process of growing them made Laura very excited. But Laura realized that corn required too much water. So Laura quickly abandoned Laura's corn garden idea.\n", "entities": [{"id": 1, "name": "Laura", "label": "PERSON", "noun_type": "PROPER", "attributes": {"attribute1": "hard-working", "attribute2": "perfectionist"}}, {"id": 2, "name": "corn", "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": {}}, {"id": 3, "name": "backyard", "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": {}}, {"id": 4, "name": "them", "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": {}}, {"id": 5, "name": "water", "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": {"attribute1": "much"}}, {"id": 6, "name": "idea", "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": {}}], "relationships": [{"source": 1, "target": 2, "relation": "love"}, {"source": 1, "target": 3, "relation": "grow in"}, {"source": 1, "target": 4, "relation": "make"}, {"source": 2, "target": 5, "relation": "require"}, {"source": 1, "target": 6, "relation": "abandon"}]}
visualize_graph(json_data)

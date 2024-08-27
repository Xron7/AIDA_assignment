import spacy
import sys
from utils.utils import create_graph
from tqdm import tqdm
import json

TARGET = 'KG_dataset.jsonl'

nlp = spacy.load("en_core_web_trf")

with open(sys.argv[1], 'r') as file, open(TARGET, 'w') as output:
    for i, line in enumerate(tqdm(file, desc='Creating KG Dataset')):
        KG_json = create_graph(line, nlp)

        json_data = {"doc_id":  i+1, "text": line}
        json_data.update(KG_json)

        json_line = json.dumps(json_data)
        output.write(json_line + '\n')

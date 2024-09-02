import spacy
import sys
from utils.utils import create_graph
from tqdm import tqdm
import json
import csv

TARGET = 'KG_dataset.jsonl'

nlp = spacy.load("en_core_web_trf")

with open(sys.argv[1], 'r') as file, open(TARGET, 'w') as output:
    reader = csv.reader(file, delimiter='|')
    for i, row in enumerate(tqdm(reader, desc='Creating KG Dataset')):
        KG_json = create_graph(row[1], nlp)

        json_data = {"doc_id":  i+1, "text": row[0]}
        json_data.update(KG_json)

        json_line = json.dumps(json_data)
        output.write(json_line + '\n')

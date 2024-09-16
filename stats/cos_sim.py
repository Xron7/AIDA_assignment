import json
from sentence_transformers import SentenceTransformer, util
import numpy as np
from tabulate import tabulate

def reconstruct_text(json_data):
  text  = []
  nodes = {}
  for node in json_data['nodes']:
    nodes[node['id']] = node['name']
  for edge in json_data['edges']:

    text.append(nodes[edge['source']])
    text.append(edge['relation'])
    text.append(nodes[edge['target']])
    text.append('.')

  return " ".join(text)

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def calculate_sim(json_data):
  rec_text = reconstruct_text(json_data)

  texts = []
  texts.append(rec_text)
  texts.append(json_data['text'])

  embeddings = model.encode(texts)
  sim = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

  return round(sim, 2)

auto_sims = []
ref_sims  = []

with open("automated_dataset.jsonl") as auto, open("manual_dataset.jsonl") as ref:
    for auto_line, ref_line in zip(auto, ref):
      auto_sims.append(calculate_sim(json.loads(auto_line)))
      ref_sims.append(calculate_sim(json.loads(ref_line)))

stats = [ ('AVG Cos Sim', round(np.mean(auto_sims),2), round(np.mean(ref_sims), 2)), ('SD Cos Sim', round(np.std(auto_sims), 2), round(np.std(ref_sims), 2))]
print(tabulate(stats, headers=['', 'Automated', 'Manually Refined'], tablefmt='grid'))


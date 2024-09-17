from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

cos_sims = []

with open("gpt_reconstructed.txt") as rec, open("manual_dataset.jsonl") as og:
    for rec_line, og_line in zip(rec, og):

      og_text = json.loads(og_line)['text']

      texts = []
      texts.append(og_text)
      texts.append(rec_line)

      embeddings = model.encode(texts)
      sim = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

      cos_sims.append(round(sim, 2))

print("AVG Cos Sim = ", round(np.mean(cos_sims), 2))
print("SD Cos Sim = ", round(np.std(cos_sims), 2))

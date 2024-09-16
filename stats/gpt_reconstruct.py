import openai
from utils.utils import get_key
import sys
from tqdm import tqdm
import json

api_key = get_key('../utils/api_key.txt')
client  = openai.OpenAI(api_key=api_key)

input_file  = sys.argv[1]
OUTPUT      = 'reconstructed.txt'

PROMPT  = ("Given a JSON which depicts nodes and edges of a Knowledge Graph, reconstruct the story described, "
           "DO NOT overuse excess words. Reply only with a single paragraph of continuous text, no new lines.")
REQUEST = ("I will give you a JSON which depicts nodes and edges of a Knowledge Graph, and I would like you to recI "
           "will give you a JSON which depicts nodes and edges of a Knowledge Graph, and I would like you to "
           "reconstruct the story described, do not overuse excess words ok?ostruct the story described, "
           "DO NOT overuse excess words. Please reply in a single paragraph.")

with open(input_file, 'r') as file, open(OUTPUT, 'w') as output_file:
    for line in tqdm(file, desc= 'Reconstructing Samples'):
        json_data     = json.loads(line)
        filtered_json = {k: json_data[k] for k in ['nodes', 'edges']}

        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": REQUEST},
                {"role": "user", "content": str(filtered_json)}
            ]
        )

        output_file.write(completion.choices[0].message.content + '\n')

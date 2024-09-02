import json
import sys
from utils.utils import characterize_attributes, get_key
import openai
from tqdm import tqdm

#
# argument is the jsonl file
#

TARGET = 'KG_dataset_attr.jsonl'

api_key = get_key('../utils/api_key.txt')
client  = openai.OpenAI(api_key=api_key)

with open(sys.argv[1], 'r') as file, open(TARGET, 'w') as output:
    for i, json_data in enumerate(tqdm(file, desc='Characterizing Attributes and Objects')):
        json_data_attr = characterize_attributes(json.loads(json_data.strip()), client)

        json_line = json.dumps(json_data_attr)
        output.write(json_line + '\n')

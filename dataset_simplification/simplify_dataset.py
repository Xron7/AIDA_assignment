import openai
from utils.utils import get_key, simplify_text
import sys
from tqdm import tqdm

#
# simplifies the dataset using the fine-tuned gpt model, check the sample_dataset for the input format
#

api_key = get_key('../utils/api_key.txt')
client  = openai.OpenAI(api_key=api_key)

input_file  = sys.argv[1]
OUTPUT      = 'simplified_dataset.csv'

with open(input_file, 'r') as file, open(OUTPUT, 'w') as output_file:
    for line in tqdm(file, desc= 'Simplifying Dataset'):
        output_file.write(line.strip() + '|' + simplify_text(line, client) + '\n')
        pass

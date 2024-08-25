import openai
from utils.utils import get_key, simplify_text
import sys
from tqdm import tqdm

api_key = get_key('../utils/api_key.txt')
client  = openai.OpenAI(api_key=api_key)

input_file  = sys.argv[1]
OUTPUT      = 'simplified_dataset.txt'

with open(input_file, 'r') as file, open(OUTPUT, 'w') as output_file:
    for line in tqdm(file, desc= 'Simplifying Dataset'):
        output_file.write(simplify_text(line, client) + '\n')
        pass

import json
import csv
import sys

#
# The argument is the file that will be used for fine-tuning. It needs to be named as fine_tune_{name}.csv
# and be pipe-separated
#
# this is what we want to create, for fine-tuning purposes
#{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
#

source = sys.argv[1]
mode   = source.replace('fine_tune_', '').replace('.csv', '')
target = f'fine_tune_{mode}.jsonl'

if mode == 'simplify':
    prompt = ("Transform the following sentences by replacing all pronouns (e.g., he, she, it, they, his, her, "
              "their) and relative clauses (e.g., who, that, which) with the corresponding actual entities, "
              "ensuring that the text remains grammatically correct and clear. Focus on maintaining the original "
              "meaning while explicitly stating each entity.")
else:
    prompt = ("Given a single word, return the most appropriate general category or type that describes it. The "
              "response should be a single word that encapsulates the essence of the input word, such as its "
              "category, type, or a more general term that describes it. Avoid overly specific or technical terms, "
              "and aim for broad, intuitive categories.")

user_messages      = []
assistant_messages = []

# read and store the csv
with open(source, 'r') as file:
    reader = csv.reader(file, delimiter='|')

    messages = []
    for row in reader:
        user      = {"role": "user",      "content": row[0]}
        assistant = {"role": "assistant", "content": row[1]}

        user_messages.append(user)
        assistant_messages.append(assistant)

system = {"role": "system", "content": prompt}

# create the jsonl
with open(target, 'w') as file:
    for i in range(len(user_messages)):
        item = {"messages": [system, user_messages[i], assistant_messages[i]]}
        json_line = json.dumps(item)
        file.write(json_line + '\n')

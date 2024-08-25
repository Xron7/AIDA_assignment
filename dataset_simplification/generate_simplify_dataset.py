import json
import csv

#
# this is what we want to create, for fine-tuning purposes
#{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
#

SOURCE = 'simplify_dataset.csv'
TARGET = 'simplify_dataset.jsonl'
PROMPT = "Transform the following sentences by replacing all pronouns (e.g., he, she, it, they, his, her, their) and relative clauses (e.g., who, that, which) with the corresponding actual entities, ensuring that the text remains grammatically correct and clear. Focus on maintaining the original meaning while explicitly stating each entity."

user_messages      = []
assistant_messages = []

# read and store the csv
with open(SOURCE, 'r') as file:
    reader = csv.reader(file, delimiter='|')

    messages = []
    for row in reader:
        user      = {"role": "user",      "content": row[0]}
        assistant = {"role": "assistant", "content": row[1]}

        user_messages.append(user)
        assistant_messages.append(assistant)

system = {"role": "system", "content": PROMPT}

# create the jsonl
with open(TARGET, 'w') as file:
    for i in range(len(user_messages)):
        item = {"messages": [system, user_messages[i], assistant_messages[i]]}
        json_line = json.dumps(item)
        file.write(json_line + '\n')

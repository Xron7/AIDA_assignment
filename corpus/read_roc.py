import csv
import sys
from tqdm import tqdm

#
# Reads the ROC dataset and converts it to a suitable txt dataset. ROC dataset needs to be downloaded from the website
#
SOURCE = 'roc_dataset.csv'
TARGET = 'roc_dataset.txt'

limit = 100
if len(sys.argv) > 1:
    limit = int(sys.argv[1])

with open(SOURCE, 'r') as csvfile, open(TARGET, 'w') as txtfile:
    reader = csv.DictReader(csvfile)
    for count, row in enumerate(tqdm(reader, total=limit, desc="Processing rows"), start=1):
        if count > limit:
            break
        combined_sentence = ' '.join(
            [row['sentence1'], row['sentence2'], row['sentence3'], row['sentence4'], row['sentence5']])
        txtfile.write(combined_sentence + '\n')

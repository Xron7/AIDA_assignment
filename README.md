# Artificial Intelligence and Data Analysis Assignment

This repository contains the dataset requested by the project as well as the code and files used for constructing it.

## The Files

### manual_dataset.jsonl

This is the final dataset, constructing by refining the automated with human intelligence.

### automated_dataset.jsonl

This is the dataset constructing using code. The Python files will be listed in the order they were used.

## Requirements

#### Python                3.8.10
#### spacy                 3.3.3
#### en_core_web_trf       3.3.0 (install through spacy)
#### openai                1.42.0
#### sentence-transformers 3.1.0

## The Main Flow

### corpus

#### read_roc.py

Reads the ROCStories dataset (needs to be downloaded from https://cs.rochester.edu/nlp/rocstories/) and reconstructs the stories as a new dataset.

### dataset_simplification

#### simplify_dataset.py

Using gpt (fine-tuned model, check the section), performs coreference resolution to the dataset.

### graph_creation

#### create_KG_dataset.py

Using spaCy, constructs the JSONL dataset, by extracting triples.

#### attribute_labeling.py

Enhances the JSONL by labeling the attributes using gpt(fine-tuned model, check the section)

## Other Files

### utils

#### utils.py

Contains various functions that could be isolated for general use by the rest of the files.

### fine_tuning

#### generate_fine_tune_dataset.py

Creates a dataset suitable for fine-tuning the gpt, using a .csv, depending on the use.

#### upload_training_file.py

Uploads the fine-tune dataset to the gpt dashboard.

#### fine_tune.py

Creates a fine-tuning job in the gpt dashboard.

### stats

#### statistics.py

Calculates some metrics about the automated and the manual dataset.

#### cos_sim.py

Calculates the cosine similarity between a KG dataset and the original text.

#### gpt_reconstruct.py

Using gpt, reconstructs the text using the KG as input.

#### gpt_cos_sim.py

Calculates the cosine similarity between the gpt reconstructed text and the original text.

### visualization

#### graph_visualization.py

Plots the KG.

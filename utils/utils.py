import networkx as nx
import matplotlib as plt
import json

# gets the api key from the text file
def get_key(file="api_key.txt"):
    f = open(file, "r")
    api_key = f.read().strip()
    f.close()
    return api_key


# simplifies a sentence (removes he/his/him and who/that/which etc.)
def simplify_text(text, client):
    prompt = "Transform the following sentences by replacing all pronouns (e.g., he, she, it, they, his, her, their) and relative clauses (e.g., who, that, which) with the corresponding actual entities, ensuring that the text remains grammatically correct and clear. Focus on maintaining the original meaning while explicitly stating each entity."
    request = "Please simplify the sentence I will give you in the next message. Return ONLY the simplified sentence"
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::A0BlPz97",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": request},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content


# creates a knowledge graph from the text
def create_graph(text, nlp):
    doc = nlp(text)

    json_data = {
        "entities": [],
        "relationships": []
    }

    # entities
    # proper nouns
    entities = {}
    counter = 0
    for ent in doc.ents:
        if ent.text not in entities.keys():
            counter += 1
            entities[ent.text] = counter
            entity_obj = {"id": counter, "name": ent.text, "label": ent.label_}

            json_data["entities"].append(entity_obj)

    # common nouns and
    # relations/triplets
    for sent in doc.sents:
        subject = None
        object_ = None
        verb    = None

        for token in sent:
            if 'subj' in token.dep_:
                subject = token.text
            if 'obj' in token.dep_:
                object_ = token.text

            if token.pos_ == 'VERB':
                verb = token.lemma_

        # Print relationships if subject, verb, and object are identified
        if subject and object_ and verb:
            # rest of the subjects
            if subject not in entities.keys():
                counter += 1
                entities[subject] = counter
                entity_obj = {"id": counter, "name": object_, "label": "OTHER"}
                json_data["entities"].append(entity_obj)

            # common nouns
            if object_ not in entities.keys():
                counter += 1
                entities[object_] = counter
                entity_obj = {"id": counter, "name": object_, "label": "COMMON_NOUN"}
                json_data["entities"].append(entity_obj)

            # triplets
            relation_obj = {"source": entities[subject], "target": entities[object_], "relation": verb}
            json_data["relationships"].append(relation_obj)

    return json_data

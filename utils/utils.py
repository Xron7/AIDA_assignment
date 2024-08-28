import networkx as nx
import matplotlib.pyplot as plt
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

                # phrasal verb
                for child in token.children:
                    if child.dep_ == "prep" and child.pos_ == "ADP":
                        verb = f"{verb} {child.text}"

        # Print relationships if subject, verb, and object are identified
        if subject and object_ and verb:
            # rest of the subjects
            if subject not in entities.keys():
                counter += 1
                entities[subject] = counter
                entity_obj = {"id": counter, "name": subject, "label": "OTHER"}
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


# visualizes a graph
def visualize_graph(json_data):
    G = nx.DiGraph()

    # Add entities (nodes) to the graph
    entities = {entity['id']: entity['name'] for entity in json_data['entities']}
    for entity_id, entity_name in entities.items():
        G.add_node(entity_id, label=entity_name)

    # Add relationships (edges) to the graph
    for relationship in json_data['relationships']:
        source = relationship['source']
        target = relationship['target']
        relation = relationship['relation']
        G.add_edge(source, target, label=relation)

    # Define positions for a better layout
    pos = nx.spring_layout(G)

    # Draw the nodes with labels
    nx.draw(G, pos, with_labels=True, labels=entities, node_color='lightblue', node_size=3000, font_size=10,
            font_weight='bold', arrows=True)

    # Draw the edges with labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    # Display the graph
    plt.title("Knowledge Graph Visualization")
    plt.show()
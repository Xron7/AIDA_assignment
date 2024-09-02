# gets the api key from the text file
def get_key(file="api_key.txt"):
    f = open(file, "r")
    api_key = f.read().strip()
    f.close()
    return api_key


# simplifies a sentence (removes he/his/him and who/that/which etc.)
def simplify_text(text, client):
    prompt = ("Transform the following sentences by replacing all pronouns (e.g., he, she, it, they, his, her, "
              "their) and relative clauses (e.g., who, that, which) with the corresponding actual entities, "
              "ensuring that the text remains grammatically correct and clear. Focus on maintaining the original "
              "meaning while explicitly stating each entity.")
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

# checks if the noun is needed to be appended as an entity
def noun_2_entity(noun, entity_list):
    string_lists = [string.split() for string in entity_list]

    actual_entity = 0
    for sublist in string_lists:
        if noun in sublist:
            actual_entity = ' '.join(sublist)

    return actual_entity


# gets the attributes of the entity from the doc
def get_attributes(entity, doc):
    attributes    = []
    enhance_types = ['compound', 'conj', 'amod']

    for token in doc:
        token_head = token.head

        if token_head.text == entity and token.dep_ == "amod":
            attributes.append(token.text)

            for child in token.children:
                if child.dep_ in enhance_types:
                    attributes.append(child.text)

        if token.text == entity and token_head.dep_ == 'ROOT':
            for child in token_head.children:
                if child.dep_ == 'attr':
                    attributes.append(child.text)

                    for subchild in child.children:
                        if subchild.dep_ in enhance_types:
                            attributes.append(subchild.text)

    return {f"attribute{i+1}": value for i, value in enumerate(attributes)}


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
        ent_name = ent.text
        if ent_name not in entities.keys():
            counter += 1
            entities[ent_name] = counter

            # get the head
            ent_head = ent_name
            for token in ent:
                if 'subj' in token.dep_ or 'obj' in token.dep_:
                    ent_head = token.text
                    break

            entity_obj = {"id": counter, "name": ent.text, "label": ent.label_, "noun_type": "PROPER", "attributes": get_attributes(ent_head, doc)}

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
            subj_entity = noun_2_entity(subject, entities.keys())
            obj_entity  = noun_2_entity(object_, entities.keys())

            # no matches found, needs to be added
            if subj_entity == 0:
                counter += 1
                entities[subject] = counter
                entity_obj = {"id": counter, "name": subject, "label": "OTHER", "noun_type": "COMMON", "attributes": get_attributes(subject, doc)}
                json_data["entities"].append(entity_obj)
            # else replace with the complete
            else:
                subject = subj_entity

            # common nouns
            # no matches found, needs to be added
            if obj_entity == 0:
                counter += 1
                entities[object_] = counter
                entity_obj = {"id": counter, "name": object_, "label": "COMMON_NOUN", "noun_type": "COMMON", "attributes": get_attributes(object_, doc)}
                json_data["entities"].append(entity_obj)
            else:
                object_ = obj_entity

            # triplets
            relation_obj = {"source": entities[subject], "target": entities[object_], "relation": verb}
            json_data["relationships"].append(relation_obj)

    return json_data


# visualizes a graph
def visualize_graph(json_data):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()

    # Add entities (nodes) to the graph
    entities = {}
    node_sizes = []
    for ent in json_data['entities']:
        attributes = ent['attributes']
        attributes_str = '\n '.join(f'{k}: {v}' for k, v in attributes.items()) if attributes else ''
        ent_name = ent['name']
        ent_label = f'{ent_name}\n {attributes_str}'

        entities[ent['id']] = ent_label

        # calculate node size
        num_lines = len(attributes) + 1
        max_line_length = max(len(line) for line in ent_label.split("\n"))

        node_sizes.append(max_line_length * 600 + num_lines * 800)

    for entity_id, entity_name in entities.items():
        G.add_node(entity_id)

    # Add relationships (edges) to the graph
    for relationship in json_data['relationships']:
        source = relationship['source']
        target = relationship['target']
        relation = relationship['relation']
        G.add_edge(source, target, label=relation)

    # Define positions for a better layout
    pos = nx.spring_layout(G)

    # Draw the nodes with labels
    nx.draw(G, pos, with_labels=True, labels=entities, node_color='lightblue', node_size=node_sizes, font_size=10,
            font_weight='bold', arrows=True)

    # Draw the edges with labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    # Display the graph
    plt.title("Knowledge Graph Visualization")
    plt.show()

    return None

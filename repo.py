# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1buQMBtTqGwpb4Opyj7mIea9nUAoaV_y1
"""

import networkx as nx
import matplotlib.pyplot as plt
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

# Step 1: Initialize NER Pipeline
def initialize_ner_pipeline(model_name):
    return pipeline("ner", model=model_name)

# Step 2: Extract Entities
def extract_entities(ner_pipeline, sentence):
    return ner_pipeline(sentence)

# Step 3: Create Knowledge Graph
def create_knowledge_graph(entities):
    G = nx.DiGraph()

    # Add nodes with labels
    for entity in entities:
        G.add_node(entity['word'], label=entity['entity'])

    # Add edges based on proximity
    for i in range(len(entities) - 1):
        G.add_edge(entities[i]['word'], entities[i + 1]['word'])

    return G

# Step 4: Draw Knowledge Graph
def draw_knowledge_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black')
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# Step 5: Enhance Knowledge Graph with Dependency Parsing
def enhance_knowledge_graph(sentence):
    # Load dependency parsing model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("Davlan/bert-base-multilingual-cased-ner-hrl")
    model = AutoModelForTokenClassification.from_pretrained("Davlan/bert-base-multilingual-cased-ner-hrl")

    # Initialize the NER pipeline
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    result = nlp(sentence)

    entities = [(res['word'], res['entity']) for res in result]

    # Create a new graph
    G = nx.DiGraph()

    # Add nodes and edges based on extracted entities
    for i, entity in enumerate(entities):
        G.add_node(entity[0], label=entity[1])
        if i > 0:
            G.add_edge(entities[i - 1][0], entity[0])

    # Draw the enhanced graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black')
    plt.show()

# Main function to run the steps
def main():
    model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
    sentence = "Barack Obama was born in Hawaii. He was elected president in 2008."

    # Step 1: Initialize NER pipeline
    ner_pipeline = initialize_ner_pipeline(model_name)

    # Step 2: Extract entities
    entities = extract_entities(ner_pipeline, sentence)
    print("Extracted Entities:", entities)

    # Step 3: Create knowledge graph
    G = create_knowledge_graph(entities)

    # Step 4: Draw the knowledge graph
    draw_knowledge_graph(G)

    # Step 5: Enhance and draw knowledge graph with dependency parsing
    enhance_knowledge_graph(sentence)

# Run the main function
if __name__ == "__main__":
    main()
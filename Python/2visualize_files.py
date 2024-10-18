import os
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import sys
from ipywidgets import Output, Button, HBox, VBox
from IPython.display import display

# Folder parsing
def parse_folder(folder_path):
    folder_structure = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            folder_structure[os.path.join(root, file)] = {'type': 'file', 'connections': 0}
        for dir in dirs:
            folder_structure[os.path.join(root, dir)] = {'type': 'folder', 'connections': 0}
    return folder_structure

# Graph creation
def create_graph(folder_structure):
    G = nx.DiGraph()
    for node, props in folder_structure.items():
        G.add_node(node, type=props['type'], connections=props['connections'])
        if props['type'] == 'folder':
            for child in folder_structure:
                if child.startswith(node):
                    G.add_edge(node, child)
    return G

# Interactive visualization
def visualize_graph(G):
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.spring_layout(G)
    node_colors = ['blue' if node[1]['type'] == 'folder' else 'red' for node in G.nodes(data=True)]
    node_sizes = [node[1]['connections'] * 100 for node in G.nodes(data=True)]
    nx.draw_networkx(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
    plt.axis('off')

    # Create interactive widgets
    output = Output()
    with output:
        display(fig)
    button = Button(description='Open file')
    button.on_click(lambda b: open_file(b, G))
    hbox = HBox([button])
    vbox = VBox([output, hbox])
    display(vbox)

def open_file(b, G):
    node_id = b.description
    node = G.nodes[node_id]
    if node['type'] == 'file':
        # Open file using default application
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', node_id])
        elif sys.platform == 'linux':  # Linux
            subprocess.run(['xdg-open', node_id])
        else:  # Windows
            os.startfile(node_id)

# Main program
folder_path = '/Users/flenski/Documents/Coding/histograms'  # Replace with your folder path
folder_structure = parse_folder(folder_path)
G = create_graph(folder_structure)
visualize_graph(G)
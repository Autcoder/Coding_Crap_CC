import os
import networkx as nx
import matplotlib.pyplot as plt


def traverse_directory(directory, max_depth=None):
    """
    Traverse the directory and return a list of edges (parent, child) for the graph.
    Also returns a dictionary indicating whether a node is a file or a directory.
    """
    edges = []
    node_types = {directory: "dir"}  # Initialize the root directory as a 'dir'

    def add_edges(root, dirs, files):
        for d in dirs:
            child_path = os.path.join(root, d)
            edges.append((root, child_path))
            node_types[child_path] = "dir"
        for f in files:
            child_path = os.path.join(root, f)
            edges.append((root, child_path))
            node_types[child_path] = "file"

    for root, dirs, files in os.walk(directory):
        depth = root[len(directory) :].count(os.sep)
        if max_depth is not None and depth >= max_depth:
            del dirs[:]  # Don't recurse further
        add_edges(root, dirs, files)

    return edges, node_types


def build_graph(edges, node_types):
    """
    Build a graph using the edges from the directory traversal and label node types.
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)
    nx.set_node_attributes(G, node_types, "type")
    return G


def visualize_graph(G):
    """
    Visualize the graph using matplotlib, differentiating between files and directories.
    """
    pos = nx.spring_layout(G, k=0.1)  # positions for all nodes

    plt.figure(figsize=(12, 8))

    dir_nodes = [n for n, attr in G.nodes(data=True) if attr["type"] == "dir"]
    file_nodes = [n for n, attr in G.nodes(data=True) if attr["type"] == "file"]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=dir_nodes,
        node_shape="o",
        node_color="skyblue",
        label="Directories",
        node_size=50,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=file_nodes,
        node_shape="s",
        node_color="lightgreen",
        label="Files",
        node_size=50,
    )

    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10)

    labels = {node: os.path.basename(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Only add legend if there are any nodes
    if dir_nodes or file_nodes:
        plt.legend(scatterpoints=1)

    plt.show()


def main(directory, max_depth=None):
    edges, node_types = traverse_directory(directory, max_depth)
    G = build_graph(edges, node_types)
    visualize_graph(G)


if __name__ == "__main__":
    print("Example: /Users/flenski/Documents")
    directory = input("Enter the directory to visualize: ")
    max_depth = input(
        "Enter the maximum depth to traverse (or leave blank for no limit): "
    )
    max_depth = int(max_depth) if max_depth else None
    main(directory, max_depth)

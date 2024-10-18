import os
import networkx as nx
import plotly.graph_objects as go


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
    Visualize the graph using plotly, differentiating between files and directories.
    """
    pos = nx.spring_layout(G, k=0.1)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(os.path.basename(node))
        node_color.append("skyblue" if G.nodes[node]["type"] == "dir" else "lightgreen")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        marker=dict(showscale=False, color=node_color, size=10, line_width=2),
        textposition="top center",
        hoverinfo="text",
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        ),
    )

    fig.show()


def main(directory, max_depth=None):
    edges, node_types = traverse_directory(directory, max_depth)
    G = build_graph(edges, node_types)
    visualize_graph(G)


if __name__ == "__main__":
    directory = input("Enter the directory to visualize: ")
    max_depth = input(
        "Enter the maximum depth to traverse (or leave blank for no limit): "
    )
    max_depth = int(max_depth) if max_depth else None
    main(directory, max_depth)

# Function to get shortest paths from source to all other nodes in the graph
import networkx as nx
import pdb

def get_shrtt_paths_from_src(g, Params):
    srcNode = Params['srcNode']
    numNodes = Params['numNodes']

    # generate networkx graph
    gnx = nx.Graph()

    for indNode in range(numNodes):
        gnx.add_node(indNode)
    
    for indNodeRow in range(numNodes):
        for indNodeCol in g[indNodeRow]:
            if indNodeCol>indNodeRow:
                gnx.add_edge(indNodeRow, indNodeCol)
    
    shrttPathsList = nx.single_source_shortest_path_length(gnx, srcNode)
     
    return shrttPathsList

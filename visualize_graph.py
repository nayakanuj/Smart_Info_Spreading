import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pdb

def visualize_graph(G, g, blfMat, pos, Params):

    srcQ = Params['srcQNode']
    srcR = Params['srcRNode']
    numNodes = Params['numNodes']
    graphName = Params['graphName']
    
    #G = nx.random_geometric_graph(200, 0.125)
    # position is stored as node attribute data for random_geometric_graph
   
    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5)**2 + (y - 0.5)**2
        if d < dmin:
            ncenter = n
            dmin = d

    plt.figure(100, figsize=(8, 8))
    plt.gcf().clear()

    # q to 
    

    # edge thickness according to action-values
    #for indNode in range(numNodes)
        #for nbr in g[ind]
    if graphName == 'grid2d':
        pos = dict((n, n) for n in G.nodes())
        nx.draw_networkx_edges(G, pos, alpha=0.1)
    else: #graphName == 'rgg':
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.1)

    for indNode in range(numNodes):
        alphaVal = (blfMat[indNode][0]/(blfMat[indNode][0]+blfMat[indNode][1]))
        if graphName == 'grid2d':
            indNodeRow = int(indNode/Params['numNodesRow'])
            indNodeCol = np.mod(indNode, Params['numNodesRow'])
            indNode4Grid = (indNodeRow, indNodeCol)
            srcRRow = int(srcR/Params['numNodesRow'])
            srcRCol =  np.mod(srcR, Params['numNodesRow']) 
            srcR4Grid = (srcRRow, srcRCol)
            nx.draw_networkx_nodes(G,pos, nodelist=[indNode4Grid, srcR4Grid],node_color='r', node_size=100, alpha=0.8*alphaVal)
        else: #graphName == 'rgg':
            nx.draw_networkx_nodes(G,pos, nodelist=[indNode, srcR],node_color='r', node_size=100, alpha=0.8*alphaVal)

        if graphName == 'pa':
            plt.xlim(-0.015, 0.015)
            plt.ylim(-0.015, 0.015)
            plt.axis('off')   
        elif graphName == 'pa' and numNodes == 1000:
            plt.xlim(-0.035, 0.035)
            plt.ylim(-0.07, 0.07)
            plt.axis('off')   


        if graphName == 'rgg':
            plt.xlim(-0.05, 1.05)
            plt.ylim(-0.05, 1.05)
            plt.axis('off')   

    plt.show(block=False)



    for indNode in range(numNodes):
        alphaVal = (blfMat[indNode][1]/(blfMat[indNode][0]+blfMat[indNode][1]))
        if graphName == 'grid2d':
            indNodeRow = int(indNode/Params['numNodesRow'])
            indNodeCol = np.mod(indNode, Params['numNodesRow'])
            indNode4Grid = (indNodeRow, indNodeCol)
            srcQRow = int(srcQ/Params['numNodesRow'])
            srcQCol =  np.mod(srcQ, Params['numNodesRow']) 
            srcQ4Grid = (srcQRow, srcQCol)
            nx.draw_networkx_nodes(G,pos, nodelist=[indNode4Grid, srcQ4Grid],node_color='b', node_size=100, alpha=0.8*alphaVal)
        else: #graphName == 'rgg':
            nx.draw_networkx_nodes(G,pos, nodelist=[indNode, srcQ],node_color='b', node_size=100, alpha=0.8*alphaVal)

        if graphName == 'rgg':
            plt.xlim(-0.05, 1.05)
            plt.ylim(-0.05, 1.05)
            plt.axis('off')

        if graphName == 'pa' and numNodes == 500:
            plt.xlim(-0.015, 0.015)
            plt.ylim(-0.015, 0.015)
            plt.axis('off')   
        elif graphName == 'pa' and numNodes == 1000:
            plt.xlim(-0.035, 0.035)
            plt.ylim(-0.07, 0.07)
            plt.axis('off')   

    if Params['qLrnEn'] == True:
        plt.title('With Q-learning')
    else:
        plt.title('Without Q-learning')

    plt.show(block=False)



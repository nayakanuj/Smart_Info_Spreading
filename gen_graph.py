# Function to generate graphs given topological parameters
# Input: Params
# Outputs: gn           - graph as list of neighbors
#          numNbrDict   - dictionary of number of neighbors of each node
#          g            - networkx graph

import networkx as nx
import numpy as np
import pdb
import copy

def gen_graph(Params):
    # 2D grid graph
    if Params['graphName'] == 'grid2d':
        #g = nx.grid_2d_graph(Params['numNodesRow'], Params['numNodesCol'])
        g = nx.grid_graph(dim=[Params['numNodesRow'], Params['numNodesCol']])
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        gnodes = [xx for xx in g.nodes()]

        for ind in range(g.number_of_nodes()):
            nodeRow = gnodes[ind][0]
            nodeCol = gnodes[ind][1]
            nodeIndex = nodeRow*Params['numNodesRow']+nodeCol
            neighborList = [xx for xx in nx.neighbors(g, gnodes[ind])]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn][0]*Params['numNodesRow']+neighborList[indnn][1])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[nodeIndex] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[nodeIndex] = len(nnList)
            del nnList[:]

    # 3D grid graph
    elif Params['graphName'] == 'grid3d':
        g = nx.grid_graph(dim=[Params['numNodesDim1'], Params['numNodesDim2'], Params['numNodesDim3']])
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        gnodes = [xx for xx in g.nodes()]
        for ind in range(g.number_of_nodes()):
            nodeDim1 = gnodes[ind][0]
            nodeDim2 = gnodes[ind][1]
            nodeDim3 = gnodes[ind][2]
            nodeIndex = nodeDim1*Params['numNodesDim2']*Params['numNodesDim3']+nodeDim2*Params['numNodesDim3']+nodeDim3
            neighborList = nx.neighbors(g, gnodes[ind])
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn][0]*Params['numNodesDim2']*Params['numNodesDim3']+neighborList[indnn][1]*Params['numNodesDim3']+neighborList[indnn][2])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[nodeIndex] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[nodeIndex] = len(nnList)
            del nnList[:]

    # Random Geometric Graph
    elif Params['graphName'] == 'rgg':
        g = nx.random_geometric_graph(Params['numNodes'], radius = Params['rggRad'], seed=0)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            #neighborList = nx.neighbors(g, g.nodes()[ind])
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

#        for ind in range(Params['numNodes']):
#            print(gn[ind])

    # Power-law tree graph
    elif Params['graphName'] == 'pltree':
        g = nx.random_powerlaw_tree(Params['numNodes'], gamma=Params['pltreegamma'], seed=None, tries = 10000)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

    # Preferential attachment graph
    elif Params['graphName'] == 'pa':
        g = nx.barabasi_albert_graph(n=Params['numNodes'], m=Params['mVal'], seed=None)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

    elif Params['graphName'] == 'er':
        pEr = (2*np.log(Params['numNodes']))/Params['numNodes']
        g = nx.gnp_random_graph(Params['numNodes'], p=pEr, seed=None, directed=False)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

    elif Params['graphName'] == 'wxrnd':
        g = nx.waxman_graph(Params['numNodes'], alpha=Params['alphaWxRnd'], beta=Params['betaWxRnd'], L=None, domain=(0,0,1,1))
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

    elif Params['graphName'] == 'plclust':
        g = nx.powerlaw_cluster_graph(Params['numNodes'], m=Params['mVal'],p=Params['pTriangle'], seed=None)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

    elif Params['graphName'] == 'dgm':
        g = nx.dorogovtsev_goltsev_mendes_graph(Params['depthParam'], create_using=None)
        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]

        # graph as neighbor list
        gn = {}
        nnList = []
        numNbrDict = {}
        for ind in range(g.number_of_nodes()):
            neighborListPrime = nx.neighbors(g, ind)
            neighborList = [x for x in neighborListPrime]
            for indnn in range(len(neighborList)):
                nnList.append(neighborList[indnn])

            # check which one is convenient
            #gn[nodeIndex] = np.array(nnList) # gn as dictionary of numpy arrays
            gn[ind] = copy.copy(nnList) # gn as dictionary of lists
            numNbrDict[ind] = len(nnList)
            del nnList[:]         

    return (gn, numNbrDict, g)
    

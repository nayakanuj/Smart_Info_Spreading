import networkx as nx
import pdb
import matplotlib.pyplot as plt

def display_centralities(gnx, srcQ, srcR):

    
    cntraltyEigVec = nx.eigenvector_centrality(gnx, max_iter=100, tol=1e-06, nstart=None, weight='weight')
    maxCntraltyEigVec = max(cntraltyEigVec.values())
    minCntraltyEigVec = min(cntraltyEigVec.values())
    print('srcQNode = ' + str(srcQ) + ', Eigenvector Centrality = ' +  str(cntraltyEigVec[srcQ]))
    print('srcRNode = ' + str(srcR) + ', Eigenvector Centrality = ' + str(cntraltyEigVec[srcR]))
    print('Max = ' + str(maxCntraltyEigVec) + ', Min = ' + str(minCntraltyEigVec))

    #print(" ")
    #
    #cntraltyBtw = nx.betweenness_centrality(gnx, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    #maxCntraltyBtw = max(cntraltyBtw.values())
    #minCntraltyBtw = min(cntraltyBtw.values())
    #print('srcQNode = ' + str(srcQ) + ', Betweenness Centrality = ' +  str(cntraltyBtw[srcQ]))
    #print('srcRNode = ' + str(srcR) + ', Betweenness Centrality = ' + str(cntraltyBtw[srcR]))
    #print('Max = ' + str(maxCntraltyBtw) + ', Min = ' + str(minCntraltyBtw))

    return [cntraltyEigVec]



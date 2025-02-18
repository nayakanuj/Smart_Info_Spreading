import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pdb
import copy
import random
import sys

from boltzmann_explr_opin import boltzmann_explr_opin
from compute_prob import compute_prob
from gen_graph import gen_graph
from prune_feed import prune_feed
from normalize_vector import normalize_vector
from load_graph import load_graph
from visualize_graph import visualize_graph
from display_centralities import display_centralities
from save_results_qopin import save_results_qopin

def qopin_tb(sim, Params):

    #Initialization
    seed = sim['iterNum']
    random.seed(seed)

    rememberingFactor = 1

    blfBatchSize = Params['blfBatchSize']

    gammVal = Params['gammaVal'] 
    if Params['genGraphFlg'] == True:
        (g, numNbrDict, gnx) = gen_graph(Params)
    else:
        (g, numNbrDict, gnx) = load_graph(Params)


    if Params['graphName'] == 'rgg' or Params['graphName'] == 'grid2d':
        pos = nx.get_node_attributes(gnx, 'pos')
    else:
        pos = nx.spectral_layout(gnx, scale=4)
        #pos = nx.shell_layout(gnx, scale=2)

    ########################## initialization begin #######################################
    # New params
    tauMax = Params['tauMax']
    learnRate = Params['learnRate']

    actionSet = {} # dict dict list
    
    # initializing src node, Q-table and action sets
    srcQNode = Params['srcQNode']
    srcRNode = Params['srcRNode']
    numNodes = Params['numNodes']
    # Display centralities and degrees of the nodes
    [cntraltyEigVec] = display_centralities(gnx, srcQNode, srcRNode)

    actionSet = g 
    
    Q = copy.deepcopy(actionSet)
    Qdel = copy.deepcopy(actionSet)
    cntMat = copy.deepcopy(actionSet)
   
    for indNode in range(numNodes):
        Q[indNode] = [0.5]*len(actionSet[indNode])
        cntMat[indNode] = [0]*len(actionSet[indNode]) 
        Qdel[indNode] = [0]*len(actionSet[indNode]) 
    informerDict = {x:[] for x in range(numNodes)}
    informeeDict = {x:[] for x in range(numNodes)}
    opinionList = []
    opinionListOppon = []
    feedList = {x:[[],[],[],[]] for x in range(numNodes)} # [[Q or R message],[time of reception],[incoming node], [No. of times msg is Tx]]
    infNodesDumpAllRnd = {} # For future use. Collecting stats of the nodes informed at each time slot for all rounds
    blfMat = np.ones((numNodes, 2))
    sumOpinionQ = np.array(Params['numRounds']*[0])
    sumOpinionR = np.array(Params['numRounds']*[0])

    #blfMatAllRnd = np.array([])
    blfMatAllRnd = list()

    #Loop for all rounds
    for indRnd in range(Params['numRounds']):

        if np.mod(indRnd, 10) == 0:
            print("Round", indRnd, end=",")
            sys.stdout.flush()
        
        #################### initialization - for each round - begin ####################
        qTxNodesList = []
        rTxNodesList = []
        qChosenFeedList = []
        rChosenFeedList = []
        infNodesDumpOneRnd = []
        infNodesDumpOneRnd.append([srcQNode])
         
        # initialize state sequence
        stateSeq = {x:[] for x in range(numNodes)}
        # keep a count of the number of occurence of each state-action pair (size of count matrix = size of action set)
        
        del qTxNodesList[:]
        del rTxNodesList[:]
        del qChosenFeedList[:]
        del rChosenFeedList[:]
        feedDelDict = {x:[] for x in range(numNodes)}
        blfMatPrev = copy.deepcopy(blfMat)
        
        # Loop for all nodes 
        for indNode in range(numNodes):
            # 1. Remove all the messages older than tauMax [TODO]
            feedList = prune_feed(feedList, indNode, int(indRnd/blfBatchSize), tauMax)
            # 2. If source node (Q or R), then
            if indNode == srcQNode:
                # collect infQ nodes
                qTxNodesList.append(indNode)
                qChosenFeedList.append(0)
            elif indNode == srcRNode:
                # collect infR nodes
                rTxNodesList.append(indNode)
                rChosenFeedList.append(0)
            else:
                # check if feedsize>0
                if len(feedList[indNode][0]) != 0:
                    # Choose a message from list w.p. exp(-tau)
                    # Get probability vector from exp(-tau)
                    [probFeedVec, noTx] = compute_prob(feedList[indNode][1],feedList[indNode][3],int(indRnd/blfBatchSize), Params['eta'], Params['xi'])
                    #if len(probFeedVec)>1:
                    #    pdb.set_trace()

                    if noTx == False:
                        if len(probFeedVec) == 1:
                            chosenFeedTmp = [0]
                        else:
                            chosenFeedTmp = np.random.choice(len(probFeedVec),1,p=probFeedVec)
                        
                        chosenFeed = chosenFeedTmp[0]
                        chosenMsg = feedList[indNode][0][chosenFeed]

                        # If no message chosen dont collect nodes otherwise collect - Does not occur now. We can consider finite buffer size [TODO]
                        # Collect qTx nodes or collect rTx nodes
                        if chosenMsg == 1:
                            qTxNodesList.append(indNode)
                            qChosenFeedList.append(chosenFeed)
                        else:
                            rTxNodesList.append(indNode)
                            rChosenFeedList.append(chosenFeed)                        


        # Loop for all qTx nodes
        for (loopInd, indNode) in enumerate(qTxNodesList):

            # 2. Compute p_q (probability of transmitting message m_q)
            probSendMsgBlf = blfMatPrev[indNode][1]/np.sum(blfMatPrev[indNode])
            # 3. sample sendMsgFlg using p_q
            sendMsgSamp = (np.random.rand(1,1)<=probSendMsgBlf)

            if indNode == srcQNode:
                sendMsgSamp = True
            # 4. If sendMsgFlg == True then 
            #   4.a. Choose recipient (neighbor) using action-values by Boltzmann exploration rule
            #   4.b. Update belief of the chosen recipient
            #   4.c. Compute reward, update Q-table
            #   4.d. send msg
            #   4.e. delete msg
            if sendMsgSamp == True:
                # 4.a. Choose a neighbor using boltzmann exploration rule
                if indNode == srcQNode:
                    incomingNodeIndex = []
                else:
                    chosenFeed = qChosenFeedList[loopInd] # location of the feed
                    incomingNode = feedList[indNode][2][chosenFeed] # incoming node for indNode
                
                    incomingNodeIndexTmp = np.where(np.array(g[indNode]) == incomingNode)
                    incomingNodeIndex = incomingNodeIndexTmp[0][0]
                    
                    if np.mod(indRnd, blfBatchSize) == 0:
                        feedList[indNode][3][chosenFeed] += 1

                seedInBoltzmann = random.randint(1,100000)
                [action, actionIdx] = boltzmann_explr_opin(Q[indNode], incomingNodeIndex, g[indNode], Params['tempVal'], seedInBoltzmann)
               
                # 4.b.
                #blfMat[action][1] += 1 
                if np.mod(indRnd, blfBatchSize) == 0:
                    #blfMat[action][1] = blfMat[action][1] + 1
                    blfMat[action][1] = blfMat[action][1]*rememberingFactor + 1 # for debug
                
                # 4.c.
                if Params['qLrnEn'] == True:
                    opinion = blfMatPrev[action][1]/np.sum(blfMatPrev[action])
                    #rwdImm = 10*opinion*(1-opinion)/blfMatPrev[action][1] # for debug
                    rwdImm = opinion*(1-opinion)/blfMatPrev[action][1]
                    Qmax = np.max(Q[action])
                    Q[indNode][actionIdx] = (1-learnRate)*Q[indNode][actionIdx]+learnRate*(rwdImm+gammVal*Qmax)
                
                ## 4.e. Delete feed and related records from feedList of indNode
                if np.mod(indRnd, blfBatchSize) == 0:
                    if indNode != srcQNode:
                        feedDelDict[indNode].append(chosenFeed)

                    # 4.f Append feed and related records in feedList of action node
                    feedList[action][0].append(1) # message
                    feedList[action][1].append(int(indRnd/blfBatchSize)) # time
                    feedList[action][2].append(indNode) # incoming node
                    feedList[action][3].append(0) # Number of times msg is Tx 
                
        
        if np.mod(indRnd, blfBatchSize) == 0:
            # Loop for all rTx nodes
            for (loopInd, indNode) in enumerate(rTxNodesList):

                # 2. Compute p_r (probability of transmitting message m_q)
                probSendMsgBlf = blfMatPrev[indNode][0]/np.sum(blfMatPrev[indNode])
                # 3. sample sendMsgFlg using p_q
                sendMsgSamp = (np.random.rand(1,1)<=probSendMsgBlf)

                if indNode == srcRNode:
                    sendMsgSamp = True

                if sendMsgSamp == True:
                    # 4.a. Choose a neighbor using boltzmann exploration rule
                    if indNode == srcRNode:
                        incomingNodeIndex = []
                    else:
                        chosenFeed = rChosenFeedList[loopInd] # location of the feed
                        incomingNode = feedList[indNode][2][chosenFeed]
                        incomingNodeIndexTmp = np.where(np.array(g[indNode]) == incomingNode)
                        incomingNodeIndex = incomingNodeIndexTmp[0][0]               
                        feedList[indNode][3][chosenFeed] += 1
                    
                    seedInBoltzmann = random.randint(1,100000)
                    [action, actionIdx] = boltzmann_explr_opin([1]*numNbrDict[indNode], incomingNodeIndex, g[indNode], Params['tempVal'], seedInBoltzmann)
                    
                    # 4.b.
                    #blfMat[action][0] += 1 
                    # no need to check mod(.,.). Because....refer to if
                    # condition outside the for loop
                    blfMat[action][0] = blfMat[action][0]*rememberingFactor + 1 # for debug
                    
                    if indNode != srcRNode:
                        feedDelDict[indNode].append(chosenFeed)

                    # 4.f Append feed and related records in feedList of action node
                    feedList[action][0].append(0) # message
                    feedList[action][1].append(int(indRnd/blfBatchSize)) # time
                    feedList[action][2].append(indNode) # incoming node
                    feedList[action][3].append(0) # Number of times msg is Tx 

        ##deleting feeds
        #for indNode in range(numNodes):
        #    if len(feedDelDict[indNode])>0:
        #        for ind in sorted(feedDelDict[indNode], reverse=True):
        #            del feedList[indNode][0][ind]
        #            del feedList[indNode][1][ind]
        #            del feedList[indNode][2][ind]
        #            del feedList[indNode][3][ind]
        #        del feedDelDict[indNode][:]


        if np.mod(indRnd, blfBatchSize) == 0:
            muiList = np.divide(blfMat[:,1], np.sum(blfMat, 1))
            opinionList.append(np.sum(muiList))
            muiOpponList = np.divide(blfMat[:,0], np.sum(blfMat, 1))
            opinionListOppon.append(np.sum(muiOpponList))

        #if indRnd == 0:
        #    blfArr = np.atleast_2d(blfMat[:,0])
        #    blfArr = np.append(blfArr, np.atleast_2d(blfMat[:,1]), axis=1)
        #    blfMatAllRnd = np.atleast_3d(blfArr)
        #else:
        #    blfArr = np.atleast_2d(blfMat[:,0])
        #    blfArr = np.append(blfArr, np.atleast_2d(blfMat[:,1]), axis=1)
        #    blfMatAllRnd = np.append(blfMatAllRnd, np.atleast_3d(blfArr), axis=2)
        
            blfMatAllRnd.append(blfMat)

        #if np.mod(indRnd,50*blfBatchSize) == 0 or indRnd == Params['numRounds']-1:
        ##if indRnd == Params['numRounds']-1:
        #    visualize_graph(gnx, g, blfMat, pos, Params)
        #    plt.pause(0.01)
        #    pdb.set_trace()


    if Params['saveSimresFlg'] == True:
        dumpVarNames = ['opinionList', 'opinionListOppon','blfMatAllRnd','cntraltyEigVec']
        dumpVarVals = [opinionList, opinionListOppon, blfMatAllRnd, cntraltyEigVec]
    
        save_results_qopin(sim, Params, dumpVarNames, dumpVarVals)

    plt.figure(2)
    plt.plot(opinionList, linewidth=4, markersize=10, label='opinion-1')
    plt.plot(opinionListOppon, linewidth=4, markersize=10, label='opinion-2')
    plt.ylabel("Sum opinions", fontsize=24)
    plt.xlabel("Round", fontsize=24)

    if Params['qLrnEn'] == True:
        plt.title('with Q-learning', fontsize=24)
    else:
        plt.title('without Q-learning', fontsize=24)

    print(" ")
    plt.grid(True)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.legend(fontsize=20)
    #plt.ylim((140, 360))
    plt.show()
    plt.show(block=False)


    plt.figure(3)
    plt.hist(muiList, bins=10, label='opinion-1')
    plt.hist(muiOpponList, bins=10, label='opinion-2')
    plt.ylabel("Frequency", fontsize=24)
    plt.xlabel("Opinion", fontsize=24)

    if Params['qLrnEn'] == True:
        plt.title('with Q-learning', fontsize=24)
    else:
        plt.title('without Q-learning', fontsize=24)

    print(" ")
    plt.grid(True)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.legend(fontsize=20)
    #plt.ylim((140, 360))
    plt.show()
    plt.show(block=False)

    plt.figure(4)
    visualize_graph(gnx, g, blfMat, pos, Params)
    plt.show()
    plt.show(block=False)


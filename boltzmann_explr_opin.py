import numpy as np
import pdb

def boltzmann_explr_opin(qList, incomingNodeIndex, gList, tempVal, seedIn):

    np.random.seed(seedIn)
    if incomingNodeIndex != []:
        qList[incomingNodeIndex] = 0
    maxQ = max(qList)
    maxQTmp = maxQ/tempVal
    MAXQTMPALLOWED = 500
    MAXQALLOWED = MAXQTMPALLOWED*tempVal
    if maxQTmp>MAXQTMPALLOWED:
        subtractQ = maxQ-MAXQALLOWED
        qListNew = [xx-subtractQ for xx in qList]
        print("Q", end=' ')
    elif maxQ<0:
        qListNew = [xx-((maxQ)*tempVal) for xx in qList]
        pdb.set_trace()
    else:
        qListNew = qList

    expQList = [np.exp(x/tempVal) for x in qListNew]
    pDenom = float(sum(expQList))

    #if pDenom == 0: # often encountered in local cooperation case with exp(.) scaling factor
    #    pDenom = 1 # helps in case of local cooperation with exp(.) scaling factor
    #    for ii in range(len(expQList)):
    #        expQList[ii] = 1.0/len(expQList)

    pList = [float(x)/pDenom for x in expQList]

    rndIdx = np.random.choice(len(pList),1,p=pList)

    actionIdx = rndIdx[0]
    action = gList[actionIdx]
     
    return [action, actionIdx]

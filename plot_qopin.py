import numpy as np
import matplotlib.pyplot as plt
import pdb
import os.path
from get_params_list2plot_qopin import *

markerList = ['k-o','b-s','r-^','k-s','b-^','r-o','k-^','b-o','r-s']

for ind, numNodes in enumerate(numNodesList):
    numNodes        = numNodesList[ind]
    numPts          = numPtsList[ind]
    srcQNode        = srcQNodeList[ind]          
    srcRNode        = srcRNodeList[ind]          
    learnRate       = learnRateList[ind]        
    gammaVal        = gammaValList[ind]         
    blfBatchSize       = blfBatchSizeList[ind]        
    tempVal         = tempValList[ind]          
    graphName       = graphNameList[ind]        
    mVal            = mValList[ind]             
    rggRad          = rggRadList[ind]
    qLrnEn          = qLrnEnList[ind]
    tauMax          = tauMaxList[ind]
    eta             = etaList[ind]
    xi              = xiList[ind]

    saveFileNameHead = saveFileNameHead
    
    if graphName =='rgg':
        fileName = savePath+"/"+saveFileNameHead+"nodes"+str(numNodes) \
                +"rnd"+str(numRounds)+ "qLrnEn" + str(qLrnEn) + "lrnRate"+ str(learnRate) + "gam" + str(gammaVal) + "gamEx" + str(gammaExtraVal) + "temp" + str(tempVal) + "blfBchSz"+str(blfBatchSize)+"grph"+graphName+"rggRad"+str(rggRad)

    elif graphName == 'pa':
        fileName = savePath+"/"+saveFileNameHead+"nodes"+str(numNodes) \
                +"slt"+str(numPts)+ "lrnRate"+ \
                str(learnRate) + "gam" + str(gammaVal) \
                + "temp" + str(tempVal) + "tauMax" + str(tauMax) \
                + "blfBchSz"+str(blfBatchSize)+"grph"+graphName+'mVal'+str(mVal) \
                + "eta"+str(eta)+"xi"+str(xi) \
                + "srcQ"+str(srcQNode) \
                + "srcR"+str(srcRNode) \
                + "qLrnEn" + str(int(qLrnEn))

#    if ~os.path.exists(fileName+".npy"):
#        continue

    dumpVar = np.load(fileName+"0.npy")

    varNameList = dumpVar[0]
    varValList = dumpVar[1]
    nArg = len(varNameList)
    dct = {}

    # collecting all the variables in dictionary "dct"
    for indVar, varName in enumerate(varNameList):
        print(indVar)
        dct[varName] = varValList[indVar]
   
    opinionList = dct['opinionList']
    opinionListOppon= dct['opinionListOppon']
    blfMatAllRnd = dct['blfMatAllRnd']
    ## Opinion vs time slots
    
    # With Q-learning
    plt.figure(1)

    if(graphName == "rgg"):
        graphNameStr = "Random geometric graph: r = "+str(rggRad)
    elif(graphName == "pa"):
        graphNameStr = "PA graph: m = "+str(mVal)
    elif(graphName == 'er'):
        graphNameStr = 'ER graph'

    if qLrnEn == False:
        plt.plot(opinionList, linewidth=4, markersize=10, \
                label=" without Q-learning (opinion-1)")
    else:
        plt.plot(opinionList, linewidth=4, markersize=10, \
                label=" with Q-learning (opinion-1)")

    plt.ylabel("Sum of opinions", fontsize=24)
    plt.xlabel("Round", fontsize=24)

    # Without Q-learning
    plt.figure(1)
    if qLrnEn == False:
        plt.plot(opinionListOppon, linewidth=4, markersize=10, \
                label=" without Q-learning (opinon-2)")
    else:
        plt.plot(opinionListOppon, linewidth=4, markersize=10, \
                label=" with Q-learning (opinion-2)")

    plt.title(graphNameStr, fontsize=20)
    plt.ylabel("Sum of opinions", fontsize=24)
    plt.xlabel("Time-slot", fontsize=24)
    print(" ")


    if qLrnEn == True:
        # Conditional histogram
        plt.figure(2)
        blfMatLast = blfMatAllRnd[-1]
        muiList = np.divide(blfMatLast[:,1], np.sum(blfMatLast, 1))
        muiOpponList = np.divide(blfMatLast[:,0], np.sum(blfMatLast, 1))
        plt.title('with Q-learning', fontsize=24)
        plt.hist(muiList, bins=20, label='opinion-1')
        plt.hist(muiOpponList, bins=20, label='opinion-2')
    else:
        # Conditional histogram
        plt.figure(3)
        blfMatLast = blfMatAllRnd[-1]
        muiList = np.divide(blfMatLast[:,1], np.sum(blfMatLast, 1))
        muiOpponList = np.divide(blfMatLast[:,0], np.sum(blfMatLast, 1))
        plt.title('without Q-learning', fontsize=24)
        plt.hist(muiList, bins=20, label='opinion-1')
        plt.hist(muiOpponList, bins=20, label='opinion-2')
    
    plt.ylabel("Frequency", fontsize=24)
    plt.xlabel("Opinion", fontsize=24)
    print(" ")



for indFig in range(1,4):
    plt.figure(indFig)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.grid(True)
    plt.legend(fontsize=20)
    plt.legend(fontsize=20)
    plt.show(block=False)

pdb.set_trace()



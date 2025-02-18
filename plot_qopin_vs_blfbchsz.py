import numpy as np
import matplotlib.pyplot as plt
import pdb
import os.path
from get_params_list2plot_qopin import *

markerList = ['k-o','b-s','r-^','k-s','b-^','r-o','k-^','b-o','r-s']

finalOpinionList = []
finalOpinionListOppon = []

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

    finalOpinionList.extend([opinionList[-1]])
    finalOpinionListOppon.extend([opinionListOppon[-1]])

plt.figure(1)
if(graphName == "rgg"):
    graphNameStr = "Random geometric graph: r = "+str(rggRad)
elif(graphName == "pa"):
    graphNameStr = "PA graph: m = "+str(mVal)
elif(graphName == 'er'):
    graphNameStr = 'ER graph'

plt.plot(blfBatchSizeList, finalOpinionList, linewidth=4, markersize=10, \
            label="opinion-1")

plt.plot(blfBatchSizeList, finalOpinionListOppon, linewidth=4, markersize=10, \
            label="opinion-2")

plt.title(graphNameStr, fontsize=20)
plt.ylabel("Sum of opinions", fontsize=24)
plt.xlabel("R_Q", fontsize=24)
print(" ")

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.grid(True)
plt.legend(fontsize=20)
plt.legend(fontsize=20)
plt.show(block=False)

pdb.set_trace()



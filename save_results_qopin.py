import numpy as np
import pdb

def save_results_qopin(sim, Params, dumpVarNames, dumpVarVals):

    ## save results
    savePath = sim['savePath']
    saveFileNameHead = sim['saveFileNameHead']
    graphName = Params['graphName']

    if graphName =='rgg': # [TODO]
        fileName = savePath+"/"+saveFileNameHead+"nodes"+str(Params['numNodes']) \
                +"slt"+str(Params['numPts'])+ "lrnRate"+ \
                str(Params['learnRate']) + "gam" + str(Params['gammaVal']) \
                + "temp" + str(Params['tempVal']) \
                + "blfBchSz"+str(Params['blfBatchSize'])\
                +"grph"+graphName+"rggRad"+str(Params['rggRad']) \
                + "eta"+str(Params['eta']+"xi"+Params['xi']) \
                + "qLrnEn" + str(Params['qLrnEn'])
    elif graphName == 'pa':
        fileName = savePath+"/"+saveFileNameHead+"nodes"+str(Params['numNodes']) \
                +"slt"+str(Params['numPts'])+ "lrnRate"+ \
                str(Params['learnRate']) + "gam" + str(Params['gammaVal']) \
                + "temp" + str(Params['tempVal']) + "tauMax" + str(Params['tauMax']) \
                + "blfBchSz"+str(Params['blfBatchSize'])+"grph"+graphName+'mVal'+str(Params['mVal']) \
                + "eta"+str(Params['eta'])+"xi"+str(Params['xi']) \
                + "srcQ"+str(Params['srcQNode']) \
                + "srcR"+str(Params['srcRNode']) +"qLrnEn"+str(int(Params['qLrnEn']))

    dumpVar = []
    dumpVar.append(dumpVarNames)
    dumpVar.append(dumpVarVals)
   
    np.save(fileName+str(sim['iterNum']), dumpVar)



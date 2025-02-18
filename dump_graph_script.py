from gen_graph import gen_graph
import numpy as np

Params = {};
Params['graphName'] = 'pa'
#Params['graphName'] = 'grid2d'
#Params['graphName'] = 'wxrnd'
#Params['graphName'] = 'rgg'
#Params['graphName'] = 'plclust'

if Params['graphName'] == 'pa':
    Params['numNodes'] = 100000
    Params['mVal'] = 3
elif Params['graphName'] == 'grid2d':
    Params['numNodesRow'] = 10
    Params['numNodesCol'] = 10
    Params['numNodes'] = Params['numNodesRow']*Params['numNodesCol']
elif Params['graphName'] == 'rgg':
    Params['numNodes'] = 1000
    #Params['rggRad'] = 0.08
    #Params['rggRad'] = 0.17
    Params['rggRad'] = 0.07
elif Params['graphName'] == 'plclust':
    Params['numNodes']	= 500
    Params['mVal']      = 2
    Params['pTriangle'] = 0.5
elif Params['graphName'] == 'wxrnd':
    Params['numNodes']	= 500
    Params['alphaWxRnd'] = 0.045
    Params['betaWxRnd']  = 0.7

(g, numNbrDict, gnx) = gen_graph(Params)

dumpVarNames = ['g','numNbrDict','gnx'] 
dumpVarVals = [g, numNbrDict, gnx] 

dumpVar = []
dumpVar.append(dumpVarNames)
dumpVar.append(dumpVarVals)

## save results
savePath = 'graphDump'
graphName = Params['graphName']

if Params['graphName'] == 'pa':
    fileName = savePath+"/"+"nodes"+str(Params['numNodes'])+"mVal"+str(Params['mVal'])
elif Params['graphName'] == 'grid2d':
    fileName = savePath+"/"+"nodes"+str(Params['numNodes'])+"row"+str(Params['numNodesRow'])+"col"+str(Params["numNodesCol"])
elif Params['graphName'] == 'rgg':
    fileName = savePath+"/"+"nodes"+str(Params['numNodes'])+"rggRad"+str(Params['rggRad']) 
elif Params['graphName'] == 'plclust':
    fileName = savePath+"/"+"nodes"+str(Params['numNodes'])+"mVal"+str(Params['mVal'])+"pTriangle"+str(Params['pTriangle'])
elif Params['graphName'] == 'wxrnd':
    fileName = savePath+"/"+"nodes"+str(Params['numNodes'])+"alphaWxRnd"+str(Params['alphaWxRnd'])+"betaWxRnd"+str(Params['betaWxRnd'])
    
np.save(fileName, dumpVar)


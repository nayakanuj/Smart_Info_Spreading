import numpy as np

def load_graph(Params):
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
    
    loadGraphVar = np.load(fileName+".npy")

    g = loadGraphVar[1][0]
    numNbrDict = loadGraphVar[1][1]
    gnx = loadGraphVar[1][2]

    return (g, numNbrDict, gnx)

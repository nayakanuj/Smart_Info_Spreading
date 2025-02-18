from qopin_tb import qopin_tb
import sys


iterList = [0]

sim = {}
Params = {}
sim['savePath']             = "simRes"
sim['saveFileNameHead']     = "2024_18_02"
#Params['graphName']        = 'grid2d'
Params['graphName']        = 'rgg'
# Params['graphName']         = 'pa'
#Params['graphName']        = 'er'
# Params['genGraphFlg']       = False
Params['genGraphFlg']      = True
Params['eta']               = 0.   
Params['xi']                = 1.
Params['tauMax']            = 10
Params['blfBatchSize']      = 15
Params['numPts']            = 100
Params['qLrnEn']       = False
#Params['qLrnEn']       = True
Params['saveSimresFlg'] = False


print(Params['graphName'])


if Params['graphName'] == 'rgg':
    # Params['numNodes']	= 1000
    # Params['rggRad']	= 0.07
    # Params['numRounds']	= Params['numPts']*Params['blfBatchSize']
    # Params['srcRNode']	= 700
    # Params['srcQNode']	= 800
    # Params['learnRate']	= 0.01
    # Params['gammaVal']	= 0.9
    # Params['tempVal']	= 0.1

    Params['numNodes']	= 500
    Params['rggRad']	= 0.1
    Params['numRounds']	= 500
    Params['srcRNode']	= 10
    Params['srcQNode']	= 490
    Params['learnRate']	= 0.01
    Params['gammaVal']	= 0.9
    Params['tempVal']	= 0.1
    
    #Params['numNodes']	    = 100
    #Params['rggRad']	    = 0.17
    #Params['numRounds']	    = 520
    #Params['srcRNode']	    = 90
    #Params['srcQNode']	    = 80
    #Params['learnRate']	    = 0.05
    #Params['gammaVal']	    = 0.9
    #Params['tempVal']	    = 0.1

elif Params['graphName'] == 'er':
#    Params['numNodes']	= 1000
#    Params['numRounds']	= 1020
#    Params['freezeRound']	= 1001
#    Params['srcNode']	= 990
#    Params['learnRate']	= 0.03
#    Params['gammaVal']	= 0.9
#    Params['gammaExtraVal']= 0.2
#    Params['blfBatchSize']	= 50.
#    Params['tempVal']	= 0.2

    Params['numNodes']	= 500
    Params['numRounds']	= 1020
    Params['srcQNode']	= 495
    Params['srcRNode']	= 12
    Params['learnRate']	= 0.1
    Params['gammaVal']	= 0.8
    Params['tempVal']	= 0.1

elif Params['graphName'] == 'pa':
#    Params['numNodes']	= 1000
#    Params['mVal']      = 3
#    Params['numRounds']	= Params['numPts']*Params['blfBatchSize']
#    #Params['srcQNode']	= 900 # low degree low eigvec centrality
#    #Params['srcQNode']	= 46 # best case - high degree and second highest eigvec centrality
#    Params['srcQNode']	= 128 # high degree - low eigvec centrality
#    Params['srcRNode']	= 5 # Hub
#    Params['learnRate']	= 0.2
#    Params['gammaVal']	= 0.8
#    Params['tempVal']	= 0.1

    Params['numNodes']	= 500
    Params['mVal']  = 3
    Params['numRounds']	= Params['numPts']*Params['blfBatchSize']
    Params['srcQNode']	= 400
    #Params['srcQNode']	= 495
    #Params['srcRNode']	= 12
    Params['srcRNode']	= 1
    Params['learnRate']	= 0.1
    Params['gammaVal']	= 0.8
    Params['tempVal']	= 0.1

   #For Test
   # Params['numNodes']	= 100
   # Params['mVal']	        = 3
   # Params['numRounds']	= 120
   # Params['srcQNode']	= 75
   # Params['srcRNode']	= 85
   # Params['learnRate']	= 0.05
   # Params['gammaVal']	= 0.8
   # Params['tempVal']	= 0.1


for indIter in iterList:
    print("Iteration " + str(indIter))
    print("================================================= List of parameters - BEGIN =================================================")
    for paramName in Params.keys():
        print(paramName+" = ",Params[paramName])
    print("------------------------------------------------- List of parameters - END -------------------------------------------------")

    sim['iterNum'] = indIter
    qopin_tb(sim, Params) 


brkpnt1 = 1
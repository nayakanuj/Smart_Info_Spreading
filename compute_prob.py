import numpy as np
from normalize_vector import normalize_vector
import pdb

def compute_prob(vecIn1, vecIn2, t, eta, xi):

    # find minimum tau
    vecIn1Delta = np.add(vecIn1, -t) # vecIn1Delta is negative number

    minVecIn2 = np.min(vecIn2)
    
    #noTxTmp = (np.random.rand(1,1)>np.exp(-10*(minVecIn2))) # for debug
    #noTxTmp = (np.random.rand(1,1)>np.exp(0*(minVecIn2))) # for debug # this with vecInNeg2 factor = -3 works with pa graph
    #noTxTmp = (np.random.rand(1,1)>np.exp(-1*(minVecIn2))) # for debug # this with vecInNeg2 factor = -1 works with pa graph for batchsize of 20
    noTxTmp = (np.random.rand(1,1)>np.exp(-eta*(minVecIn2))) 
    noTx = noTxTmp[0][0]

    #noTx = False # for debug # works best
    
    if noTx == False:
        
        #vecInNeg1 = np.multiply(vecIn1Delta, 1) # works best
        #vecInNeg2 = np.multiply(vecIn2, 0.) # works best
        
        vecInNeg1 = np.multiply(vecIn1Delta, xi) 
        vecInNeg2 = np.multiply(vecIn2, eta) 
        
        vecInNeg = np.add(vecInNeg1, vecInNeg2)
        vecNegExp = np.exp(vecInNeg)
        probVec = normalize_vector(vecNegExp)
    else:
        probVec = []

    ##if noTx == False and minVecIn2>0 and len(vecIn1)>1:
    #if noTx == False and len(vecIn1)>1:
    #    print(sorted(vecIn1Delta, reverse=True))

    #if len(vecIn1)>1:
    #    pdb.set_trace()

    return [probVec, noTx]

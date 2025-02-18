# Function to normalize a vector
import numpy as np

def normalize_vector(vecIn):
    sumVal = np.sum(vecIn)
    vecNormalized = np.divide(vecIn, sumVal)
    return vecNormalized

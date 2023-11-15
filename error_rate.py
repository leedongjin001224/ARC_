import numpy as np
def error_rate(output, pred):
    return  (np.array(output) != np.array(pred)).sum() / (output.shape[0] * output.shape[1])
import numpy as np

def most_likely(input, output, just_shape=False):
    in_ = np.array(input)
    out_ = np.array(output)
    if just_shape:
        in_ = None

def zoom_in(input, output_shape):
    sample1 = np.zeros(output_shape, int)
    for i in range(0, output_shape[0], input.shape[0]):
        for j in range(0, output_shape[1], input.shape[1]):
            sample1[i:min(i+input.shape[0],output_shape[0]),j:min(j+input.shape[1],output_shape[1])] = input[:min(input.shape[0],output_shape[0]-i),:min(input.shape[1],output_shape[1]-j)]
    result = [sample1]
    m = output_shape[0] / input.shape[0]
    n = output_shape[1] / input.shape[1]
    if m == round(m) and n == round(n):
        m = round(m)
        n = round(n)
        sample2 = np.zeros(output_shape, int)
        sample3 = np.zeros(output_shape, int)
        reverse = np.ones(input.shape, int) * np.unique(input)[-1] - input
        sample4 = np.zeros(output_shape, int)
        sample5 = np.zeros(output_shape, int)
        i_ = 0
        for i in range(0, output_shape[0], input.shape[0]):
            j_ = 0
            for j in range(0, output_shape[1], input.shape[1]):
                if input[i_,j_]:
                    sample2[i:i+input.shape[0],j:j+input.shape[1]] = input
                    sample4[i:i+input.shape[0],j:j+input.shape[1]] = reverse
                else:
                    sample3[i:i+input.shape[0],j:j+input.shape[1]] = input
                    sample5[i:i+input.shape[0],j:j+input.shape[1]] = reverse
                j_ += 1
                if j_ == input.shape[1]:
                    j_ = 0
            i_ += 1
            if i_ == input.shape[0]:
                i_ = 0
        result += [sample2, sample3, sample4, sample5]
    return result
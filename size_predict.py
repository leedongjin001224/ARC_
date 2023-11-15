import numpy as np
import pandas as pd
import statsmodels.api as sm

def estimate_size(trains, test_input):
    train_inputs = [np.array(i['input']) for i in trains]
    train_outputs = [np.array(i['output']) for i in trains]
    test_input = np.array(test_input)
    v = pd.DataFrame({'input':[i.shape[0] for i in train_inputs], 'output':[i.shape[0] for i in train_outputs]})
    h = pd.DataFrame({'input':[i.shape[1] for i in train_inputs], 'output':[i.shape[1] for i in train_outputs]})
    v['intercept'] = 1
    h['intercept'] = 1
    v_result = sm.OLS(v['output'], v[['input']]).fit()
    h_result = sm.OLS(h['output'], h[['input']]).fit()
    if np.unique(round(v_result.predict(v[['input']])) != v['output'])[-1] or np.unique(round(h_result.predict(h[['input']])) != h['output'])[-1]:
        pass
    else:
        return (round(v_result.predict([test_input.shape[0]])[0]), round(h_result.predict([test_input.shape[1]])[0])), 'multiplied'
    
    v_result = sm.OLS(v['output'], v[['intercept', 'input']]).fit()
    h_result = sm.OLS(h['output'], h[['intercept', 'input']]).fit()
    if np.unique(round(v_result.predict(v[['intercept', 'input']])) != v['output'])[-1] or np.unique(round(h_result.predict(h[['intercept', 'input']])) != h['output'])[-1]:
        pass
    else:
        return (round(v_result.predict([1, test_input.shape[0]])[0]), round(h_result.predict([1, test_input.shape[1]])[0])), 'may have grid'
    
    if len(np.unique(v['output'])) == 1 and len(np.unique(h['output'])) == 1:
        return (np.unique(v['output']), np.unique(h['output']))
    return 0, 'failed'
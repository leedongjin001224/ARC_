import json
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import sklearn as sk
import statsmodels.api as sm
from sklearn.tree import DecisionTreeClassifier
from show_cur import show_cur
from component import find_component, find_components, component
from tasks import *
from size_predict import *
from error_rate import error_rate

def predict(trains, test_input):
    pred = None
    out_size, state = estimate_size(trains, test_input)
    if state == 'multiplied':
        in_ = [zoom_in(np.array(i['input']), np.array(i['output']).shape) for i in trains]
        out_ = [np.array(i['output']) for i in trains]
        l = 5
        just_one = False
        for i in in_:
            if len(i) != 5:
                just_one = True
        if just_one:
            sample_num = 1
        else:
            sample_num = 5
        error_rates = [0] * sample_num
        min_error = 1
        min_error_idx = 0
        for i in range(sample_num):
            cur_error = [error_rate(j[i], k) for j, k in zip(in_,out_)]
            error_rates[i] = sum(cur_error) / sample_num
            if min_error > error_rates[i]:
                min_error = error_rates[i]
                min_error_idx = i
        if min_error == 0:
            pred = zoom_in(np.array(test_input), out_size)[min_error_idx]
        else:
            likey = zoom_in(np.array(test_input), out_size)[min_error_idx]
    elif state == 'failed':
        in_components = [find_components(i['input'], diagonal=True, multi_color=True, reversed=False) for i in trains]
        out_mat = [np.array(i['output']) for i in trains]
        eq = True
        df = pd.DataFrame()
        for comps, output in zip(in_components, out_mat):#Each input-output pair
            df_ = pd.DataFrame()
            sub = False
            eq_ = False
            for comp in comps:#Each one component in one input
                feature = pd.DataFrame(comp.get_features())
                feature['is_this'] = False
                feature['repeated'] = 0
                if comp.shape == output.shape:
                    sub = True
                    feature['is_this'] = 'same_size'
                    if np.unique(comp.mat == output)[0]:
                        eq_ = True
                        feature['is_this'] = 'it_is'
                for other in comps:
                    if comp == other:
                        feature['repeated'] += 1
                df_ = pd.concat([df_, feature], axis=0, ignore_index=True)
            for i in range(10):
                df_['{} order'.format(i)] = 0
                if df_['{}'.format(i)].max() != 0:
                    df_['{} order'.format(i)] = df_['{}'.format(i)] / df_['{}'.format(i)].max()
            if not sub:
                break
            eq = eq and eq_
        df = pd.concat([df, df_], axis=0, ignore_index=True)
        if sub:
            df_ = pd.DataFrame()
            components = find_components(np.array(test_input), diagonal=True)
            for comp in components:
                feature = comp.get_features()
                feature['repeated'] = 0
                for other in comps:
                    if comp == other:
                        feature['repeated'] += 1
                df_ = pd.concat([df_, feature], axis=0, ignore_index=True)
            for i in range(10):
                df_['{} order'.format(i)] = 0
                if df_['{}'.format(i)].max() != 0:
                    df_['{} order'.format(i)] = df_['{}'.format(i)] / df_['{}'.format(i)].max()
            if eq:
                target = 'it_is'
            else:
                target = 'same_size'
            df['is_this'] = df['is_this'] == target
            for p in [['hsym', 'vsym'], ['{} order'.format(i) for i in range(10)]]:
                tree = DecisionTreeClassifier(random_state=0, max_depth=1).fit(df[p], df['is_this'])
                guess = tree.predict(df_[p])

                for i in range(len(components)):
                    if guess[i] == True:
                        pred = components[i].mat
            
            if pred is None:
                tree = DecisionTreeClassifier(random_state=0, max_depth=1).fit(df[df.columns.drop('is_this')], df['is_this'])
                guess = tree.predict(df_)

                for i in range(len(components)):
                    if guess[i] == True:
                        pred = components[i].mat
    
    return pred
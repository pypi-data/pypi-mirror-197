from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import time
from core import *

def sliding_windows(bmp, emp, lt_data, window_length=0.3, step=0.1, criterion='MAXMIN', fields = ['MP', 'FC_6']):
    windows = gen_windows(bmp, emp, window_length, step)
    windows = cal_statistics(windows, lt_data, fields)
    slices = gen_zones(bmp, emp, step)
    slices = cal_statsitics_slices(slices, windows, criterion)
    slices_merged = merge_by_identical(slices, criterion)

    # windows.to_csv(r'D:\repos\LT_D7W\data\report_example_windows.csv')
    # slices.to_csv(r'D:\repos\LT_D7W\data\report_example_slices.csv')
    # slices_merged.to_csv(r'D:\repos\LT_D7W\data\report_example_slices_merged.csv')

    return slices_merged

def sliding_windows_sequential_clustering(bmp, emp, lt_data, window_length=0.3, step=0.1, bins=None, labels=None, mini_length=None, 
                                          criterion='MAXMIN', fields = ['MP', 'FC_6'], max_iters = 5000, display = False, disp_prefix = ''):
    '''
        Function calculate ratio-based uniformity using sliding windows
        Paramters:
            lt_data:        standard ALMS lighting data
            window_lenth:   sliding window length in miles
            step:           sliding window moving step in miles
            bins:           bins for categorization, default is None (no categroziation will be executed)
            labels:         labels for categorization, default is None (if bins is given, default labels will be used)
            mini_length:    merge the short segment to neighbors, default is None (no merge will be executed)
            criterion:      MAXMIN = Max/Min; AVGMIN = average/min; P95MIN = P95/P5; AVGP5 = Average/P5
            display:        dispay iteration information
        Return:
            windows:        a dataframe contains the list of sliding windows    
            slices:         a dataframe contains the list of slices
            slices_merged:  a dataframe contains the list of slices with merged same uniformity
            slices_cat:     a dataframe contains the list of slices with categorized uniformity
            slices_mini:    a dataframe contains the list of slices with categorized uniformity and merged short segments
    '''
    
    slices = sliding_windows(bmp, emp, lt_data, window_length, step, criterion, fields)

    slices_cat = None
    slices_mini = None

    if bins is not None:
        slices_cat = merge_by_cat(slices, feature_name=criterion, bins=bins, labels=labels)

        if mini_length is not None:
            slices_mini = merge_short_sections(slices_cat, feature_name=criterion, mini_length=mini_length, average_method='LENGTH')
            slices_mini = slices_mini.drop(['MAXMIN_CAT','LENGTH'], axis=1)
            slices_mini = merge_by_cat(slices_mini, feature_name=criterion, bins=bins, labels=labels)
    
    return slices_cat, slices_mini

def sliding_windows_hierarchical_clustering(bmp, emp, lt_data, window_length=0.3, step=0.1, bins=None, labels=None, mini_length=None, 
                                            criterion='MAXMIN', fields = ['MP', 'FC_6'], max_iters = 5000, display = False, disp_prefix = ''):
    '''
        Function calculate ratio-based uniformity using sliding windows
        Paramters:
            lt_data:        standard ALMS lighting data
            window_lenth:   sliding window length in miles
            step:           sliding window moving step in miles
            bins:           bins for categorization, default is None (no categroziation will be executed)
            labels:         labels for categorization, default is None (if bins is given, default labels will be used)
            mini_length:    merge the short segment to neighbors, default is None (no merge will be executed)
            criterion:      MAXMIN = Max/Min; AVGMIN = average/min; P95MIN = P95/P5; AVGP5 = Average/P5
            display:        dispay iteration information
            disp_prefix:    prefix for display
        Return:
            windows:        a dataframe contains the list of sliding windows    
            slices:         a dataframe contains the list of slices
            slices_merged:  a dataframe contains the list of slices with merged same uniformity
            slices_cat:     a dataframe contains the list of slices with categorized uniformity
            slices_mini:    a dataframe contains the list of slices with categorized uniformity and merged short segments
    '''
    
    slices = sliding_windows(bmp, emp, lt_data, window_length, step, criterion, fields)

    slices_cat = slices.copy()
    slices_cat['LENGTH'] = slices_cat['EMP'] - slices_cat['BMP']
    slices_cat = cal_statistics(slices_cat, lt_data, fields)
    slices_cat['LABEL'] = pd.cut(slices_cat[criterion], bins=bins, labels=labels)
    slices_cat = cal_adjcent_zones_diff(slices_cat, criterion)
    slices_cat = cal_blocked(slices_cat, mini_length)

    # iteration
    iter = 0
    cnt_nochange = 0
    while ((not is_all_blocked(slices_cat)) & (iter<max_iters) & (cnt_nochange < len(slices_cat))):

        zone_num = len(slices_cat)
        blocked_num = len(slices_cat[slices_cat['BLOCKED']==False])

        merge_pair = find_merge_zones(slices_cat)
        if len(merge_pair)>0:   
            slices_cat = merge_zones(slices_cat, merge_pair, lt_data, fields, criterion, bins, labels, mini_length)

        iter+=1
        if (zone_num == len(slices_cat) and (blocked_num == len(slices_cat[slices_cat['BLOCKED']==False]))):
            cnt_nochange += 1

        if display:
            print(disp_prefix + " Iteration:{}; number of zones: {}; number of unblocked: {}               ".format(iter, len(slices_cat), len(slices_cat[slices_cat['BLOCKED']==False])), end='\r')

    # final check
    slices_cat = cal_statistics(slices_cat, lt_data, fields)
    slices_cat = slices_cat[~slices_cat['NUM'].isnull()]

    return slices_cat

def lt_uniformity_windows_stat(windows, bins = [0, 5, 10, 20, 40, 10000]):
    values = windows['UNIFORMITY'].to_numpy()
    max_val = max(values)
    mean_val = np.mean(values)

    tot = len(values)
    if tot>0:
        hist = np.histogram(values, bins=bins, density=False)
        hist_p = hist[0]/tot
    
    return max_val, mean_val, hist[0].tolist(), hist_p.tolist()

if __name__ == '__main__':
    pass
import pandas as pd
import numpy as np
from core import *

def hierarchical_clustering(bmp, emp, lt_points, bins, labels=None, init_length = 0.003, mini_length = 0.1, 
                            criterion = 'MEAN', fields = ['MP', 'FC_6'], max_iters = 5000, display = False, disp_prefix = ''):
    '''
    Function:   Cluster roadway segments based on the similarity of the given feature
                Stop literation if (1) all zone length >= mini_length; and (2) all neighboring sections have different labels
    Parameters:
        bmp: begaining mp
        emp: ending mp
        lt_points: a dataframe of lt points for the segment, including "RDWYID, BMP, EMP, FC_6"
        label_bins: the bins of labels for cutting off for the clustering criterion
        init_length: initial zone length in miles
        mini_length: the minimum zone length in outputs
        criterion: clustering measures MEAN, STD, MAXMIN, MEANMIN, P95P5, MEANP5 
        fields: clustering criterion, (1) MEAN, (2) STD, (3) max/min, (3) mean/min, 
    Output:
        a dataframe constains cluterted zones with lt statistics 
    '''

    # initialization
    zones = gen_zones(bmp, emp, init_length)            # split the whole segment into small zones with initial length
    zones['LENGTH'] = zones['EMP'] - zones['BMP']
    zones = cal_statistics(zones, lt_points, fields)
    zones['LABEL'] = pd.cut(zones[criterion], bins = bins, labels = labels)
    zones = cal_adjcent_zones_diff(zones, criterion)
    zones = cal_blocked(zones, mini_length)

    # iteration
    iter = 0
    cnt_nochange = 0
    while ((not is_all_blocked(zones)) & (iter<max_iters) & (cnt_nochange <= len(zones))):

        zone_num = len(zones)
        blocked_num = len(zones[zones['BLOCKED']==False])

        merge_pair = find_merge_zones(zones)
        if len(merge_pair)>0:   
            zones = merge_zones(zones, merge_pair, lt_points, fields, criterion, bins, labels, mini_length)

        iter += 1    
        if (zone_num == len(zones) and (blocked_num == len(zones[zones['BLOCKED']==False]))):
            cnt_nochange += 1

        if display:
            print(disp_prefix + " Iteration:{}; number of zones: {}; number of unblocked: {}             ".format(iter, len(zones), len(zones[zones['BLOCKED']==False])), end='\r')

    # final check
    zones = cal_statistics(zones, lt_points, fields)
    zones = zones[~zones['NUM'].isnull()]

    return zones

def sequential_clustering(bmp, emp, lt_points, bins, labels = None, init_length = 0.003, mini_length = 0.1, criterion = 'MEAN', fields = ['MP', 'FC_6'], max_iters = 5000, display = False):
     
    # initialization
    zones = gen_zones(bmp, emp, init_length)            
    zones = cal_statistics(zones, lt_points, fields)
    zones['CAT'] = pd.cut(zones[criterion], bins = bins, labels = labels)

    col_names = zones.columns.to_list() 

    # merge zones with the same category
    results = []
    iter = 0
    while len(zones)>0:
        zones = zones.reset_index(drop=True)

        emp_0 = zones.iloc[0]['EMP']
        selected = zones.loc[((zones['BMP']-emp_0)<0.001) & ((zones['BMP']-emp_0)>=0)]

        if len(selected)>0:
            selected_index = selected.index.tolist()[0]
            if (zones.iloc[0]['CAT'] == selected.iloc[0]['CAT']):
                zones.at[selected_index, 'BMP'] = zones.iloc[0]['BMP']
                zones.at[selected_index, criterion] = cal_weighted_average(zones.iloc[0], selected.iloc[0], criterion, method='COUNT')
            else:
                results.append(zones.iloc[0].to_list())
        else:
            results.append(zones.iloc[0].to_list())

        iter+=1    
        if display:
            print("Merging similar zones - iteration:{}; number of zones: {}                   ".format(iter, len(zones)), end='\r')

        zones.drop(index = zones.index[0], axis=0, inplace=True)
    
    zones = pd.DataFrame(results, columns=col_names)

    # merge short zones
    zones = merge_short_sections(zones, feature_name=criterion, mini_length=mini_length, average_method = 'COUNT', display=display)
    zones = cal_statistics(zones, lt_points, fields)
    zones['CAT'] = pd.cut(zones[criterion], bins = bins, labels = labels)

    return zones

if __name__=="__main__":
    pass


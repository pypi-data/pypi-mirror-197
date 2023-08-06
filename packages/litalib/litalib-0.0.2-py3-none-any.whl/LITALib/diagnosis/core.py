import pandas as pd
import numpy as np

def gen_zones(bmp, emp, length):
    '''
        Split the whole segment into non-overlapped zones by uniform length.
    '''
    slices = []

    temp_bmp = bmp
    temp_emp = temp_bmp + length
    while temp_emp < emp:
        slices.append([round(temp_bmp,3), round(temp_emp,3)])
        temp_bmp = temp_emp
        temp_emp = temp_bmp + length
    slices.append([round(temp_bmp,3), round(emp,3)])
        
    df = pd.DataFrame(slices, columns=['BMP', 'EMP'])
    return df

def gen_zones_by_distance(bmp, emp, lt_data, field_bmp = 'BMP', field_EMP = 'EMP', field_dist = 'DISTANCE'):
    '''
        Split the segment into non-overlapped zones by lighting data distance on a given lane
    '''
    lt = lt_data.loc[(lt_data['BMP']>=bmp) & (lt_data['BMP']>=emp)]
    lt.sort_values(by = [field_dist], inplace = True)

    df = lt[['BMP', 'EMP']]

    

def gen_windows(bmp, emp, window_length, step):
    '''
        Split the whole segment into overlapped windows by uniform length with a moving step.
    '''
    windows = []

    tempBMP = bmp
    tempEMP = tempBMP + window_length 
    while tempEMP < emp:
        windows.append([round(tempBMP,3), round(tempEMP,3)])
        tempBMP = tempBMP + step
        tempEMP = tempBMP + window_length

    tempBMP = max(bmp, emp-window_length)
    windows.append([round(tempBMP,3), round(emp,3)])

    df = pd.DataFrame(windows, columns=['BMP', 'EMP'])
    df['LENGTH'] = df['EMP'] - df['BMP']
    df.drop(df[df['LENGTH']==0].index, inplace=True)

    return df

def cal_statistics(windows, lt_data, fields, mini_fc = 0.0001):

    for index, window in windows.iterrows():
        lt = lt_data.loc[(lt_data[fields[0]]>=window['BMP']) & (lt_data[fields[0]]<=window['EMP'])][fields[1]].to_numpy()

        if len(lt) > 0:
            windows.at[index, 'NUM'] = len(lt)
            val_mean = np.mean(lt)
            val_std = np.std(lt)
            val_max =  np.amax(lt)
            val_min = max(np.amin(lt), 0.0001)
            val_p95 = np.percentile(lt, 95)
            val_p5 = max(np.percentile(lt, 5), 0.0001)

            windows.at[index, ['MEAN', 'STD', 'MAX', 'MIN', 'P95', 'P5', 'MAXMIN', 'MEANMIN', 'P95P5', 'MEANP5']] = [val_mean, val_std, val_max, val_min, val_p95, val_p5, 
                                                        val_max/val_min, val_mean/val_min, val_p95/val_p5, val_mean/val_p5]
    return windows

def is_all_blocked(zones):
    if len(zones.loc[zones['BLOCKED']==False]) > 0:
        return False
    else:
        return True

def cal_adjcent_zones_diff(org_zones, criterion):
    zones = org_zones.copy()
    zones['DIFF'] = None
    total = len(zones)
    for i in list(range(total-1)):
        zones['DIFF'].iat[i] = abs(zones[criterion].iloc[i] - zones[criterion].iloc[i+1])

    return zones

def cal_blocked(org_zones, mini_length):
    zones = org_zones
    zones['BLOCKED'] = False
    total = len(zones)

    if total<=1:
        zones['BLOCKED'] = True
    else:
        for i in list(range(total-1)):
            if (zones['LENGTH'].iloc[i] < mini_length) | (zones['LENGTH'].iloc[i+1] < mini_length):
                zones['BLOCKED'].iat[i] = False
            elif zones['LABEL'].iloc[i] == zones['LABEL'].iloc[i+1]:
                zones['BLOCKED'].iat[i] = False
            else:
                zones['BLOCKED'].iat[i] = True
    
    zones['BLOCKED'].iat[-1] = True

    return zones

def find_merge_zones(zones):
    result = []
    nonblocks = zones.loc[zones['BLOCKED']==False]
    min_diff = nonblocks['DIFF'].min()      
    min_pairs = zones.index[(zones['DIFF']==min_diff)].tolist()

    if len(min_pairs) > 0:   
        index_1 = min_pairs[0]
        index_2 = index_1 + 1
        result = [index_1, index_2]

    return result

def merge_zones(org_zones, pair, lt_points, fields, criterion, bins, labels, mini_length):
    zones = org_zones.copy()

    zones.at[pair[0], 'EMP'] = zones.loc[pair[1], 'EMP']
    zones.at[pair[0], 'LENGTH'] = zones.loc[pair[0], 'EMP'] - zones.loc[pair[0], 'BMP']

    index = pair[0]
    bmp = zones.loc[pair[0], 'BMP']
    emp = zones.loc[pair[0], 'EMP']

    lt = lt_points.loc[(lt_points[fields[0]]>=bmp) & (lt_points[fields[0]]<=emp)][fields[1]].to_numpy()

    # update statistics
    zones.at[index, 'NUM'] = len(lt)
    if len(lt) > 0:
        val_mean = np.mean(lt)
        val_std = np.std(lt)
        val_max =  np.amax(lt)
        val_min = max(np.amin(lt), 0.0001)
        val_p95 = np.percentile(lt, 95)
        val_p5 = max(np.percentile(lt, 5), 0.0001)

        zones.at[index, ['MEAN', 'STD', 'MAX', 'MIN', 'P95', 'P5', 'MAXMIN', 'MEANMIN', 'P95P5', 'MEANP5']] = [val_mean, val_std, val_max, val_min, val_p95, val_p5, 
                                                        val_max/val_min, val_mean/val_min, val_p95/val_p5, val_mean/val_p5]

    zones['LABEL'] = pd.cut(zones[criterion], bins = bins, labels = labels)

    # update difference and blocks
    zone_pre = zones.loc[zones['EMP']==bmp]
    zone_next = zones.loc[zones['BMP']==emp]
    
    if len(zone_pre) == 1:
        index_pre = zone_pre.index.values[0]
        zones.at[index_pre, 'DIFF'] = abs(zones[criterion].loc[index_pre] - zones[criterion].loc[index])

        if (zones.loc[index_pre, 'LENGTH']<mini_length) | (zones.loc[index, 'LENGTH']<mini_length):
            zones.at[index_pre, 'BLOCKED'] = False
        elif zones.loc[index_pre, 'LABEL'] == zones.loc[index, 'LABEL']:
            zones.at[index_pre, 'BLOCKED'] = False
        else:
            zones.at[index_pre, 'BLOCKED'] = True

    if len(zone_next) == 1:
        index_next = zone_next.index.values[0]
        zones.at[index, 'DIFF'] = abs(zones[criterion].loc[index] - zones[criterion].loc[index_next])

        if (zones.loc[index, 'LENGTH']<mini_length) | (zones.loc[index_next, 'LENGTH']<mini_length):
            zones.at[index, 'BLOCKED'] = False
        elif zones.loc[index, 'LABEL'] == zones.loc[index_next, 'LABEL']:
            zones.at[index, 'BLOCKED'] = False
        else:
            zones.at[index, 'BLOCKED'] = True

    if len(zones)<=1:
        zones['BLOCKED'] = True

    zones = zones.drop(pair[1])
    zones = zones.reset_index(drop=True)

    zones['BLOCKED'].iat[-1] = True

    return zones

def cal_weighted_average(section_1, section_2, feature_name, method='COUNT'):
    '''
        Calculate weighted average by numbers of lt points
        Parameters:
            section_1: segment 1
            section_2: segment 2
            feature_name: LT Feature name
            method: COUNT - by number of LT points; LENGTH - length of sections
    '''
    if method == 'COUNT':
        deno_1 = section_1['NUM']
        deno_2 = section_2['NUM']
    else:
        deno_1 = section_1['EMP'] - section_1['BMP']
        deno_2 = section_2['EMP'] - section_2['BMP']

    val_1 = section_1[feature_name]
    val_2 = section_2[feature_name]
    try:
        weighted_ave = (val_1*deno_1+val_2*deno_2)/(deno_1+deno_2)
    except ZeroDivisionError:
        weighted_ave = None
        
    return weighted_ave

def merge_short_sections(sections, feature_name, mini_length, average_method='COUNT', display=False):
        
    sections['LENGTH'] = sections['EMP'] - sections['BMP']
    selected = sections.loc[sections['LENGTH']<mini_length]

    iter = 0
    while len(selected)>0:
            
        bmp_0 = selected.iloc[0]['BMP']
        emp_0 = selected.iloc[0]['EMP']

        left_neighbor = sections.loc[((sections['EMP']-bmp_0)<0.001) & ((sections['EMP']-bmp_0)>=0)]
        right_neighbor = sections.loc[((sections['BMP']-emp_0)<0.001) & ((sections['BMP']-emp_0)>=0)]

        difference_l = None
        if len(left_neighbor)>0:
            difference_l = abs(left_neighbor.iloc[0][feature_name] - selected.iloc[0][feature_name])
        difference_r = None
        if len(right_neighbor)>0:
            difference_r = abs(right_neighbor.iloc[0][feature_name] - selected.iloc[0][feature_name])

        if (difference_l is not None) and (difference_r is not None):
            if difference_l<=difference_r:
                index_l = left_neighbor.index[0]
                sections.at[index_l, 'EMP'] = selected.iloc[0]['EMP']
                sections.at[index_l, feature_name] = cal_weighted_average(sections.loc[index_l], selected.iloc[0], feature_name, average_method)
                sections.drop(index = selected.index[0], axis=0, inplace=True)
            else:
                index_r = right_neighbor.index[0]
                sections.at[index_r, 'BMP'] = selected.iloc[0]['BMP']
                sections.at[index_r, feature_name] = cal_weighted_average(sections.loc[index_r], selected.iloc[0], feature_name, average_method)
                sections.drop(index = selected.index[0], axis=0, inplace=True)
        elif difference_l is not None:
            index_l = left_neighbor.index[0]
            sections.at[index_l, 'EMP'] = selected.iloc[0]['EMP']
            sections.at[index_l, feature_name] = cal_weighted_average(sections.loc[index_l], selected.iloc[0], feature_name, average_method)
            sections.drop(index = selected.index[0], axis=0, inplace=True)
        elif difference_r is not None:
            index_r = right_neighbor.index[0]
            sections.at[index_r, 'BMP'] = selected.iloc[0]['BMP']
            sections.at[index_r, feature_name] = cal_weighted_average(sections.loc[index_r], selected.iloc[0], feature_name, average_method)
            sections.drop(index = selected.index[0], axis=0, inplace=True)
            
        sections = sections.reset_index(drop=True)
        selected = sections.loc[sections['LENGTH']<mini_length]

        iter+=1    
        if display:
            print("Merging short zones - iteration:{}; number of zones: {}             ".format(iter, len(sections)), end='\r')
    
    sections['LENGTH'] = sections['EMP'] - sections['BMP']
    return sections

'''
    Functions for sliding windows --------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
def cal_statsitics_slices(slices, windows, criterion, method = 'MAX'):
    '''
        method: the method for worst case; MAX - default, MIN, 
    '''
    
    for index, slice in slices.iterrows():
        bmp = slice['BMP']
        emp = slice['EMP']

        selected = windows.loc[(windows['BMP']<=bmp) & (windows['EMP']>=emp)]
        value = None
        if len(selected>0):
            if method == 'MIN':
                value = selected[criterion].min()    # the worst case (min uniformity value)
            else:
                value = selected[criterion].max()    # the worst case (max uniformity value)

        slices.at[index, criterion] = value

    return slices

def merge_by_identical(slices, feature_name):

    sections = slices.copy()
    results = []

    while len(sections)>0:
        sections = sections.reset_index(drop=True)

        emp_0 = sections.iloc[0]['EMP']
        selected = sections.loc[((sections['BMP']-emp_0)<0.001) & ((sections['BMP']-emp_0)>=0)]

        if len(selected)>0:
            selected_index = selected.index.tolist()[0]
            identical = (sections.iloc[0][feature_name] == selected.iloc[0][feature_name])

            if identical:
                sections.at[selected_index, 'BMP'] = sections.iloc[0]['BMP']
            else:
                results.append(sections.iloc[0].to_list())
        else:
            results.append(sections.iloc[0].to_list())

        sections.drop(index = sections.index[0], axis=0, inplace=True)
    
    return pd.DataFrame(results, columns=slices.columns)
    
def merge_by_cat(slices, feature_name, bins, labels=None):

    sections = slices.copy()
    sections['CAT'] = pd.cut(sections[feature_name], bins = bins, labels = labels)
        
    results = []
    while len(sections)>0:
        sections = sections.reset_index(drop=True)

        emp_0 = sections.iloc[0]['EMP']
        selected = sections.loc[((sections['BMP']-emp_0)<0.001) & ((sections['BMP']-emp_0)>=0)]

        if len(selected)>0:
            selected_index = selected.index.tolist()[0]

            if sections.iloc[0]['CAT'] == selected.iloc[0]['CAT']:
                sections.at[selected_index, 'BMP'] = sections.iloc[0]['BMP']
                sections.at[selected_index, feature_name] = cal_weighted_average(sections.iloc[0], selected.iloc[0], feature_name, method='LENGTH')
            else:
                results.append(sections.iloc[0].to_list())
        else:
            results.append(sections.iloc[0].to_list())

        sections.drop(index = sections.index[0], axis=0, inplace=True)
        
    return pd.DataFrame(results, columns=['BMP', 'EMP', feature_name, feature_name+'_CAT'])

'''
    Functions for combine zones -----------------------------------------------------------------------------------------------------------------------------
'''

def get_mps(zones, fields_mp = ['BMP', 'EMP']):
    mps = []
    for index, zone in zones.iterrows():
        mps.append(round(zone[fields_mp[0]], 3))
        mps.append(round(zone[fields_mp[1]], 3))
    mps = list(dict.fromkeys(mps))                  # remove duplicated mps
    mps.sort()

    return mps

def combine_zones(zones, fields_mp = ['BMP', 'EMP']):
    mps = get_mps(zones, fields_mp)
    
    mps_length = len(mps)      
    for i in range(mps_length-1):
        bmp = mps[i]
        emp = mps[i+1]
        
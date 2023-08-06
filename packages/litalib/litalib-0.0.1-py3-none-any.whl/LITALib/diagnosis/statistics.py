import pandas as pd
import numpy as np

def point_statistics(lt_data, field, mini_fc = 0.0001):

    if len(lt_data) > 0:
        
        lt = lt_data[field].to_numpy()

        num = len(lt)
        val_mean = np.mean(lt)
        val_std = np.std(lt)
        val_max =  np.amax(lt)
        val_min = max(np.amin(lt), 0.0001)
        val_p95 = np.percentile(lt, 95)
        val_p5 = max(np.percentile(lt, 5), 0.0001)

        return [num, val_mean, val_std, val_max, val_min, val_p95, val_p5, val_max/val_min, val_mean/val_min, val_p95/val_p5, val_mean/val_p5]

def histogram(lt_data, field, bins = None, method = 'frequency'):
    '''
        method: frequency, density, percent
    '''
    values =lt_data[field].to_numpy()

    result = None
    tot = len(values)
    if tot>0:        
        if method == 'frequency':
            hist = np.histogram(values, bins=bins, density=False)
            result = hist[0].tolist()
        elif method == 'percent':
            hist = np.histogram(values, bins=bins, density=False)
            hist_p = hist[0] / tot
            result = hist_p.tolist()
        elif method == 'density':
            hist = np.histogram(values, bins=bins, density=True)
            result = hist[0].tolist()
    
    return result

def weighted_average(data, fields_mps = ['BMP', 'EMP'], criterion = 'MAXMIN'):
    lt = data.copy()
    lt['LENGTH'] = abs(data[fields_mps[1]] - data[fields_mps[0]])
    tot_length = abs(lt['EMP'].max() - lt['BMP'].min())

    if tot_length > 0:
        lt['PRODUCT'] = lt[criterion]*lt['LENGTH']/tot_length
        return lt['PRODUCT'].sum()
    else:
        return None

def zone_percentage(sections, field_length = 'LENGTH', field_label = 'LABEL'):
    return sections.groupby(field_label).agg('sum')
    
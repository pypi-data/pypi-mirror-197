import pandas as pd
from .clustering import hierarchical_clustering, sequential_clustering
from .sliding import sliding_windows_hierarchical_clustering, sliding_windows
from ..data.lt import LT

class Diagnosis:
    def __init__(self, lt_points, bmp = None, emp = None, mp_name = 'MP', fc_name = 'FC_6', by = 'both'):
        '''
        lt_points       - the lighting data
        bmp             - the specified BMP; None - the minimum BMP in lighting data
        emp             - the specified EMP; None - the maximum EMP in lighting data
        mp_name         - the field name for milepost in the lighting data
        fc_name         - the field name for footcandle in the lighting data
        by              - 'both': clustering based on both directions; 'side': clustering by direction; 'lane': clustering by lane; default is 'both'
        '''
        self.lt_points = lt_points
        if bmp is None:
            self.bmp = self.lt_points[mp_name].min()
        else:
            self.bmp = bmp
        if emp is None:
            self.emp = self.lt_points[mp_name].max()
        else:
            self.emp = emp

        self.mp_name = mp_name
        self.fc_name = fc_name
        self.by = by

    def lighting_level(self, bins = [0, 0.2, 1, 1.5, 10], labels = None, init_length = 0.01, mini_length = 0.1, max_iters = 5000, display = False):
        '''
        Inputs:
            label_bins      - a list of cut-off points to split lighting level, default is [0, 0.2, 1, 1.5, 10]
            init_length     - the initial zone length, default is 0.01 miles
            mini_length     - the minimum zone length in the final set, default is 0.1 miles
            max_iters       - the maximum iterations in clustering, default is 5000
            display         - output processing information during iterations, default is False
            disp_prefix     - prefix information for display
        Output:
            a dataframe contains the segments clustered by the similarity of HFC mean
        '''

        if self.by == 'side':

            lt_points_left = LT.select_ltpoints_by_side(self.lt_points, roadside='L')
            results_left = hierarchical_clustering(self.bmp, self.emp, lt_points_left, bins=bins, labels=labels,
                                        init_length = init_length, mini_length = mini_length, 
                                        fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display, disp_prefix='Left')
            results_left['SIDE'] = 'L'

            lt_points_right = LT.select_ltpoints_by_side(self.lt_points, roadside='R')
            results_right = hierarchical_clustering(self.bmp, self.emp, lt_points_right, bins=bins, labels=labels,
                                        init_length = init_length, mini_length = mini_length, 
                                        fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display, disp_prefix='Right')
            results_right['SIDE'] = 'R'

            results = pd.concat([results_left, results_right])

        elif self.by == 'lane':
            
            lanes = self.lt_points['LANE_ID'].unique()
            results_list = []
            for lane in lanes:
                lt = self.lt_points[self.lt_points['LANE_ID']==lane]
                r = hierarchical_clustering(self.bmp, self.emp, lt, bins=bins, labels=labels,
                                        init_length = init_length, mini_length = mini_length, 
                                        fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display, disp_prefix='Lane-'+str(lane))
                r['LANE_ID'] = lane 

                results_list.append(r)

            results = pd.concat(results_list)

        else:
            results = hierarchical_clustering(self.bmp, self.emp, self.lt_points, bins=bins, labels=labels,
                                        init_length = init_length, mini_length = mini_length, 
                                        fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display)    
        return results

    def uniformity(self, method='MAXMIN', window_length=0.114, step=0.019, bins=None, labels=None, mini_length=0.1, max_iters = 5000, display = True):
        
        '''
        Inputs:
            method          - the uniformity measure, 'MAXMIN', 'MEANMIN', 'P95P5', 'MEANP5', 'STD'; default is 'MAXMIN'
            windows_length  - the length of sliding window, default is 0.114 miles (600 ft)
            step            - moving step length 
            bins            - a list of cut-off points to split uniformity, default is None (auto)
            labels          - a list of labels, defualt is None (auto)
            mini_length     - the minimum zone length in the final set, default is 0.1 miles
            max_iters       - the maximum iterations in clustering, default is 5000
            display         - output processing information during iterations, default is False
        Output:
            a dataframe contains the segments clustered by the similarity of uniformity
        '''

        if bins is None:
            if (method == 'MAXMIN' or method == 'P95P5'):
                bins = [0, 10, 100000]
                if labels is None:
                    labels = ['<=10', '>10']

            elif (method == 'MEANMIN' or method == 'MEANP5'):
                bins = [0, 4, 100000]
                if labels is None:
                    labels = ['<=4', '>4']

            elif (method == 'STD'):
                bins = [0, 0.5, 1, 10]
                if labels is None:
                    labels = ['<=0.5', '(0.5, 1])', '>1']

        if (self.by == 'side'):
            
            lt_points_left = LT.select_ltpoints_by_side(self.lt_points, roadside='L')
            results_left = sliding_windows_hierarchical_clustering(self.bmp, self.emp, lt_points_left, window_length=window_length, step = step,
                                                            bins = bins, labels = labels, mini_length = mini_length, criterion = method,
                                                            fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display, disp_prefix='Left')
            results_left['SIDE'] = 'L'

            lt_points_right = LT.select_ltpoints_by_side(self.lt_points, roadside='R')
            results_right = sliding_windows_hierarchical_clustering(self.bmp, self.emp, lt_points_right, window_length=window_length, step = step,
                                                            bins = bins, labels = labels, mini_length = mini_length, criterion = method,
                                                            fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display, disp_prefix='Right')
            results_right['SIDE'] = 'R'

            results = pd.concat([results_left, results_right])

        elif (self.by == 'lane'):

            lanes = self.lt_points['LANE_ID'].unique()
            results_list = []
            for lane in lanes:
                lt = self.lt_points[self.lt_points['LANE_ID']==lane]
                r = sliding_windows_hierarchical_clustering(self.bmp, self.emp, lt, window_length=window_length, step = step,
                                                            bins = bins, labels = labels, mini_length = mini_length, criterion = method,
                                                            fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display,
                                                            disp_prefix='Lane-'+str(lane))
                r['LANE_ID'] = lane 
                results_list.append(r)

            results = pd.concat(results_list)

        else:
            results = sliding_windows_hierarchical_clustering(self.bmp, self.emp, self.lt_points, window_length=window_length, step = step,
                                                            bins = bins, labels = labels, mini_length = mini_length, criterion = method,
                                                            fields=[self.mp_name, self.fc_name], max_iters=max_iters, display=display)
        return results
    
    def percent(sections, criterions, field_length = 'LENGTH', field_label = 'LABEL'):
        results = pd.DataFrame()
        if (len(sections) == len(criterions)):
            for i in range(len(sections)):
                r = sections[i].groupby(field_label).agg({field_length:'sum'})
                r['NAME'] = r.index
                for index, row in r.iterrows():
                    results[criterions[i]+'_'+row['NAME']] = row[field_length]
    
    if __name__=="__main__":
        pass
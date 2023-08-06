import pandas as pd
from ..data.rci import RCI
from .aggregation import Aggregation

class Segmentation:
    def __init__(self):
        self.aggregator = Aggregation()
    
    def split_segment_by_points(self, rid, bmp, emp, point_features):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            year - point feature year
        return:
            a pandas dataframe contains segmented segments: RDWYID, BMP, EMP, YEAR
        '''
        mps = self.aggregator.get_mps(bmp, emp, point_features)

        results = []
        mps_length = len(mps)
        for i in range(mps_length-1):
            results.append([rid, mps[i], mps[i+1]])
        return pd.DataFrame(results, columns=['RDWYID', 'BMP', 'EMP'])

    def split_by_features(self, rid, bmp, emp, list_features):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            list_features - list of centralized rci characteristic
        return:
            a pandas dataframe contains sub-sections: RDWYID, BMP, EMP, CALYEAR, RDWYCHAR, VALUE
        '''
        
        # 1 - split segment by mps
        mps = []
        for feature in list_features:
            mps.extend(self.aggregator.get_mps(bmp, emp, feature))
        mps = list(dict.fromkeys(mps))                  # remove duplicated mps
        mps.sort()

        results = []
        mps_length = len(mps)
        for i in range(mps_length-1):
            for feature in list_features:

                value = self.aggregator.get_value(mps[i], mps[i+1], feature, None)
                feature_name = feature.iloc[0]['RDWYCHAR']
                year = feature.iloc[0]['CALYEAR']
                results.append([rid, mps[i], mps[i+1], year, feature_name, value])

        return pd.DataFrame(results, columns=['RDWYID', 'BMP', 'EMP', 'CALYEAR', 'RDWYCHAR', 'VALUE'])

    def split_segments_by_features(self, segments, features):
        results = []
        for index, segment in segments.iterrows():
            rid = segment['RDWYID']
            bmp = segment['BMP']
            emp = segment['EMP']

            results.append(self.split_by_features(rid, bmp, emp, features))

        return self.export_table(pd.concat(results))

    def split_by_feature(self, rid, bmp, emp, feature):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            feature - centralized rci characteristic
        return:
            a pandas dataframe contains sub-sections: RDWYID, BMP, EMP, CALYEAR, RDWYCHAR, VALUE
        '''
        list_features = [feature]
        return self.split_by_features(rid, bmp, emp, list_features)
    
    def split_by_feature_on_segments(self, rid, bmp, emp, feature, seg, colnames, name):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            feature - centralized rci characteristic
            seg - orginal segment
            name - name for the new feature
        return:
            a pandas dataframe contains sub-sections
        '''

        results = []
        if len(feature)>0:
            sub_segs = self.split_by_feature(rid, bmp , emp, feature)
        
            for index2, sub_seg in sub_segs.iterrows():
                result = [sub_seg['RDWYID'], sub_seg['BMP'], sub_seg['EMP']]
                for colname in colnames:
                    result.append(seg[colname])
                result.append(sub_seg['VALUE'])
                results.append(result)
        else:
            result = [rid, bmp, emp]
            for colname in colnames:
                result.append(seg[colname])
            result.append(None)
            results.append(result)

        names = ['RDWYID', 'BMP', 'EMP']
        names.extend(colnames)
        names.append(name)

        return pd.DataFrame(results, columns=names)

    def split_by_addtional_feature(self, segments, feature):
        '''
        parameters:
            segments - segments with homogenous features 
            feature - centralized addtional feature
        return:
            segments with new homogneous feature
        '''
        bmp = segments['BMP'].min()
        emp = segments['EMP'].max()
        rid = segments.iloc[0]['RDWYID']
        year = segments.iloc[0]['CALYEAR']

        mps = self.aggregator.get_mps(bmp, emp, feature)
        for index, segment in segments.iterrows():
            mps.append(segment['BMP'])
            mps.append(segment['EMP'])
        mps = list(dict.fromkeys(mps))                  # remove duplicated mps
        mps.sort()

        results = []        
        mps_length = len(mps)
        for i in range(mps_length-1):  
            selected_segments = segments.loc[(segments['BMP']<=mps[i]) & (segments['EMP']>=mps[i+1])].reset_index()
            if len(selected_segments) > 0:
                feature_name = selected_segments.iloc[0]['RDWYCHAR']
                value = selected_segments.iloc[0]['VALUE']
                results.append([rid, mps[i], mps[i+1], year, feature_name, value])

            value = self.aggregator.get_value(mps[i], mps[i+1], feature, None)
            feature_name = feature.iloc[0]['RDWYCHAR']
            year = feature.iloc[0]['CALYEAR']
            results.append([rid, mps[i], mps[i+1], year, feature_name, value])
            
        return pd.DataFrame(results, columns=['RDWYID', 'BMP', 'EMP', 'CALYEAR', 'RDWYCHAR', 'VALUE'])

    def export_table(self, segments, merge = False):
        '''
        parameters:
            segments - segments with homogenous features
        return:
            a dataframe contains segments with row-based homogenous features
        '''
        mps = list(zip(segments['BMP'].unique(), segments['EMP'].unique()))
        feature_names = segments['RDWYCHAR'].unique()
        column_names = ['RDWYID', 'BMP', 'EMP', 'YEAR']
        column_names.extend(feature_names)
        
        converted_list = []       
        for mp in mps:
            row = [segments.iloc[0]['RDWYID'], round(mp[0], 3), round(mp[1],3), segments.iloc[0]['CALYEAR']]
            for feature_name in feature_names:
                selected_segments = segments.loc[(segments['BMP']==mp[0]) & (segments['RDWYCHAR']==feature_name)].reset_index()
                if selected_segments.iloc[0]['VALUE'] is not None:
                    row.extend([selected_segments.iloc[0]['VALUE']])
                else:
                    row.extend(None)

            converted_list.append(row)
        converted_segments = pd.DataFrame(converted_list, columns=column_names)

        results = []
        # merge duplicated segments ........
        if merge == True:
            while len(converted_segments)>0:
                converted_segments = converted_segments.reset_index(drop=True)

                emp_0 = converted_segments.iloc[0]['EMP']
                selected = converted_segments.loc[((converted_segments['BMP']-emp_0)<0.001) & ((converted_segments['BMP']-emp_0)>=0)]

                if len(selected)>0:
                    selected_index = selected.index.tolist()[0]

                    identical = True
                    for feature_name in feature_names:

                        identical = identical & (converted_segments.iloc[0][feature_name] == selected.iloc[0][feature_name])

                    if identical == True:
                        converted_segments.at[selected_index, 'BMP'] = converted_segments.iloc[0]['BMP']
                    else:
                        results.append(converted_segments.iloc[0].to_list())
                else:
                    results.append(converted_segments.iloc[0].to_list())

                converted_segments.drop(index = converted_segments.index[0], axis=0, inplace=True)

            return pd.DataFrame(results, columns=column_names)

        else:
            return converted_segments

    def feature_percentage(self, rid, bmp, emp, feature):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            feature_name - rci characteristic name
        return:
            a pandas dataframe contains segments with feature percentage: RDWYID, BMP, EMP, YEAR, VALUE, PERCENT
        '''
        segments = self.split_by_feature(rid, bmp, emp, feature)
        
        seg_length = emp - bmp
        segments['PERCENT'] = (segments['EMP'] - segments['BMP'])/seg_length

        return segments

    def feature_weighted_average(self, rid, bmp, emp, feature):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            feature_name - rci characteristic name
        return:
            weighted average feature
        '''
        weighted_average = None
        if len(feature)>0:
            segments = self.feature_percentage(rid, bmp, emp, feature)
            segments['PRODUCT'] = segments['VALUE'].astype(float) * segments['PERCENT']
            weighted_average = segments['PRODUCT'].sum()
            
            #results = pd.DataFrame(columns=['RDWYID', 'BMP', 'EMP', 'YEAR', 'VALUE'])
            #results.loc[0] = [rid, bmp, emp, year, weighted_average]
        
        return weighted_average
    
    def feature_weighted_average_for_segments(self, segments, feature, colname = ''):
        
        if not colname:
            colname = 'WGT_'+feature.iloc[0]['RDWYCHAR']

        for index, segment in segments.iterrows():
            rid = segment['RDWYID']
            bmp = segment['BMP']
            emp = segment['EMP']

            segments.at[index, colname] = self.feature_weighted_average(rid, bmp, emp, feature)

        return segments

    def feature_percentage_list_by_values(self, rid, bmp, emp, feature, values):
        '''
        parameters:
            rid - roadway id of segment, 8-digit string
            bmp - beginning milepost
            emp - ending milepost
            feature - rci characteristic name
        return:
            weighted average feature
        '''
        results = []
        fields = []

        if len(feature)>0:
            segments = self.feature_percentage(rid, bmp, emp, feature)
            prefix = feature.iloc[0]['RDWYCHAR']

            for val in values:
                fields.append(prefix+'_'+str(val))
                selected = segments.loc[segments['VALUE']==val]
                if len(selected)>0:
                    results.append(selected['PERCENT'].sum())
                else:
                    results.append(0)

        return pd.DataFrame([results], columns=fields)
    
    def get_dataframe_row(series):
        rows = []
        names = []
        for index, value in series.items():
            names.append(index)
            rows.append(value)
        results = pd.DataFrame(rows).T
        results.columns = names
        
        return results

if __name__ == '__main__':
    pass

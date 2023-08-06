from itertools import count
import pandas as pd

class Collection:
    def __init__(self) -> None:
        pass

    def match_point_feature(self, rid, bmp, emp, point_features, include = 'both'):
        '''
        paramters:
            rid - roadway id
            bmp - begining milepost
            emp - ending milepost
            point_features - point features at [RDWYID, MP, CALYEAR, ...]
            bound - include bound: both - both sides, left - left side, right - right side, none - not include
        return:
            a dataframe contains point_features winthin the segment
        '''
        rid = str(rid).zfill(8)
        
        if include == 'both':
            results = point_features.loc[(point_features['RDWYID']==rid) & (point_features['MP']>=bmp) & (point_features['MP']<=emp)].reset_index(drop=True)
        elif include == 'left':
            results = point_features.loc[(point_features['RDWYID']==rid) & (point_features['MP']>=bmp) & (point_features['MP']<emp)].reset_index(drop=True)
        elif include == 'right':
            results = point_features.loc[(point_features['RDWYID']==rid) & (point_features['MP']>bmp) & (point_features['MP']<=emp)].reset_index(drop=True)
        else:
            results = point_features.loc[(point_features['RDWYID']==rid) & (point_features['MP']>bmp) & (point_features['MP']<emp)].reset_index(drop=True)

        return results

    def count_matched_point_feature(self, rid, bmp, emp, point_features, include = 'both'):
        '''
        paramters:
            rid - roadway id
            bmp - begining milepost
            emp - ending milepost
            point_features - point features at [RDWYID, MP, CALYEAR, ...]
        return:
            the count of matched point_features winthin the segment
        '''
        return len(self.match_point_feature(rid, bmp, emp, point_features, include))

    def count_matched_point_feature_for_segments(self, segments, point_features, feature_name, include = 'both'):
        '''
        paramters:
            segments - a dataframe of segments 
            point_features - point features at [RDWYID, MP, CALYEAR, ...]
        return:
            a dataframe of segments with the count of matched point_features
        '''
        for index, segment in segments.iterrows():
            segments.at[index, feature_name] = self.count_matched_point_feature(segment['RDWYID'], segment['BMP'], segment['EMP'], point_features, include)

        return segments

if __name__=='__main__':
    pass

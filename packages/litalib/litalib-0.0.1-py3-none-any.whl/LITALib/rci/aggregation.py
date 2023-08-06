import pandas as pd

class Aggregation:
    def __init__(self) -> None:
        pass
    
    def get_value(self, bmp, emp, features, default=None):
        selected_features = features.loc[(round(features['BMP'], 3)<=bmp) & (round(features['EMP'], 3)>=emp)].reset_index()
        results = default

        if len(selected_features) > 0:
            results = selected_features.iloc[0]['VALUE']

        return results

    def get_value_zero(self, bmp, emp, features):
        selected_features = features.loc[(round(features['BMP'], 3)<=bmp) & (round(features['EMP'], 3)>=emp)].reset_index()
        results = 0

        if len(selected_features) > 0:
            results = selected_features.iloc[0]['VALUE']

        return results

    @staticmethod
    def get_mps(bmp, emp, features):
        mps = [round(bmp, 3), round(emp, 3)]
        for index, feature in features.iterrows():
            if (round(feature['BMP'], 3) > bmp) & (round(feature['BMP'], 3) < emp):
                mps.append(round(feature['BMP'], 3))
            if (round(feature['EMP'], 3) > bmp) & (round(feature['EMP'], 3) < emp):
                mps.append(round(feature['EMP'], 3))
        mps = list(dict.fromkeys(mps))                  # remove duplicated mps
        mps.sort()
        
        return mps
    
    def centralize(self, feature, method = 'sum', none_value = 0):
        '''
        functions:
            - Combine left, right, and central numeric values as one value (central) using spefici method
            - Cut the summated values into categories by bins
            - Combine adjcent features with the same category
        paramters:
            feature - the rci feature for cut off
            method - sum (default): summate L/R/C values, average: average L/R/C values, max - max L/R values (if L<>R), min - L/R values (if L<>R)
        return:
            a dataframe with categozied values
        '''
        list_features = [] 
        if len(feature)>0:
            rid = feature.iloc[0]['RDWYID']
            year = feature.iloc[0]['CALYEAR']
            feature_name = feature.iloc[0]['RDWYCHAR']
            bmp = feature['BMP'].min()
            emp = feature['EMP'].max()
            mps = self.get_mps(bmp, emp, feature)

            feature_left = feature.loc[feature['RDWYSIDE']=='L']
            feature_right = feature.loc[feature['RDWYSIDE']=='R']
            feature_center = feature.loc[feature['RDWYSIDE']=='C']

            mps_length = len(mps)      
            for i in range(mps_length-1):

                if method == 'sum':
                    value_left = self.get_value(mps[i], mps[i+1], feature_left, default=none_value)
                    value_right = self.get_value(mps[i], mps[i+1], feature_right, default=none_value)
                    value_center = self.get_value(mps[i], mps[i+1], feature_center, default=none_value)
                    sum = float(value_left) + float(value_right) + float(value_center)
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, sum])

                elif method == 'average':
                    values = []
                    values.append(self.get_value(mps[i], mps[i+1], feature_left, none_value))
                    values.append(self.get_value(mps[i], mps[i+1], feature_right, none_value))
                    values.append(self.get_value(mps[i], mps[i+1], feature_center, none_value))
                    sum = 0
                    n = 0
                    for val in values:
                        if val is not None:
                            sum = sum + float(val)
                            n = n + 1
                    if n > 0:
                        ave = sum / n
                    else:
                        ave = None
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, ave])

                elif method == 'max':
                    value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                    value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                    value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)
                    if value_center != none_value:
                        list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, float(value_center)])
                    else:
                        list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, max(float(value_left), float(value_right))])
                elif method == 'min':
                    value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                    value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                    value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)
                    if value_center != none_value:
                        list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, float(value_center)])
                    else:
                        list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, min(float(value_left), float(value_right))])
                else:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, none_value])

        return pd.DataFrame(list_features, columns=['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE'])

    def centralize_and_recode_num(self, feature, bins, labels, method = 'sum', none_value = 0):
        '''
        functions:
            - Combine left, right, and central numeric values as one value (central) using spefici method
            - Cut the summated values into categories by bins
            - Combine adjcent features with the same category
        paramters:
            feature - the rci feature for cut off
            bins - a list of cut off points [min, ..., max]
            labels - a list of labels for category
            method - sum (default): summate L/R/C values, average: average L/R/C values, max - max L/R values (if L<>R), min - L/R values (if L<>R)
        return:
            a dataframe with categozied values
        '''
        rid = feature.iloc[0]['RDWYID']
        year = feature.iloc[0]['CALYEAR']
        feature_name = feature.iloc[0]['RDWYCHAR']
        bmp = feature['BMP'].min()
        emp = feature['EMP'].max()
        mps = self.get_mps(bmp, emp, feature)

        feature_left = feature.loc[feature['RDWYSIDE']=='L']
        feature_right = feature.loc[feature['RDWYSIDE']=='R']
        feature_center = feature.loc[feature['RDWYSIDE']=='C']

        mps_length = len(mps)
        list_features = []        
        for i in range(mps_length-1):

            if method == 'sum':
                value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)

                sum = float(value_left) + float(value_right) + float(value_center)
                list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, sum])

            elif method == 'average':
                values = []
                values.append(self.get_value(mps[i], mps[i+1], feature_left, none_value))
                values.append(self.get_value(mps[i], mps[i+1], feature_left, none_value))
                values.append(self.get_value(mps[i], mps[i+1], feature_left, none_value))
                sum = 0
                n = 0
                for val in values:
                    if val is not None:
                        sum = sum + float(val)
                        n = n + 1
                if n > 0:
                    ave = sum / n
                else:
                    ave = None
                list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, ave])
            elif method == 'max':
                value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)
                if value_center != none_value:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, float(value_center)])
                else:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, max(float(value_left), float(value_right))])
            elif method == 'min':
                value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)
                if value_center != none_value:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, float(value_center)])
                else:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, min(float(value_left), float(value_right))])
            else:
                list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, none_value])
        
        aggregate_features = pd.DataFrame(list_features, columns=['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','TEMP_VAL'])
        aggregate_features['VALUE'] = pd.cut(aggregate_features['TEMP_VAL'], bins = bins, labels = labels)
        aggregate_features.drop(columns=['TEMP_VAL'], inplace=True)

        results = []
        while len(aggregate_features)>0:
            aggregate_features = aggregate_features.reset_index(drop=True)
            emp_0 = aggregate_features.iloc[0]['EMP']
            value_0 = aggregate_features.iloc[0]['VALUE']
            selected = aggregate_features.loc[((aggregate_features['BMP']-emp_0)<0.001) & ((aggregate_features['BMP']-emp_0)>=0) & (aggregate_features['VALUE']==value_0)]
            if len(selected)>0:
                selected_index = selected.index.tolist()[0]
                aggregate_features.at[selected_index, 'BMP'] = aggregate_features.iloc[0]['BMP']
            else:
                results.append(aggregate_features.iloc[0].to_list())
            aggregate_features.drop(index = aggregate_features.index[0], axis=0, inplace=True)

        return pd.DataFrame(results, columns=['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE'])

    def centralize_and_recode_cat(self, feature, org_codes, re_codes, method = 'join', none_value = None):
        '''
        functions:
            - Combine left, right, and central categorical values as one value (central) using spefici method
            - Cut the summated values into categories by bins
            - Combine adjcent features with the same category
        paramters:
            feature - the rci feature for cut off
            bins - a list of category values
            labels - a list of labels for categories
            method - left: left values if L<>R, right: right value if L<>R, join (default) - L_R value (if L<>R), 
        return:
            a dataframe with categozied values
        '''
        results = []
        if len(feature)>0:
            rid = feature.iloc[0]['RDWYID']
            year = feature.iloc[0]['CALYEAR']
            feature_name = feature.iloc[0]['RDWYCHAR']
            bmp = feature['BMP'].min()
            emp = feature['EMP'].max()
            mps = self.get_mps(bmp, emp, feature)

            feature_left = feature.loc[feature['RDWYSIDE']=='L']
            feature_right = feature.loc[feature['RDWYSIDE']=='R']
            feature_center = feature.loc[feature['RDWYSIDE']=='C']

            feature_left['VALUE'] = feature_left['VALUE'].apply(lambda x: re_codes[org_codes.index(x)])
            feature_right['VALUE'] = feature_right['VALUE'].apply(lambda x: re_codes[org_codes.index(x)])
            feature_center['VALUE'] = feature_center['VALUE'].apply(lambda x: re_codes[org_codes.index(x)])

            mps_length = len(mps)
            list_features = []        
            for i in range(mps_length-1):
                value_left = self.get_value(mps[i], mps[i+1], feature_left, none_value)
                value_right = self.get_value(mps[i], mps[i+1], feature_right, none_value)
                value_center = self.get_value(mps[i], mps[i+1], feature_center, none_value)

                if value_center != none_value:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, value_center])
                elif value_left == value_right:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, value_left])
                elif (method == 'left') & (value_left != none_value):
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, value_left])
                elif (method == 'right') & (value_left != none_value):
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, value_right])
                elif (method == 'join'):
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, value_left+'_'+value_right])
                else:
                    list_features.append([rid, mps[i], mps[i+1], 'C', year, feature_name, none_value])
                            
            aggregate_features = pd.DataFrame(list_features, columns=['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE'])
            
            while len(aggregate_features)>0:
                aggregate_features = aggregate_features.reset_index(drop=True)
                emp_0 = aggregate_features.iloc[0]['EMP']
                value_0 = aggregate_features.iloc[0]['VALUE']
                selected = aggregate_features.loc[((aggregate_features['BMP']-emp_0)<0.001) & ((aggregate_features['BMP']-emp_0)>=0) & (aggregate_features['VALUE']==value_0)]
                if len(selected)>0:
                    selected_index = selected.index.tolist()[0]
                    aggregate_features.at[selected_index, 'BMP'] = aggregate_features.iloc[0]['BMP']
                else:
                    results.append(aggregate_features.iloc[0].to_list())
                aggregate_features.drop(index = aggregate_features.index[0], axis=0, inplace=True)

        return pd.DataFrame(results, columns=['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE'])


if __name__ == '__main__':
    pass

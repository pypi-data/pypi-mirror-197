import pandas as pd
import sqlite3

class RCI:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file,header=0,low_memory=False)

        self.data['RDWYID'] = self.data['RDWYID'].astype(str).str.zfill(8)
        self.data['RDWYCHAR'] = self.data['RDWYCHAR'].str.strip()

    def get_last_year(self):
        return pd.to_numeric(self.data['CALYEAR']).max()

    def get_aadt_by_rid(self, rid, year):
        selected_data = self.data.loc[(self.data['RDWYID']==rid) & (self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='SECTADT')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','VALUE']].reset_index(drop=True)
    
    def get_aadts(self, year):
        selected_data = self.data.loc[(self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='SECTADT')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','VALUE']].reset_index(drop=True)
    
    def get_interchange_by_rid(self, rid, year):
        selected_data = self.data.loc[(self.data['RDWYID']==rid) & (self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='INTERCHG')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)

    def get_interchanges(self, year):
        selected_data = self.data.loc[(self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='INTERCHG')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
    
    def get_signal_by_rid(self, rid, year):
        selected_data = self.data.loc[(self.data['RDWYID']==rid) & (self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='SIGNALTY') & (self.data['VALUE']=='02')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
    
    def get_signals(self, year):
        selected_data = self.data.loc[(self.data['CALYEAR']==year) & (self.data['RDWYCHAR']=='SIGNALTY') & (self.data['VALUE']=='02')].copy()
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
    
    def get_urban(self, rid, year):
        selected_data = self.get_feature(rid, year, 'FUNCLASS')
        selected_data['FUNCLASS'] = selected_data['VALUE']
        selected_data['VALUE'] = 1
        selected_data.loc[selected_data['FUNCLASS'].astype(int)<10, 'VALUE'] = 0
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)

    def get_feature(self, rid, year, name):
        '''
            parameters:
                rid - roadway id, 8-digit string
                year - rci calendar year
                name - rci characteristic name
            return:
                a pandas dataframe contains selected features: RDWYID, BMP, EMP, RDWYSIDE, CALYEAR, RDWYCHAR, VALUE
        '''
        selected_data = self.data.loc[(self.data['RDWYID']==rid) & (self.data['CALYEAR']==year) & (self.data['RDWYCHAR']==name.upper())].copy()
        selected_data['BMP'] = selected_data['BMP'].apply(lambda x: round(x, 3))
        selected_data['EMP'] = selected_data['EMP'].apply(lambda x: round(x, 3))
        
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
    
    def get_feature_lastest(self, rid, name):
        '''
            parameters:
                rid - roadway id, 8-digit string
                name - rci characteristic name
            return:
                a pandas dataframe contains selected features: RDWYID, BMP, EMP, RDWYSIDE, CALYEAR, VALUE
        '''
        year = self.get_last_year()
        return self.get_feature(rid, year, name)
    
    def get_features(self, rid, year, feature_names):
        features = []
        mps = []
        for feature_name in feature_names:
            rid = str(rid).zfill(8)
            features.append(self.get_feature(rid, year, feature_name))
        
        return features
    
    def get_point_feature(self, rid, year, feature_name):
        '''
            parameters:
                rid - roadway id, 8-digit string
                year - rci calendar year
                feature_name - rci characteristic name
            return:
                a pandas dataframe contains selected features: RDWYID, BMP, EMP, RDWYSIDE, CALYEAR, RDWYCHAR, VALUE
        '''
        selected_data = self.data.loc[(self.data['RDWYID']==rid) & (self.data['CALYEAR']==year) & (self.data['RDWYCHAR']==feature_name.upper())].copy()
        selected_data['BMP'] = round(selected_data['BMP'], 3)
        selected_data['EMP'] = round(selected_data['EMP'], 3)
        results = selected_data[['RDWYID','BMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
        results.columns = ['RDWYID','MP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']
        return results
    
    def get_point_features(self, rid, year, feature_names):
        features = []
        for feature_name in feature_names:
            rid = str(rid).zfill(8)
            features.append(self.get_point_feature(rid, year, feature_name))
        
        return pd.concat(features)
    
    def get_intersections(self, rid, year):
        return self.get_point_features(rid, year, ['INTSDIR1', 'INTSDIR2', 'INTSDIR3', 'INTSDIR4', 'INTSDIR5', 'INTSDIR6', 'INTSDIR7', 'INTSDIR8', 'INTSDIR9'])
        
    def get_unique_values(self, feature_name):
        selected = self.data.loc[self.data['RDWYCHAR']==feature_name.upper()].copy()
        return selected['VALUE'].unique()
    
    def get_radius_by_rid(self, rid, year):
        selected_data = self.get_feature(rid, year, 'HRZDGCRV')
        
        for index, seg in selected_data.iterrows():
            if seg['VALUE']:
                items = seg['VALUE'].split('D')
                if not items[0]:
                    items[0] = '0'
                d = float(items[0])

                items_2 = items[1].split("'")
                if not items_2[0]:
                    items_2[0] = '0'
                m = float(items_2[0])
        
                de = d + m/60
                r = 5729.6 / de

                selected_data.at[index, 'VALUE'] = r

        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)

class RCISQLITE:
    def __init__(self, database_file, table_name):
        self.database = database_file
        self.table_name = table_name

    def __query(self, rid, year, feature_name):
        conn = sqlite3.connect(self.database)
        query_express = "SELECT RDWYID, BEGSECPT AS BMP, ENDSECPT AS EMP, RDWYSIDE, CALYEAR, RDWYCHAR, RCDVALUE AS VALUE FROM " + self.table_name + " WHERE CALYEAR="+str(year)+" AND RDWYID='"+rid+"' AND RDWYCHAR='"+feature_name+"'"
        df = pd.read_sql_query(query_express, conn)
        conn.close()
        return df

    def get_last_year(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CALYEAR) FROM "+ self.table_name)
        cursor.close()
        conn.close()
        return cursor.fetchone()[0]

    def get_aadt_by_rid(self, rid, year):
        return self.__query(rid, year, 'SECTADT')
        
    def get_interchange_by_rid(self, rid, year):
        return self.__query(rid, year, 'INTERCHG')
    
    def get_signal_by_rid(self, rid, year):
        data = self.__query(rid, year, 'SIGNALTY')
        selected_data = data.loc[data['VALUE']=='02']
        return selected_data.copy().reset_index(drop=True)
    
    def get_urban(self, rid, year):
        selected_data = self.query(rid, year, 'FUNCLASS')
        selected_data['FUNCLASS'] = selected_data['VALUE']
        selected_data['VALUE'] = 1
        selected_data.loc[selected_data['FUNCLASS'].astype(int)<10, 'VALUE'] = 0
        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)

    def get_feature(self, rid, year, name):
        return self.__query(rid, year, name.upper())
        
    def get_feature_lastest(self, rid, name):
        '''
            parameters:
                rid - roadway id, 8-digit string
                name - rci characteristic name
            return:
                a pandas dataframe contains selected features: RDWYID, BMP, EMP, RDWYSIDE, CALYEAR, VALUE
        '''
        year = self.get_last_year()
        return self.get_feature(rid, year, name)
    
    def get_features(self, rid, year, feature_names):
        features = []
        for feature_name in feature_names:
            rid = str(rid).zfill(8)
            features.append(self.get_feature(rid, year, feature_name))
        
        return features
    
    def get_point_feature(self, rid, year, feature_name):
        '''
            parameters:
                rid - roadway id, 8-digit string
                year - rci calendar year
                feature_name - rci characteristic name
            return:
                a pandas dataframe contains selected features: RDWYID, BMP, EMP, RDWYSIDE, CALYEAR, RDWYCHAR, VALUE
        '''
        selected_data = self.__query(rid, year, feature_name.upper())
        selected_data['BMP'] = round(selected_data['BMP'], 3)
        selected_data['EMP'] = round(selected_data['EMP'], 3)
        results = selected_data[['RDWYID','BMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)
        results.columns = ['RDWYID','MP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']
        return results
    
    def get_point_features(self, rid, year, feature_names):
        features = []
        for feature_name in feature_names:
            rid = str(rid).zfill(8)
            features.append(self.get_point_feature(rid, year, feature_name))
        
        return pd.concat(features)
    
    def get_intersections(self, rid, year):
        return self.get_point_features(rid, year, ['INTSDIR1', 'INTSDIR2', 'INTSDIR3', 'INTSDIR4', 'INTSDIR5', 'INTSDIR6', 'INTSDIR7', 'INTSDIR8', 'INTSDIR9'])

    def get_radius_by_rid(self, rid, year):
        selected_data = self.get_point_features(rid, year, 'HRZDGCRV')
        
        for index, seg in selected_data.iterrows():
            if seg['VALUE']:
                items = seg['VALUE'].split('D')
                if not items[0]:
                    items[0] = '0'
                d = float(items[0])

                items_2 = items[1].split("'")
                if not items_2[0]:
                    items_2[0] = '0'
                m = float(items_2[0])
        
                de = d + m/60
                r = 5729.6 / de

                selected_data.at[index, 'VALUE'] = r

        return selected_data[['RDWYID','BMP','EMP','RDWYSIDE','CALYEAR','RDWYCHAR','VALUE']].reset_index(drop=True)

if __name__ == '__main__':
    pass

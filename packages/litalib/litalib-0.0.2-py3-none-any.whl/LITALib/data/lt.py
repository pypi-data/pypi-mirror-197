import sqlite3
import pandas as pd
import urllib.parse, urllib.request, ssl
import json
import numpy as np

class LT:
    def __init__(self):
        pass
    
    @staticmethod
    def load_ltpoints_from_sqlite(database, table, rid, bmp, emp):
        conn = sqlite3.connect(database)
        express = "SELECT * FROM "+table+" WHERE ROADWAY='"+rid+"' AND MP>="+str(bmp)+" AND MP<="+str(emp)
        df = pd.read_sql_query(express, conn)
        conn.close()
        return df

    @staticmethod
    def load_from_mapservice(url, input_fields="*", query=""):

        params = {'where': query,
                'geometryType': 'esriGeometryPoint',
                'spatialRel': 'esriSpatialRelIntersects',
                'relationParam': '',
                'outFields': input_fields,
                'returnGeometry': 'true',
                'geometryPrecision':'',
                'outSR': '',
                'returnIdsOnly': 'false',
                'returnCountOnly': 'false',
                'returnGeometry': 'true',
                'orderByFields': '',
                'groupByFieldsForStatistics': '',
                'returnZ': 'false',
                'returnM': 'false',
                'returnDistinctValues': 'false',
                'f': 'pjson'}

        encode_params = urllib.parse.urlencode(params).encode("utf-8")
        response = urllib.request.urlopen(url, encode_params, context=ssl._create_unverified_context())
        results = response.read()
        raw_json = json.loads(results)
        formatted_json = [feature['attributes'] for feature in raw_json['features']]
        return pd.json_normalize(formatted_json)

    @staticmethod
    def load_ltpoints_from_mapservice(url, rid, bmp = None, emp = None):

        if ((bmp is None) and (emp is None)):
            query = "ROADWAY='"+rid+"'"
        elif emp is None:
            query = "ROADWAY='"+rid+"' AND MP>="+str(bmp)
        elif bmp is None:
            query = "ROADWAY='"+rid+"' AND MP<="+str(emp)
        else:
            query = "ROADWAY='"+rid+"' AND MP>="+str(bmp)+" AND MP<="+str(emp)
        
        return LT.load_from_mapservice(url, query=query)
    
    @staticmethod
    def select_ltpoints_by_side(lt_data, roadside='C'):
        if roadside.upper().strip() == "R":
            data_side = lt_data.loc[lt_data["LANE_ID"].isin([1, 3, 5, 7, 9, 11, 13])]
        elif roadside.upper().strip() == "L":
            data_side = lt_data.loc[lt_data["LANE_ID"].isin([2, 4, 6, 8, 10, 12, 14])]
        else:
            data_side = lt_data
        return data_side

if __name__ == '__main__':
    lt_points_1 = LT.load_ltpoints_from_mapservice('https://arcgis.ddns.net:6443/arcgis/rest/services/maps/lt_d7/MapServer/0/query?', '10290000')
    print(lt_points_1)
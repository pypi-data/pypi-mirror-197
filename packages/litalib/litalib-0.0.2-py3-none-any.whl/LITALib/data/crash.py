import sqlite3
import pandas as pd
import urllib.parse, urllib.request, ssl
import json
import numpy as np

class SSOGIS:
    def __init__(self, url = ''):
        if url:
            self.url = url
        else:
            self.url = "https://gis.fdot.gov/arcgis/rest/services/sso/ssogis/FeatureServer/11/query?"

    def load_from_mapservice(self, input_fields="*", query=""):

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
        response = urllib.request.urlopen(self.url, encode_params, context=ssl._create_unverified_context())
        results = response.read()
        raw_json = json.loads(results)
        formatted_json = [feature['attributes'] for feature in raw_json['features']]
        return pd.json_normalize(formatted_json)

    def load_crashes_from_mapservice(self, rid, bmp, emp, years=[]):
        year_string = ''
        for year in years:
            year_string += str(year) + ','
        
        if year_string:
            year_string = year_string[:-1]
            query = "ROADWAYID='"+rid+"' AND LOCMP>="+str(bmp)+" AND LOCMP<="+str(emp)+" AND CALENDAR_YEAR IN ("+year_string+")"
        else:
            query = "ROADWAYID='"+rid+"' AND LOCMP>="+str(bmp)+" AND LOCMP<="+str(emp)

        return self.load_from_mapservice(query=query)
    
    def count_crashes(self, crashes, period = 'all', crash_type = 'all', severity = 'all'):
        '''
            
        '''
        

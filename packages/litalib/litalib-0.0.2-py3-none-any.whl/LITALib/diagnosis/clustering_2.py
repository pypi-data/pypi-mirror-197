import pandas as pd
import numpy as np
from core import *
from ..data.lt import LT

class Cluster:
    def __init__(self, lt_points, bmp, emp, fields = ['MP', 'FC_6', 'DISTANCE', 'LANE_ID']):
        self.lt = lt_points.loc[(lt_points[fields[0]]>=bmp) & (lt_points[fields[0]]<=emp)].reset_index()
        self.bmp = bmp
        self.emp = emp
        self.field_mp = fields[0]
        self.fc = fields[1]
        self.distance = fields[2]
        self.lane = fields[3]

if __name__=="__main__":
    print('Loading LT data ...')
    lt_points = LT.load_ltpoints_from_mapservice('https://arcgis.ddns.net:6443/arcgis/rest/services/maps/lt_d7/MapServer/0/query?', '10290000')

    print(lt_points)
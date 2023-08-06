import pandas as pd
from ..data.rci import RCI
from .aggregation import Aggregation
from .segmentation import Segmentation

class Utility:
    def __init__(self, rci):
        self.rci = rci
        self.segmentor = Segmentation()
        self.aggregator = Aggregation()
        
    def get_lane_miles(self, rid, bmp, emp, year):
        lanes = self.rci.get_feature(rid, year, 'NOLANES')
        lanes_agg = self.aggregator.centralize(lanes, method='sum')
        segs = self.segmentor.split_by_feature(rid, bmp, emp, lanes_agg)

        segs['LENGTH'] = segs['EMP'] - segs['BMP']
        segs['LANE_MILES'] = segs['LENGTH'] * segs['VALUE']

        return sum(segs['LANE_MILES'])
    

if __name__ == "__main__":
    print("Loading RCI data ...")
    rci = RCI(r'D:\repos\LT_D7W\rci\rci_d7.csv')
    ut = Utility(rci)
    print(ut.get_lane_miles('02030000', 0, 25.107, 2021))
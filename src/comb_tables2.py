import pickle
import warnings

import numpy as np
import pandas as pd





# resort_dfs = [telluride, BM, steamboat, AS, WC]


# '''fixing trail names'''
# # WC['trail_name'] = WC['trail_name'].apply(lambda x: ' '.join(x.split()[1:]))
# WC['trail_name'] = WC['trail_name'].apply(lambda x: ' '.join(x.split()[1:]) if x.split()[
#                                           0] in ['l', 'u', 'm', 'c', 'g', 'r'] else ' '.join(x.split()))


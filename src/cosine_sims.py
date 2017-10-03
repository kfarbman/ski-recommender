import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

pkl_file = open('../data/df.pkl', 'rb')
df = pickle.load(pkl_file)
pkl_file.close() 

df = df.reset_index(drop=True)

features = ['top_elev_(ft)', 
            'bottom_elev_(ft)', 
            'vert_rise_(ft)', 
            'slope_length_(ft)', 
            'avg_width_(ft)', 
            'slope_area_(acres)', 
            'avg_grade_(%)', 
            'max_grade_(%)', 
            'groomed']
X = df[features].values

ss = StandardScaler()
X = ss.fit_transform(X)

def cos_sim_recommendations_resort(trail_name, resort_name, X, n=5, resort=None):
    index = df.index[(df['trail_name'] == trail_name) & (df['resort'] == resort_name)][0]
    trail = X[index].reshape(1,-1)
    cs = cosine_similarity(trail, X)
    rec_index = np.argsort(cs)[0][::-1][1:]
    ordered_df = df.loc[rec_index]
    if resort:
        ordered_df = ordered_df[ordered_df['resort'] == resort]
    rec_df = ordered_df.head(n)
    orig_row = df.loc[[index]].rename(lambda x: 'original')
    total = pd.concat((orig_row,rec_df))
    return total
    
print(cos_sim_recommendations_resort('Sorensen Park','Winter Park',X,n=5,resort='Winter Park'))
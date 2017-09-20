from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

with open('../df.pkl','rb') as f:
    df = pickle.load(f)    
    
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

def cos_sim_recs(index, n=5, resort=None):
    trail = X[index].reshape(1,-1)
    cs = cosine_similarity(trail, X)
    rec_index = np.argsort(cs)[0][::-1][1:]
    ordered_df = df.loc[rec_index]
    if resort:
        ordered_df = ordered_df[ordered_df['resort'] == resort]
    rec_df = ordered_df.head(n)
    rec_df = rec_df.reset_index(drop=True)
    rec_df.index = rec_df.index+1
    orig_row = df.loc[[index]].rename(lambda x: 'original')
    total = pd.concat((orig_row,rec_df))
    return total
    

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html',df=df)
    
@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    resort = request.form['resort']
    trail = request.form['trail']
    index = int(trail)
    dest_resort = request.form['dest_resort']
    num_recs = int(request.form['num_recs'])
    rec_df = cos_sim_recs(index,num_recs,dest_resort)
    rec_df['groomed'][rec_df['groomed'] == 1] = 'Groomed'
    rec_df['groomed'][rec_df['groomed'] == 0] = 'Ungroomed'
    rec_df['color_names'] = rec_df['colors']
    rec_df['color_names'][rec_df['color_names'] == 'green'] = 'Green'
    rec_df['color_names'][rec_df['color_names'] == 'blue'] = 'Blue'
    rec_df['color_names'][rec_df['color_names'] == 'black'] = 'Black'
    rec_df['color_names'][rec_df['color_names'] == 'bb'] = 'Double Black'
    rec_df = rec_df[['trail_name','resort','location','color_names','groomed','top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','slope_length_(ft)','avg_width_(ft)','slope_area_(acres)','avg_grade_(%)','max_grade_(%)']]
    rec_df.columns = ['Trail Name', 'Resort','Location','Rating','Groomed','Top Elev (ft)', 'Bottom Elev (ft)', 'Vert Rise (ft)', 'Slope Length (ft),', 'Avg Width (ft)', 'Slope Area (acres)', 'Avg Grade (%)', 'Max Grade (%)']
    return render_template('recommendations.html',rec_df=rec_df)
    
@app.route('/get_trails')
def get_trails():
    resort = request.args.get('resort')
    # print(resort)
    if resort:
        sub_df = df[df['resort'] == resort]
        id_name = zip(list(sub_df.index),list(sub_df['trail_name']))
        data = [{"id": str(x[0]), "name": x[1]} for x in id_name]
        # print(data)
    return jsonify(data)
    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
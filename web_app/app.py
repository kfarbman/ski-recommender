from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

with open('../df.pkl','rb') as f:
    df = pickle.load(f)    
    
with open('../mtn_df.pkl','rb') as f:
    mtn_df = pickle.load(f)
    
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

mtn_features = ['top_elev_(ft)', 
                'bottom_elev_(ft)', 
                'vert_rise_(ft)', 
                'slope_length_(ft)', 
                'avg_width_(ft)', 
                'slope_area_(acres)', 
                'avg_grade_(%)', 
                'max_grade_(%)', 
                'groomed',
                'resort_bottom',
                'resort_top',
                'greens',
                'blues',
                'blacks',
                'bbs',
                'lifts',
                'price']
                
X_mtn = mtn_df[mtn_features].values    
X_mtn = ss.fit_transform(X_mtn)

resort_stats_df = mtn_df[['resort', 'resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price']].drop_duplicates()

links = {'Loveland': ["../static/images/Loveland.jpg", "http://skiloveland.com/trail-lift-report/"],
           'Arapahoe Basin': ['http://arapahoebasin.com/ABasin/image-library/inline-landscape/A-BASIN-17-18-Front.jpg', 'http://arapahoebasin.com/ABasin/snow-conditions/terrain.aspx'],
           'Copper': ['http://www.coppercolorado.com/sites/copper/files/2017-07/Web-TrailMap-WinterFY17.jpg', 'http://www.coppercolorado.com/the-mountain/trail-lift-info/winter-trail-report'],
           'Eldora': ['http://www.eldora.com/sites/eldora/files/inline-images/map2-web.jpg', 'http://www.eldora.com/the-mountain/lift-trail-report/snow-grooming-alpine'],
           'Alpine Meadows': ['../static/images/AM.jpeg', 'http://squawalpine.com/skiing-riding/weather-conditions-webcams/lift-grooming-status'],
           'Vail': ['https://i.pinimg.com/originals/91/22/4b/91224b89f5b358f4fbe329ca0a0741dd.jpg', 'http://www.vail.com/mountain/current-conditions/whats-open-today.aspx#/GA4'],
           'Monarch': ['http://15098-presscdn-0-99.pagely.netdna-cdn.com/wp-content/uploads/2015/06/wall-map.jpg', 'http://www.skimonarch.com/daily-snow-report/'],
           'Crested Butte': ['../static/images/CB.jpeg', 'http://www.skicb.com/the-mountain/grooming-lift-status'],
           'Taos': ['https://www.skitaos.com/uploaded/trail%20maps/1-01.jpg', 'http://www.skitaos.com/lifts-trails/'],
           'Diamond Peak': ['http://www.diamondpeak.com/uploads/pages/DP_TrailMaponly.png', 'http://www.diamondpeak.com/mountain/conditions'],
           'Winter Park': ['../static/images/WP.jpeg', 'https://www.winterparkresort.com/the-mountain/weather-dashboard#mountain-status'],
           'Beaver Creek': ['http://www.beavercreek.com/~/media/beaver%20creek/files/maps/bc%20fy17%20winter%20trail%20map.ashx', 'http://www.beavercreek.com/the-mountain/terrain-status.aspx#/TerrainStatus']}

def cos_sim_recs(index, n=5, resort=None, color=None):
    trail = X[index].reshape(1,-1)
    cs = cosine_similarity(trail, X)
    rec_index = np.argsort(cs)[0][::-1][1:]
    ordered_df = df.loc[rec_index]
    if resort:
        ordered_df = ordered_df[ordered_df['resort'] == resort]
    if color:
        ordered_df = ordered_df[ordered_df['colors'].isin(color)]
    rec_df = ordered_df.head(n)
    rec_df = rec_df.reset_index(drop=True)
    rec_df.index = rec_df.index+1
    orig_row = df.loc[[index]].rename(lambda x: 'original')
    total = pd.concat((orig_row,rec_df))
    return total
    
def mtn_recommender(index, n=5):
    trail = X_mtn[index].reshape(1,-1)
    cs = cosine_similarity(trail, X_mtn)[0]
    mtn_df['cosine_sim'] = cs
    s = mtn_df.groupby('resort').mean()['cosine_sim'].sort_values()[::-1]
    orig_row = mtn_df.loc[[index]].rename(lambda x: 'original')
    return orig_row, list(s.index[:n])
    
def clean_df_for_recs(df):
    df['groomed'][df['groomed'] == 1] = 'Groomed'
    df['groomed'][df['groomed'] == 0] = 'Ungroomed'
    df['color_names'] = df['colors']
    df['color_names'][df['color_names'] == 'green'] = 'Green'
    df['color_names'][df['color_names'] == 'blue'] = 'Blue'
    df['color_names'][df['color_names'] == 'black'] = 'Black'
    df['color_names'][df['color_names'] == 'bb'] = 'Double Black'
    df = df[['trail_name','resort','location','color_names','groomed','top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','slope_length_(ft)','avg_width_(ft)','slope_area_(acres)','avg_grade_(%)','max_grade_(%)']]
    df.columns = ['Trail Name', 'Resort','Location','Difficulty','Groomed','Top Elev (ft)', 'Bottom Elev (ft)', 'Vert Rise (ft)', 'Slope Length (ft)', 'Avg Width (ft)', 'Slope Area (acres)', 'Avg Grade (%)', 'Max Grade (%)']
    return df
    
@app.route('/', methods =['GET','POST'])    
def index():
    return render_template('home.html')

@app.route('/trails', methods=['GET','POST'])
def trails():
    return render_template('index.html',df=df)
    
@app.route('/mountains', methods=['GET','POST'])
def mountains():
    return render_template('mtn_index.html',df=df)
    
@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    color_lst = None
    if request.form.get('green'):
        color_lst = ['green']
    if request.form.get('blue'):
        color_lst = ['green','blue']
    if request.form.get('black'):
        color_lst = ['green','blue','black']
    if request.form.get('bb'):
        color_lst = ['green','blue','black','bb']
    # CHECKBOX FUNCTIONALITY!!!
    resort = request.form['resort']
    trail = request.form['trail']
    if trail != '':
        index = int(trail)
        dest_resort = request.form['dest_resort']
        num_recs = int(request.form['num_recs'])
        rec_df = cos_sim_recs(index,num_recs,dest_resort,color_lst)
        rec_df = clean_df_for_recs(rec_df)
        if dest_resort == '':
            resort_links = links[resort]
        else:
            resort_links = links[dest_resort]
        return render_template('recommendations.html',rec_df=rec_df,resort_links=resort_links)
    return 'You must select a trail.'
    
@app.route('/mtn_recommendations', methods=['GET','POST'])
def mtn_recommendations():
    resort = request.form['resort']
    trail = request.form['trail']
    index = int(trail)
    num_recs = int(request.form['num_recs'])
    row, recs = mtn_recommender(index,num_recs)
    results_df = pd.DataFrame(columns=['resort', 'resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price'])
    for rec in recs:
        results_df = results_df.append(resort_stats_df[resort_stats_df['resort'] == rec])
    row = clean_df_for_recs(row)
    results_df.columns = ['Resort','Bottom Elevation (ft)', 'Top Elevation (ft)', 'Percent Greens', 'Percent Blues', 'Percent Blacks', 'Percent Double  Blacks', 'Number of Lifts', 'Price']
    return render_template('mtn_recommendations.html',row=row,results_df=results_df,links=links)
    
@app.route('/get_trails')
def get_trails():
    resort = request.args.get('resort')
    # print(resort)
    if resort:
        sub_df = df[df['resort'] == resort]
        id_name_color = [("","Select a Trail...","white")] + list(zip(list(sub_df.index),list(sub_df['trail_name']),list(sub_df['colors'])))
        data = [{"id": str(x[0]), "name": x[1], "color": x[2]} for x in id_name_color]
        # print(data)
    return jsonify(data)
    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
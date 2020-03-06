import pickle

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from recsys import SkiRunRecommender

app = Flask(__name__)

recsys = SkiRunRecommender()
    
@app.route('/', methods =['GET','POST'])    
def index():
    return render_template('home.html')

# TODO: Correct df input
@app.route('/trails', methods=['GET','POST'])
def trails():
    return render_template('index.html',df=recsys.load_trail_data())
    
# TODO: Correct df input
@app.route('/mountains', methods=['GET','POST'])
def mountains():
    return render_template('mtn_index.html',df=recsys.load_mountain_data())

@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    color_lst = None

    dict_run_requests = {"Green": ["Green"],
                        "Blue": ["Green", "Blue"],
                        "Black": ["Green", "Blue", "Black"],
                        "Double Black": ["Green", "Blue", "Black", "Double Black"]}

    request_difficulty = "max_difficulty"
    color_lst = request.form.get(dict_run_requests[request_difficulty])

    # if request.form.get('green'):
    #     color_lst = ['green']
    # if request.form.get('blue'):
    #     color_lst = ['green','blue']
    # if request.form.get('black'):
    #     color_lst = ['green','blue','black']
    # if request.form.get('bb'):
    #     color_lst = ['green','blue','black','bb']
    
    # CHECKBOX FUNCTIONALITY!!!
    resort = request.form['Resort']
    if resort == '':
        return 'You must select a trail from your favorite resort.'
    trail = request.form['trail']
    if trail != '':
        index = int(trail)
        dest_resort = request.form['dest_resort']
        num_recs = int(request.form['num_recs'])
        rec_df = recsys.trail_recommendations(index,num_recs,dest_resort,color_lst)
        # rec_df = recsys.clean_df_for_recs(rec_df)
        if dest_resort == '':
            resort_links = recsys.links[resort]
        else:
            resort_links = recsys.links[dest_resort]
        return render_template('recommendations.html',rec_df=rec_df,resort_links=resort_links)
    return 'You must select a trail.'
    
# TODO: Correct inputs
@app.route('/mtn_recommendations', methods=['GET','POST'])
def mtn_recommendations():
    resort = request.form['resort']
    if resort == '':
        return 'You must select a trail from your favorite resort.'
    trail = request.form['trail']
    if trail != '':
        index = int(trail)
        num_recs = int(request.form['num_recs'])
        row, recs = recsys.mountain_recommendations(index,num_recs)
        results_df = pd.DataFrame(columns=['resort', 'resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price'])
        for rec in recs:
            results_df = results_df.append(resort_stats_df[resort_stats_df['resort'] == rec])
        row = self.clean_df_for_recs(row)
        results_df.drop('Price', axis=1, inplace=True)
        results_df.columns = ['Resort','Bottom Elevation (ft)', 'Top Elevation (ft)', 'Percent Greens', 'Percent Blues', 'Percent Blacks', 'Percent Double  Blacks', 'Number of Lifts']
        return render_template('mtn_recommendations.html',row=row,results_df=results_df,links=links)
    return 'You must select a trail.'

@app.route('/get_trails')
def get_trails():
    resort = request.args.get('Resort')
    if resort:
        df = recsys.load_trail_data()
        sub_df = df[df['Resort'] == resort]
        sub_df['trail_name'] = sub_df['trail_name'].apply(lambda x: x.split()).apply(lambda x: (x[1:] + ['Upper']) if (x[0] == 'Upper') else x).apply(lambda x: ' '.join(x))
        sub_df['trail_name'] = sub_df['trail_name'].apply(lambda x: x.split()).apply(lambda x: (x[1:] + ['Lower']) if (x[0] == 'Lower') else x).apply(lambda x: ' '.join(x))
        sub_df.sort_values(by='trail_name',inplace=True)
        id_name_color = [("","Select a Trail...","white")] + list(zip(list(sub_df.index),list(sub_df['trail_name']),list(sub_df['colors'])))
        data = [{"id": str(x[0]), "name": x[1], "color": x[2]} for x in id_name_color]
        # print(data)
    return jsonify(data)

@app.route('/trail_map/<resort>')
def trail_map(resort):
    resort_image = recsys.links[resort][0]
    return render_template('trail_map.html',resort_image=resort_image)
    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
    
    # recsys = SkiRunRecommender()

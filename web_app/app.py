import pandas as pd
from flask import Flask, jsonify, render_template, request

from recsys import SkiRunRecommender

app = Flask(__name__)

recsys = SkiRunRecommender()
    
@app.route('/', methods =['GET','POST'])    
def index():
    return render_template('home.html')

@app.route('/trails', methods=['GET','POST'])
def trails():
    df_trails = recsys.load_trail_data()
    return render_template('index.html',df=df_trails)

@app.route('/mountains', methods=['GET','POST'])
def mountains():
    df_mountains = recsys.load_mountain_data()
    return render_template('mtn_index.html',df=df_mountains)

@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    
    dict_run_requests = {"green": ["Green"],
                         "blue": ["Green", "Blue"],
                         "black": ["Green", "Blue", "Black"],
                         "double-black": ["Green", "Blue", "Black", "Double Black"]}
    
    # Default recommendations: runs of all difficulty
    color_lst = dict_run_requests["double-black"]
    
    # Filter based on max run difficulty requested
    if request.form.get('green'):
        color_lst = dict_run_requests["green"]
    if request.form.get('blue'):
        color_lst = dict_run_requests["blue"]
    if request.form.get('black'):
        color_lst = dict_run_requests["black"]
    if request.form.get('bb'):
        color_lst = dict_run_requests["double-black"]

    # CHECKBOX FUNCTIONALITY!!!
    resort = request.form['resort']
    if resort == '':
        return 'You must select a trail from your favorite resort.'
    trail = request.form['trail']
    if trail != '':
        index = int(trail)
        dest_resort = request.form['dest_resort']
        num_recs = int(request.form['num_recs'])
        rec_df = recsys.trail_recommendations(
            index, num_recs, dest_resort, color=color_lst)
        if dest_resort == '':
            resort_links = recsys.links[resort]
        else:
            resort_links = recsys.links[dest_resort]
        return render_template('recommendations.html', rec_df=rec_df, resort_links=resort_links)
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

        # BUG: Out of bounds issue due to trying to request from trails, not mountains
        # TODO: Remove run duplicates?
        row, recs = recsys.mountain_recommendations(index,num_recs)
        # row = recsys.trail_recommendations(index, n=num_recs, resort=None, color=None)
        # results_df = pd.DataFrame(columns=['resort', 'resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price'])

        df_mountains = recsys.load_mountain_data()

        results_df = df_mountains[df_mountains["Resort"].isin(recs)]

        row = row[recsys.new_trail_features]
        # results_df.drop('Price', axis=1, inplace=True)
        results_df = results_df[recsys.new_features]
        results_df.drop_duplicates("Resort", keep="first", inplace=True)
        # results_df.columns = ['Resort','Bottom Elevation (ft)', 'Top Elevation (ft)', 'Percent Greens', 'Percent Blues', 'Percent Blacks', 'Percent Double  Blacks', 'Number of Lifts']
        return render_template('mtn_recommendations.html',row=row,results_df=results_df,links=recsys.links)
    return 'You must select a trail.'

@app.route('/get_trails')
def get_trails():
    resort = request.args.get('resort')
    if resort:
        df = recsys.load_trail_data()
        sub_df = df[df['Resort'] == resort]
        sub_df.sort_values(by='Trail Name', inplace=True)
        id_name_color = [("", "Select a Trail...", "white")] + list(zip(list(sub_df.index),
                                                                        list(
                                                                            sub_df['Trail Name']),
                                                                        list(sub_df['Difficulty'])))
        data = [{"id": str(x[0]), "name": x[1], "color": x[2]}
                for x in id_name_color]
    return jsonify(data)

@app.route('/trail_map/<resort>')
def trail_map(resort):
    resort_image = recsys.links[resort][0]
    return render_template('trail_map.html',resort_image=resort_image)
    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)

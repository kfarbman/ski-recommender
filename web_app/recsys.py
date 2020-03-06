# import pickle

import numpy as np
import pandas as pd
# from flask import Flask, jsonify, render_template, request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# app = Flask(__name__)

class SkiRunRecommender:
    
    def __init__(self):

        self.trail_features = [
                            # 'Trail Name',
                            'Top Elev (ft)',
                            'Bottom Elev (ft)',
                            "Vertical Drop (ft)",
                            # "Difficulty",
                            # "Resort",
                            # 'vert_rise_(ft)',
                            'Slope Length (ft)',
                            "Average Steepness",
                            # 'avg_width_(ft)',
                            # 'slope_area_(acres)',
                            # 'avg_grade_(%)',
                            # 'max_grade_(%)',
                            # 'Groomed'
                            ]
        
        self.mtn_features = [
                            # 'Top Elev (ft)',
                            # 'Bottom Elev (ft)',
                            # 'Slope Length (ft)',
                            # 'avg_width_(ft)',
                            # 'slope_area_(acres)',
                            # 'avg_grade_(%)',
                            # 'max_grade_(%)',
                            # 'Groomed',
                            'Base', # Base of mountain
                            'Top', # Top of mountain
                            'Vertical Rise (ft)',
                            'Green',
                            'Blue',
                            'Black',
                            'Double Black',
                            'Terrain Park',
                            # 'Resort',
                            'Lifts',
                            'Price']

        # TODO: Are images of maps showing up properly?
        self.links = {'Loveland': ["../static/images/Loveland.jpg", "http://skiloveland.com/trail-lift-report/"],
                'Arapahoe Basin': ['https://www.arapahoebasin.com/uploaded/trail%20maps/A-BASIN-17-18-Front.jpg','http://arapahoebasin.com/ABasin/snow-conditions/terrain.aspx'],
                'Copper': ['http://www.coppercolorado.com/sites/copper/files/2017-07/Web-TrailMap-WinterFY17.jpg', 'http://www.coppercolorado.com/the-mountain/trail-lift-info/winter-trail-report'],
                'Eldora': ['http://www.eldora.com/sites/eldora/files/inline-images/map2-web.jpg', 'http://www.eldora.com/the-mountain/lift-trail-report/snow-grooming-alpine'],
                'Alpine Meadows': ['../static/images/AM.jpeg', 'http://squawalpine.com/skiing-riding/weather-conditions-webcams/lift-grooming-status'],
                'Vail': ['https://i.pinimg.com/originals/91/22/4b/91224b89f5b358f4fbe329ca0a0741dd.jpg', 'http://www.vail.com/mountain/current-conditions/whats-open-today.aspx#/GA4'],
                'Monarch': ['http://15098-presscdn-0-99.pagely.netdna-cdn.com/wp-content/uploads/2015/06/wall-map.jpg', 'http://www.skimonarch.com/daily-snow-report/'],
                'Crested Butte': ['../static/images/CB.jpeg', 'http://www.skicb.com/the-mountain/grooming-lift-status'],
                'Taos': ['https://www.skitaos.com/uploaded/trail%20maps/1-01.jpg', 'http://www.skitaos.com/lifts-trails/'],
                'Diamond Peak': ['http://www.diamondpeak.com/uploads/pages/DP_TrailMaponly.png', 'http://www.diamondpeak.com/mountain/conditions'],
                'Winter Park': ['../static/images/WP.jpeg', 'https://www.winterparkresort.com/the-mountain/weather-dashboard#mountain-status'],
                'Beaver Creek': ['http://www.mappery.com/maps/Beaver-Creek-Resort-Ski-Trail-Map.jpg', 'http://www.beavercreek.com/the-mountain/terrain-status.aspx#/TerrainStatus']}
    

    def load_trail_data(self):

        # with open('../data/df.pkl','rb') as f:
        #     df = pickle.load(f)

        df_trails = pd.read_csv("../data/trail_data_20200306.csv")

        return df_trails

    def load_mountain_data(self):    
            
        # with open('../data/mtn_df.pkl','rb') as f:
        #     mtn_df = pickle.load(f)

        df_mountain = pd.read_parquet("../data/mountain_data_20200306.parquet")
        
        return df_mountain
    
    def transform_features(self, df, features):

        # Transform trail data
        X = df[features].values
        ss = StandardScaler()
        X_transform = ss.fit_transform(X)

        # Transform mountain data
        # X_mtn = mtn_df[mtn_features].values    
        # X_mtn = ss.fit_transform(X_mtn)
        
        return X_transform

    def create_resort_stats_df(self):

        mtn_df = self.load_mountain_data()

        # [
        # 'Lifts',
        # 'Vertical Rise (ft)',
        # 'Terrain Park',
        # 'Resort',
        # 'Price',
        # 'Total Runs'
        # ]

        resort_stats_df = mtn_df[['Resort', 'Base','Top','Green','Blue','Black','Double Black','Lifts','Price']].drop_duplicates()

        return resort_stats_df

    # TODO: Simplify syntax
    def mountain_recommendations(self, index, n=5):
        """
        Create mountain recommendations

        INPUT
            index: index of mountain for recommendations
            n: number of recommendations (default 5)
        
        OUTPUT
            orig_row: Original row of mountain used for recommendations
            list: list of mountain indices to show user in web app
        """

        df_mountain = self.load_mountain_data()

        X_mtn = self.transform_features(df=df_mountain, features = self.mtn_features)

        trail = X_mtn[index].reshape(1,-1)
        
        cs = cosine_similarity(trail, X_mtn)[0]
        
        df_mountain['cosine_sim'] = cs
        
        df_sorted_recs = df_mountain.groupby('Resort').mean()['cosine_sim'].sort_values()[::-1]
        
        orig_row = df_mountain.loc[[index]].rename(lambda x: 'original')
        
        return orig_row, list(df_sorted_recs.index[:n])

    # TODO: Simplify syntax 
    def trail_recommendations(self, index, n=5, resort=None, color=None):
        """
        Cosine similarity recommendations

        INPUT
            index
            n: number of recommendations
            resort: resort of interest
            color: list of difficulty tiers
        """

        df = self.load_trail_data()

        X = self.transform_features(df=df, features=self.trail_features)
        
        trail = X[index].reshape(1,-1)
        cs = cosine_similarity(trail, X)
        rec_index = np.argsort(cs)[0][::-1][1:]
        ordered_df = df.loc[rec_index]
        if resort:
            ordered_df = ordered_df[ordered_df['Resort'] == resort]
        if color:
            ordered_df = ordered_df[ordered_df['Difficulty'].isin(color)]
        rec_df = ordered_df.head(n)
        rec_df = rec_df.reset_index(drop=True)
        rec_df.index = rec_df.index+1
        orig_row = df.loc[[index]].rename(lambda x: 'original')
        total = pd.concat((orig_row,rec_df))
        return total
    
    # TODO: Complete this step in preprocessing, versus within the web app?
    def clean_df_for_recs(self, df):
        """
        Prepare DataFrame for recommendation processing

        INPUT
            df: Pandas DataFrame
        
        OUTPUT
            Formatted Pandas DataFrame
        """
        
        # TODO: Rename columns inplace
        df = df[['trail_name','resort','location','color_names','Groomed','Top Elev (ft)','Bottom Elev (ft)','vert_rise_(ft)','Slope Length (ft)','avg_width_(ft)','slope_area_(acres)','avg_grade_(%)','max_grade_(%)']]
        df.columns = ['Trail Name', 'Resort','Location','Difficulty','Groomed','Top Elev (ft)', 'Bottom Elev (ft)', 'Vert Rise (ft)', 'Slope Length (ft)', 'Avg Width (ft)', 'Slope Area (acres)', 'Avg Grade (%)', 'Max Grade (%)']
        
        # TODO: Current trail data columns
        # ['Trail Name',
        # 'Bottom Elev (ft)',
        # 'Top Elev (ft)',
        # 'Vertical Drop (ft)',
        # 'Difficulty',
        # 'Resort',
        # 'Slope Length (ft)',
        # 'Average Steepness']

        # TODO: Missing Trail columns (non-API)
        # Location
        # Groomed
        # Vert Rise
        # Avg. Width
        # Slope Area
        # Avg Grade
        # Max Grade
        return df
    
# @app.route('/', methods =['GET','POST'])    
# def index():
#     return render_template('home.html')

# # TODO: Correct df input
# @app.route('/trails', methods=['GET','POST'])
# def trails():
#     return render_template('index.html',df=df)
    
# # TODO: Correct df input
# @app.route('/mountains', methods=['GET','POST'])
# def mountains():
#     return render_template('mtn_index.html',df=df)

# @app.route('/recommendations', methods=['GET','POST'])
# def recommendations():
#     color_lst = None

#     dict_run_requests = {"green": ["green"],
#                         "blue": ["green", "blue"],
#                         "black": ["green", "blue", "black"],
#                         "bb": ["green", "blue", "black", "bb"]}

#     request_difficulty = "max_difficulty"
#     color_lst = request.form.get(dict_run_requests[request_difficulty])

#     # if request.form.get('green'):
#     #     color_lst = ['green']
#     # if request.form.get('blue'):
#     #     color_lst = ['green','blue']
#     # if request.form.get('black'):
#     #     color_lst = ['green','blue','black']
#     # if request.form.get('bb'):
#     #     color_lst = ['green','blue','black','bb']
    
#     # CHECKBOX FUNCTIONALITY!!!
#     resort = request.form['resort']
#     if resort == '':
#         return 'You must select a trail from your favorite resort.'
#     trail = request.form['trail']
#     if trail != '':
#         index = int(trail)
#         dest_resort = request.form['dest_resort']
#         num_recs = int(request.form['num_recs'])
#         rec_df = self.cos_sim_recs(index,num_recs,dest_resort,color_lst)
#         rec_df = self.clean_df_for_recs(rec_df)
#         if dest_resort == '':
#             resort_links = self.links[resort]
#         else:
#             resort_links = self.links[dest_resort]
#         return render_template('recommendations.html',rec_df=rec_df,resort_links=resort_links)
#     return 'You must select a trail.'
    
# # TODO: Correct inputs
# @app.route('/mtn_recommendations', methods=['GET','POST'])
# def mtn_recommendations(self):
#     resort = request.form['resort']
#     if resort == '':
#         return 'You must select a trail from your favorite resort.'
#     trail = request.form['trail']
#     if trail != '':
#         index = int(trail)
#         num_recs = int(request.form['num_recs'])
#         row, recs = self.mtn_recommender(index,num_recs)
#         results_df = pd.DataFrame(columns=['resort', 'resort_bottom','resort_top','greens','blues','blacks','bbs','lifts','price'])
#         for rec in recs:
#             results_df = results_df.append(resort_stats_df[resort_stats_df['resort'] == rec])
#         row = self.clean_df_for_recs(row)
#         results_df.drop('Price', axis=1, inplace=True)
#         results_df.columns = ['Resort','Bottom Elevation (ft)', 'Top Elevation (ft)', 'Percent Greens', 'Percent Blues', 'Percent Blacks', 'Percent Double  Blacks', 'Number of Lifts']
#         return render_template('mtn_recommendations.html',row=row,results_df=results_df,links=links)
#     return 'You must select a trail.'

# @app.route('/get_trails')
# def get_trails(self):
#     resort = request.args.get('resort')
#     if resort:
#         df = self.load_trail_data()
#         sub_df = df[df['resort'] == resort]
#         sub_df['trail_name'] = sub_df['trail_name'].apply(lambda x: x.split()).apply(lambda x: (x[1:] + ['Upper']) if (x[0] == 'Upper') else x).apply(lambda x: ' '.join(x))
#         sub_df['trail_name'] = sub_df['trail_name'].apply(lambda x: x.split()).apply(lambda x: (x[1:] + ['Lower']) if (x[0] == 'Lower') else x).apply(lambda x: ' '.join(x))
#         sub_df.sort_values(by='trail_name',inplace=True)
#         id_name_color = [("","Select a Trail...","white")] + list(zip(list(sub_df.index),list(sub_df['trail_name']),list(sub_df['colors'])))
#         data = [{"id": str(x[0]), "name": x[1], "color": x[2]} for x in id_name_color]
#         # print(data)
#     return jsonify(data)

# @app.route('/trail_map/<resort>')
# def trail_map(self, resort):
#     resort_image = self.links[resort][0]
#     return render_template('trail_map.html',resort_image=resort_image)
    
if  __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
    
    recsys = SkiRunRecommender()

    df_trails = recsys.load_trail_data()

    X_transform = recsys.transform_features(df=df_trails, features=recsys.trail_features)
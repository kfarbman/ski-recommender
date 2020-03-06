import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


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
    # TODO: Add dummied features for additional data
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
        
        df_mountain['cosine_sim'] = cosine_similarity(trail, X_mtn)[0]
        
        df_sorted_recs = df_mountain.groupby('Resort').mean()['cosine_sim'].sort_values()[::-1]
        
        orig_row = df_mountain.loc[[index]].rename(lambda x: 'original')
        
        return orig_row, list(df_sorted_recs.index[:n])

    # TODO: Simplify syntax
    # TODO: Add dummied features for additional data
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
    
if  __name__ == '__main__':
    
    recsys = SkiRunRecommender()

    df_trails = recsys.load_trail_data()

    X_transform = recsys.transform_features(df=df_trails, features=recsys.trail_features)

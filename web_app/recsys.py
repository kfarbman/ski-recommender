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

        self.new_trail_features = [
                            'Trail Name',
                            'Top Elev (ft)',
                            'Bottom Elev (ft)',
                            "Vertical Drop (ft)",
                            "Difficulty",
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
                            # 'Difficulty',
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
        
        self.new_features = [
                            # 'Top Elev (ft)',
                            # 'Bottom Elev (ft)',
                            # 'Slope Length (ft)',
                            # 'avg_width_(ft)',
                            # 'slope_area_(acres)',
                            # 'avg_grade_(%)',
                            # 'max_grade_(%)',
                            # 'Groomed',
                            # 'Difficulty',
                            'Base', # Base of mountain
                            'Top', # Top of mountain
                            'Vertical Rise (ft)',
                            'Green',
                            'Blue',
                            'Black',
                            'Double Black',
                            'Terrain Park',
                            'Resort',
                            'Lifts',
                            'Price']

        """
        Ski Resort Links

        {SKI_RESORT : [RESORT_MAP, RESORT_TRAIL_REPORT]}
        """
        self.links = {
                'Alpine Meadows': ['../static/images/alpine_meadows_trail_map.png', 'https://squawalpine.com/mountain-information/real-time-lift-grooming-status'],
                'Arapahoe Basin': ['https://www.arapahoebasin.com/images/1000/uploaded/Arapahoe%20Sports/2019-20%20Frontside%20Map_smaller.jpg','http://arapahoebasin.com/ABasin/snow-conditions/terrain.aspx'],
                'Aspen Snowmass': ['https://www.aspensnowmass.com/-/media/aspensnowmass/trail-maps/1920/2019-snowmass-website-map.ashx','https://www.aspensnowmass.com/our-mountains/aspen-mountain/snow-and-grooming-report'],
                'Bald Mountain': ['https://d26zlhfpekbdmm.cloudfront.net/files/images/maps/SV_Winter_TrailMap_23.1x17_2019_20_WEB.jpg','https://www.sunvalley.com/mountain-snow-report'],
                'Beaver Creek': ['https://www.beavercreek.com/-/media/beaver-creek/products/brochure/the-mountain/about-the-mountain/trail-map/BC_WinterTrailMap_2019-20', 'https://www.beavercreek.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx'],
                'Copper': ['../static/images/copper_trail_map.png', 'https://www.coppercolorado.com/the-mountain/conditions-weather/snow-report'],
                'Crested Butte': ['../static/images/crested_butte_trail_map.png', 'https://www.skicb.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx'],
                'Diamond Peak': ['https://www.diamondpeak.com/uploads/pages/DP_trailmappage_1819_fullsize.jpg', 'https://www.diamondpeak.com/mountain/conditions'],
                'Eldora': ['https://cms.eldora.com/sites/eldora/files/inline-images/ELDO%202018-19%20Mtn%20Map.jpg', 'http://www.eldora.com/the-mountain/lift-trail-report/snow-grooming-alpine'],
                'Jackson Hole': ['https://www.jacksonhole.com/images/maps/2056-WinterTrailMap.FINAL2019.201.jpg', 'https://www.jacksonhole.com/maps/mountain-winter.html'],
                'Loveland': ["https://secureservercdn.net/166.62.108.43/fb0.327.myftpupload.com/wp-content/uploads/2018/08/Loveland-Ski-Resort-Trail-Map-Web-1024x535.jpg", "http://skiloveland.com/trail-lift-report/"],
                'Monarch': ['https://i0.wp.com/www.skimonarch.com/wp-content/uploads/2019/11/trail-map-web-1.png?ssl=1', 'https://www.skimonarch.com/conditions/'],
                'Steamboat': ['../static/images/steamboat_trail_map.png', 'https://www.steamboat.com/the-mountain/mountain-report#/'],
                'Taos': ['../static/images/taos_trail_map.png', 'https://www.skitaos.com/ski-ride/lifts-trails'],
                'Telluride': ['https://www.tellurideskiresort.com/uploaded/maps/Trail-Map-Legend-Logo_TELSKI_1819_2000.jpg', 'https://www.tellurideskiresort.com/the-mountain/snow-report/'],
                'Vail': ['../static/images/vail_trail_map.png', 'http://www.vail.com/mountain/current-conditions/whats-open-today.aspx#/GA4'],
                'Winter Park': ['../static/images/winter_park_trail_map.png', 'https://www.winterparkresort.com/the-mountain/mountain-report#/'],
                'Wolf Creek': ["../static/images/wolf_creek_trail_map.png" , "https://wolfcreekski.com/grooming-report-page/"]}
    

    def load_trail_data(self):
        """
        Load resort trail data
        """
        df_trails = pd.read_csv("../data/trail_data_20200311.csv")

        return df_trails

    def load_mountain_data(self):
        """
        Load resort mountain data
        """

        df_mountain = pd.read_csv("../data/combined_data_20200311.csv")
        # df_mountain = pd.read_parquet("../data/mountain_data_20200306.parquet")
        
        return df_mountain
    
    def transform_features(self, df, features):
        """
        Transform features for cosine similarity matrix

        INPUT
            df: Pandas DataFrame, trail or mountain data
            features: list of trail or mountain features

        OUTPUT
            Matrix of transformed values
        """

        # Transform trail data
        X = df[features].values
        ss = StandardScaler()
        X_transform = ss.fit_transform(X)
        
        return X_transform

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
    
if  __name__ == '__main__':
    
    recsys = SkiRunRecommender()

    df_trails = recsys.load_trail_data()

    X_transform = recsys.transform_features(df=df_trails, features=recsys.trail_features)

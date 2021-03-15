import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


class SkiRunRecommender:
    def __init__(self):

        self.DUMMY_FEATURES = ["Difficulty", "Groomed", "Location", "Resort"]

        self.MODEL_FEATURES = [
            "Trail Name",
            "Resort",
            "Location",
            "Difficulty",
            "Groomed",
            "Top Elev (ft)",
            "Bottom Elev (ft)",
            "Slope Length (ft)",
            "Percent Greens",
            "Percent Blues",
            "Percent Blacks",
            "Percent Double Blacks",
            "Percent Terrain Parks",
            "Lifts",
            "Price",
        ]

        """
        Ski Resort Links

        {SKI_RESORT : [RESORT_MAP, RESORT_TRAIL_REPORT]}
        """
        self.links = {
            "Alpine Meadows": [
                "../static/images/alpine_meadows_trail_map.png",
                "https://squawalpine.com/mountain-information/real-time-lift-grooming-status",
            ],
            "Arapahoe Basin": [
                "https://www.arapahoebasin.com/images/1000/uploaded/Arapahoe%20Sports/2019-20%20Frontside%20Map_smaller.jpg",
                "http://arapahoebasin.com/ABasin/snow-conditions/terrain.aspx",
            ],
            "Aspen Snowmass": [
                "https://www.aspensnowmass.com/-/media/aspensnowmass/trail-maps/1920/2019-snowmass-website-map.ashx",
                "https://www.aspensnowmass.com/our-mountains/aspen-mountain/snow-and-grooming-report",
            ],
            "Bald Mountain": [
                "https://d26zlhfpekbdmm.cloudfront.net/files/images/maps/SV_Winter_TrailMap_23.1x17_2019_20_WEB.jpg",
                "https://www.sunvalley.com/mountain-snow-report",
            ],
            "Beaver Creek": [
                "https://www.beavercreek.com/-/media/beaver-creek/products/brochure/the-mountain/about-the-mountain/trail-map/BC_WinterTrailMap_2019-20",
                "https://www.beavercreek.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx",
            ],
            "Copper": [
                "../static/images/copper_trail_map.png",
                "https://www.coppercolorado.com/the-mountain/conditions-weather/snow-report",
            ],
            "Crested Butte": [
                "../static/images/crested_butte_trail_map.png",
                "https://www.skicb.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx",
            ],
            "Diamond Peak": [
                "https://www.diamondpeak.com/uploads/pages/DP_trailmappage_1819_fullsize.jpg",
                "https://www.diamondpeak.com/mountain/conditions",
            ],
            "Eldora": [
                "https://cms.eldora.com/sites/eldora/files/inline-images/ELDO%202018-19%20Mtn%20Map.jpg",
                "http://www.eldora.com/the-mountain/lift-trail-report/snow-grooming-alpine",
            ],
            "Jackson Hole": [
                "https://www.jacksonhole.com/images/maps/2056-WinterTrailMap.FINAL2019.201.jpg",
                "https://www.jacksonhole.com/maps/mountain-winter.html",
            ],
            "Loveland": [
                "https://secureservercdn.net/166.62.108.43/fb0.327.myftpupload.com/wp-content/uploads/2018/08/Loveland-Ski-Resort-Trail-Map-Web-1024x535.jpg",
                "http://skiloveland.com/trail-lift-report/",
            ],
            "Monarch": [
                "https://i0.wp.com/www.skimonarch.com/wp-content/uploads/2019/11/trail-map-web-1.png?ssl=1",
                "https://www.skimonarch.com/conditions/",
            ],
            "Steamboat": [
                "../static/images/steamboat_trail_map.png",
                "https://www.steamboat.com/the-mountain/mountain-report#/",
            ],
            "Taos": [
                "../static/images/taos_trail_map.png",
                "https://www.skitaos.com/ski-ride/lifts-trails",
            ],
            "Telluride": [
                "https://www.tellurideskiresort.com/uploaded/maps/Trail-Map-Legend-Logo_TELSKI_1819_2000.jpg",
                "https://www.tellurideskiresort.com/the-mountain/snow-report/",
            ],
            "Vail": [
                "../static/images/vail_trail_map.png",
                "http://www.vail.com/mountain/current-conditions/whats-open-today.aspx#/GA4",
            ],
            "Winter Park": [
                "../static/images/winter_park_trail_map.png",
                "https://www.winterparkresort.com/the-mountain/mountain-report#/",
            ],
            "Wolf Creek": [
                "../static/images/wolf_creek_trail_map.png",
                "https://wolfcreekski.com/grooming-report-page/",
            ],
        }

    def load_resort_data(self) -> pd.core.frame.DataFrame:
        """
        Load combined trail and mountain data
        """

        df_resorts = pd.read_csv(
            "./data/combined_data_20200423.csv", usecols=self.MODEL_FEATURES
        )

        return df_resorts

    def dummy_features(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Dummy features for trail and mountain recommendations

        INPUT
            df: Pandas DataFrame with features to be dummied

        OUTPUT
            Pandas DataFrame with dummied values
        """

        # Remove unused value in cosine similarity calculation
        X_dummied = df.drop("Trail Name", axis=1)

        # Dummy and combine categorical data
        X_dummied = pd.concat(
            [X_dummied, pd.get_dummies(X_dummied[self.DUMMY_FEATURES])], axis=1
        )

        # Drop original features, retain dummy features for calculations
        X_dummied.drop(self.DUMMY_FEATURES, axis=1, inplace=True)

        return X_dummied

    def transform_features(
        self, df: pd.core.frame.DataFrame, features: list
    ) -> np.ndarray:
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

    def mountain_recommendations(
        self, index: int, n: int = 5
    ) -> (pd.core.frame.DataFrame, list):
        """
        Create mountain recommendations

        INPUT
            index: index of mountain for recommendations
            n: number of recommendations (default 5)

        OUTPUT
            orig_row: Original row of mountain used for recommendations
            list: list of mountain indices to show user in web app
        """

        df_mountain = self.load_resort_data()

        # Dummy features
        X_mtn = self.dummy_features(df=df_mountain)

        # Scale features
        X_mtn = self.transform_features(df=X_mtn, features=list(X_mtn.columns))

        trail = X_mtn[index].reshape(1, -1)

        df_mountain["cosine_sim"] = cosine_similarity(trail, X_mtn)[0]

        df_sorted_recs = (
            df_mountain.groupby("Resort").mean()["cosine_sim"].sort_values()[::-1]
        )

        orig_row = df_mountain.loc[[index]].rename(lambda x: "original")

        # Exclude record used for recommendations at index 0
        # Include additional record with N + 1
        return orig_row, list(df_sorted_recs.index[1 : n + 1])

    def trail_recommendations(
        self, index: int, n: int = 5, resort: str = None, color: list = None
    ) -> pd.core.frame.DataFrame:
        """
        Cosine similarity recommendations for trails

        INPUT
            index: DataFrame index of trail provided for comparison
            n: number of trail recommendations
            resort: resort of interest
            color: list of difficulty tiers

        OUTPUT
            Pandas DataFrame, original trail and recommended trails
        """

        df = self.load_resort_data()

        # Dummy features
        X = self.dummy_features(df=df)

        # Scale features
        X = self.transform_features(df=X, features=list(X.columns))

        # Select trail for comparison
        trail = X[index].reshape(1, -1)

        # Create cosine similarity matrix
        cs = cosine_similarity(trail, X)

        # Sort recommendations by highest values
        rec_index = np.argsort(cs)[0][::-1][1:]

        # Order data by index in DataFrame
        ordered_df = df.loc[rec_index]

        # TODO: Filter before calculation for faster computation
        # Filter runs by resort and difficulty
        if resort:
            ordered_df = ordered_df[ordered_df["Resort"] == resort]
        if color:
            ordered_df = ordered_df[ordered_df["Difficulty"].isin(color)]

        # Select top N recommended trails
        rec_df = ordered_df.head(n).reset_index(drop=True)

        # Change index values
        rec_df.index = rec_df.index + 1

        # Find original run in DataFrame
        orig_row = df.loc[[index]].rename(lambda x: "original")

        # Combine original run and recommendations
        total = pd.concat((orig_row, rec_df))

        total = total[self.MODEL_FEATURES]

        return total


if __name__ == "__main__":

    recsys = SkiRunRecommender()

    df_trails = recsys.load_resort_data()

    X_dummied = recsys.dummy_features(df=df_trails)

    X_transform = recsys.transform_features(
        df=X_dummied, features=list(X_dummied.columns)
    )

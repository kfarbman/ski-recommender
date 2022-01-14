import unittest

import pandas as pd
from src.make_mtn_df import MakeMountainDF


class TestMakeMountainDF(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMakeMountainDF, self).__init__(*args, **kwargs)
        self.mountain = MakeMountainDF()

    # FIXME: Test is failing
    def test_rename_resorts(self):
        """
        GIVEN trail and mountain DataFrames

        WHEN location is mapped based on resort name

        THEN test if the data structure is a DataFrame
            and Location column is in DataFrame
        """

        self.mountain.rename_resorts()

        self.assertIsInstance(self.mountain.df_mountains, pd.core.frame.DataFrame)
        self.assertTrue("Location" in self.mountain.df_mountains.columns)

    def test_add_groomed_col(self):
        """
        GIVEN trail data as DataFrame

        WHEN a Groomed column is added based on trail name

        THEN test if data structure is a DataFrame
            and Groomed column is in DataFrame
        """

        df_trails = pd.DataFrame(
            {
                "Name": {0: "Meadow", 1: "Subway", 2: "Alpine Bowl"},
                "Top": {0: 7071, 1: 6966, 2: 8496},
                "Bottom": {0: 6916, 1: 6858, 2: 7761},
                "Vertical drop": {0: 154, 1: 108, 2: 735},
                "Length": {0: 1056.0, 1: 1056.0, 2: 2428.8},
                "Difficulty": {0: "Green", 1: "Green", 2: "Blue"},
                "Lifts": {0: 13, 1: 13, 2: 13},
                "Average Steepness": {0: 0.15, 1: 0.1, 2: 0.3},
                "Resort": {
                    0: "Alpine Meadows",
                    1: "Alpine Meadows",
                    2: "Alpine Meadows",
                },
            }
        )

        df_trails["Groomed"] = "N"
        self.mountain.add_groomed_col(df=df_trails)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)
        self.assertTrue("Groomed" in df_trails.columns)
        self.assertTrue(df_trails["Groomed"].iloc[0] == "N")
        self.assertTrue(df_trails["Groomed"].iloc[2] == "Y")

    def test_rename_resorts(self):
        """
        GIVEN a Pandas DataFrame of trail data

        WHEN resorts are renamed based on the URL

        THEN test if data structure is a DataFrame
            and Resort column is in DataFrame
            and tested resort name is Beaver Creek
        """

        df_trails = pd.DataFrame(
            {
                "Trail Name": {0: "\xa0 Anderson Way ", 1: "\xa0 Bear Paw "},
                "Bottom Elev (ft)": {0: "8025 ft", 1: "8501 ft"},
                "Top Elev (ft)": {0: "8238 ft", 1: "8547 ft"},
                "Vertical Drop (ft)": {0: "213 ft", 1: "43 ft"},
                "Length (mi)": {0: "0.73 mi", 1: "0.17 mi"},
                "URL": {
                    0: "https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green",
                    1: "https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green",
                },
            }
        )

        df_trails = self.mountain.rename_resorts(df=df_trails)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

        self.assertTrue("Resort" in list(df_trails.columns))
        self.assertTrue(all(df_trails["Resort"] == "Beaver Creek"))

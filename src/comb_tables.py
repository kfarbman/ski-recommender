import pickle
import warnings
from itertools import chain

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from create_tables import (AS_table, BC_table, BM_table, DP_table, WC_table,
                           WP_table, loveland_table, monarch_table,
                           steamboat_table, vail_table)

warnings.filterwarnings('ignore')


class CombineTables:

    def __init__(self):
        self.resorts = {
                        'Alpine Meadows': ['../data/resorts/Alpine_Meadows.txt', 'CA'],
                        'Arapahoe Basin': ['../data/resorts/Arapahoe_Basin.txt', 'CO'],
                        'Aspen Snowmass': ['../data/resorts/Aspen_Snowmass.txt', 'CO'],
                        'Bald Mountain': ['../data/resorts/Bald_Mountain.txt', 'CO'],
                        'Beaver Creek': ['../data/resorts/Beaver_Creek.txt', 'CO'],
                        'Copper': ['../data/resorts/Copper.txt', 'CO'],
                        'Crested Butte': ['../data/resorts/Crested_Butte.txt', 'CO'],
                        'Diamond Peak': ['../data/resorts/DP.txt', 'NV'],
                        'Eldora': ['../data/resorts/Eldora.txt', 'CO'],
                        'Loveland': ['../data/resorts/Loveland.txt', 'CO'],
                        'Monarch': ['../data/resorts/Monarch.txt', 'CO'],
                        'Steamboat': ['../data/resorts/Steamboat.txt', 'CO'],
                        'Taos': ['../data/resorts/Taos.txt', 'NM'],
                        'Telluride': ['../data/resorts/Telluride.txt', 'CO'],
                        'Vail': ['../data/resorts/Vail.txt', 'CO'],
                        'Winter Park': ['../data/resorts/WP.csv', 'CO'],
                        'Wolf Creek': ['../data/resorts/Wolf_Creek.txt', 'CO']}

    def format_resorts(self):
        """
        """

        #TODO: Create list of resort DataFrames
        # TODO: Pass key from resorts dict to make_dataframe
        lst_resorts = []
        
        # Aspen Snowmass
        df_resort = AS_table.make_dataframe(self.resorts["Aspen Snowmass"][0])
        df_resort = AS_table.preprocess_data(df=df_resort,
            resort = "Aspen Snowmass",
            location = "CO")
        lst_resorts.append(df_resort)
        
        # Bald Mountain
        df_resort = BM_table.make_dataframe(self.resorts["Bald Mountain"][0])
        df_resort = BM_table.preprocess_data(df=df_resort,
            resort = "Bald Mountain",
            location = "CO")
        lst_resorts.append(df_resort)

        # Beaver Creek
        df_resort = BC_table.make_dataframe(self.resorts["Beaver Creek"][0])
        df_resort = BC_table.preprocess_data(df=df_resort,
            resort = "Beaver Creek",
            location = "CO")
        lst_resorts.append(df_resort)

        # Diamond Peak
        df_resort = DP_table.make_dataframe(self.resorts["Diamond Peak"][0])
        df_resort = DP_table.preprocess_data(df=df_resort,
            resort = "Diamond Peak",
            location = "CO")
        lst_resorts.append(df_resort)

        # Loveland
        df_resort = loveland_table.make_dataframe(self.resorts["Loveland"][0])
        df_resort = loveland_table.preprocess_data(df=df_resort,
            resort = "Loveland",
            location = "CO")
        lst_resorts.append(df_resort)

        # TODO: Debug Monarch script
        # for resort in self.monarch_script:
        #     df_resort = monarch_table.make_dataframe("../data/Vail.txt")
        #     df_resort = monarch_table.preprocess_data(df=df_resort,
        #         resort = "Monarch",
        #         location = "CO")
        #     lst_resorts.append(df_resort)

        # Steamboat
        df_resort = steamboat_table.make_dataframe(self.resorts["Steamboat"][0])
        df_resort = steamboat_table.preprocess_data(df=df_resort,
            resort = "Steamboat",
            location = "CO")
        lst_resorts.append(df_resort)
        
        # Vail
        df_resort = vail_table.make_dataframe(self.resorts["Vail"][0])
        df_resort = vail_table.preprocess_data(df=df_resort,
            resort = "Vail",
            location = "CO")
        lst_resorts.append(df_resort)

        # Winter Park
        colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'horiz_dist', 'slope_length_(ft)', 'avg_grade_(%)', 'plan_acres', 'slope_area_(acres)', 'deg_grade', 'max_grade_(%)', 'avg_width_(ft)', 'ability_level']
        df_resort = pd.read_csv(self.resorts["Winter Park"][0],
            header=None,
            names=colnames)
        df_resort = WP_table.preprocess_data(df=df_resort,
            resort="Winter Park",
            location="CO")
        lst_resorts.append(df_resort)        
        
        # Wolf Creek
        df_resort = WC_table.make_dataframe(self.resorts["Wolf Creek"][0])
        df_resort = WC_table.preprocess_data(df=df_resort,
            resort = "Wolf Creek",
            location = "CO")
        lst_resorts.append(df_resort)
        
        columns = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)',
                   'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level', 'resort', 'location']

        # Combine DataFrames
        whole_table = pd.concat(lst_resorts)
        
        # Ensure columns are in the correct order
        whole_table = whole_table[columns]
        CO_resorts = whole_table[whole_table['location'] == 'CO']

        CO_resorts = CO_resorts.reset_index(drop=True)

        return CO_resorts

    def standardize_ability_levels(self, df):
        """
        Standardize ability levels across all resorts
        """

        dict_ability_levels = {"Advanced Intermediate": "Advanced",
                               "Adv. Intermediate": "Advanced",
                               "Gladed Adv Inter": "Advanced",
                               "Hike To": "Expert",
                               "Hike to": "Expert",
                               "Hike-To": "Expert",
                               "Gladed Expert": "Expert",
                               "Exp Bowl": "Expert",
                               "Expert Glade-Gated": "Expert",
                               "Chute/Bowl-Gated": "Expert",
                               "Bowl/Glade-Gated": "Expert",
                               "Chute/Glade-Gated": "Expert",
                               "Intermediate Glade": "Intermediate"}

        # Map values; fill with original value if new value doesn't exist
        df["ability_level"] = df["ability_level"].map(dict_ability_levels).fillna(df["ability_level"])

        return df

    def fix_trail_names(self, df):
        '''
        Inputs:
            df from trail_names_to_fix (DataFrame)
        Outputs:
            df w/ trail name fixed - removing number at beginning (DataFrame)
        '''
        df['trail_name'] = df['trail_name'].apply(
            lambda x: ' '.join(x.split()[1:]))
        return df

    def add_groomed_col(self, df, groomed_lst):
        '''  
        Inputs:
            df: resort_df from resort_dfs (DataFrame)
            groomed_lst: from grooms (list)
        Outputs:
            resort_df w/ groomed column added (DataFrame)
        '''
        df['groomed'] = 0
        df['groomed'][df['trail_name'].isin(groomed_lst)] = 1
        return df

if __name__ == '__main__':

    combine = CombineTables()
    
    df_resorts = combine.format_resorts()

    df_resorts = combine.standardize_ability_levels(df=df_resorts)

    # Fix trail names (remove numbers at beginning)
    df_resorts = combine.fix_trail_names(df=df_resorts)

    # TODO: Missing trails

    # TODO: List of trails


    """
    Create dictionary of resorts and groomed ski runs
    """

    dict_groomed_runs = {
        
        "Alpine Meadows": ['Alpine Bowl', 'Bobby’s Run','Charity','D-8','Dance Floor','East Creek','Ladies Slalom','Lakeview to Weasel','Leisure Lane',
                    'Loop Road','Maid Marian', 'Meadow Run','Mountain View','Nick’s Run','Outer Limits','Ray’s Rut','Reily’s Run',
                    'Return Road','Rock Garden','Sandy’s Corner','Scott Ridge Run','Sherwood Run','Shooting Star','Subway Run',
                    'Summer Road','Sun Spot','Teaching Terrain','Terry’s Return','Twilight Zone','Weasel Run','Werner’s Schuss',
                    'Winter Road','Wolverine','Yellow Trail'],

        "Arapahoe Basin": ['Carpet II','Chisholm','Chisholm Trail','Columbine','Cornice Run I','Cornice Run II',"Dercum's Gulch",'Falcon',
                    'Grizzly Road','High Noon','Humbug','Independence','Knolls','Larkspur','Lenawee Face','Lenawee Parks',
                    'Molly Hogan 1','Molly Hogan 2','Molly Hogan Upper',"Molly's Magic Carpet",'Norway Face','Powerline',
                    'Shining Light','Sundance','West Gully','West Wall','Wrangler Lower','Wrangler Middle','Wrangler Upper'],

        "Aspen Snowmass": [],

        "Bald Mountain": ['Upper College', 'Lower College', 'Lower River Run', 'Mid River Run', 'Olympic Lane/Ridge', 'Lower Olympic', 'Cut-Off',
                'Blue Grouse', 'Canyon', 'Lower Warm Springs', 'Warm Springs Face', 'Upper Flying Squirrel', 'Lower Flying Squirrel',
                'Hemingway', "Lower Picabo's Street", 'Cozy', 'Greyhawk'],

        "Beaver Creek": ['Leav the Beav', 'Sawbuck', 'Grubstake', "Gunder's", 'Roughlock', 'Redtail', 'Primrose', 'Larkspur', '1876',
                'Bear Trap', 'Centennial', 'Buckboard', 'C Prime', 'Intertwine', 'Stacker_lower', 'Red Buffalo', 'Stirrup',
                'Cresta', 'Golden Bear', 'Little Brave', 'Cabin Fever', 'Springtooth', 'BC Mtn Expressway', 'Bluebell',
                'Dally', 'Haymeadow', 'Harrier', 'Latigo', 'Stone Creek Meadows', 'Bitterroot', 'Booth Gardens', 'Beginner Terrain',
                'Chair 2', 'Yarrow', 'Bridle', 'Cinch', 'Assay', 'Piney', 'Powell', 'Upper Sheephorn'],

        "Copper": ['American Flyer',  "Andy's Encore",'Bittersweet','Bouncer','Clear  Cut','Clear Cut','Collage','Copperopolis',
                    'Coppertone','Easy Rider','Easy Road Too','Fair Play','Foul Play','Gem','Green Acres','Hidden Vein','I-Way',
                    'Lower Carefree',"Lower Easy Feelin'",'Lower Easy Road Traverse','Lower High Point','Lower Loverly','Lower Roundabout',
                    'Lower Sluice','Lower Soliloquy','Main Vein','Middle High Point','Middle Roundabout','Minor Matter','Oh No','Otto Bahn',
                    'Ptarmigan','Rattler','Rhapsody',"Rosi's Run",'Rugrat','Scooter','Skid Road','Slingshot','The Glide','The Moz','Triple Zero',
                    'Union Park','Upper Carefree',"Upper Easy Feelin'",'Upper Easy Road Traverse','Upper High Point','Upper Leap Frog','Upper Lillie G',
                    'Upper Roundabout','Upper Skid Road','Upper Soliloquy','Vein Glory','Windsong','Woodwinds','Woodwinds Traverse'],

        "Crested Butte": ['Keystone Lower', 'Roller Coaster', 'Peanut', 'Houston', 'Warming House Hill', 'Kubler', "Big Al’s", 'Smith Hill Lower',
                'Smith Hill Upper', 'Twister Lower', 'Mineral Point', 'Poverty Gulch', 'North Star', 'Silver Queen Road', 'Keystone Upper',
                'Upper Park', 'Augusta', 'High Tide', "Rustler’s Gulch", 'Cascade', 'North Pass', 'Gunsight Pass', "Panion’s Run",
                'Buckley', "Splain's Gulch", 'Homeowners', 'Deer Pass', 'Prospector', 'Lower Gallowich', 'Gallowich Upper', 'Black Eagle',
                'Daisy', 'Treasury Lower', 'Treasury Upper', 'Conundrum', "Bubba’s Shortcut Upper", "Bubba’s Shortcut Lower", 'Bushwacker',
                'Gus Way', 'Ruby Chief Lower', 'Ruby Chief Upper', 'Paradise Bowl', 'Forest Queen', 'Yellow Brick Road', 'Teaching Terrain',
                'International'],

        "Diamond Peak": ['Crystal Ridge', 'The Great Flume', 'Spillway', 'Sunnyside', "Luggi's", 'Freeway', 'Penguin', 'Ridge Run',
                'Chute', 'Upper Show-off', 'Lower Show-off', "Dusty's Delight", 'Popular', 'Lodgepole', 'School Yard'],

        "Eldora": ['Around the Horn','Bonanza','Bunnyfair','Challenge','Challenge Liftline','Chute','Corkscrew','Corona','Corona Road','Corona TRV',
                    'Crewcut','Dream & Scream','Easy Way',"Four O' Clock Trail",'Fox Tail','Ho Hum','Hornblower','Hotdog Alley','International',
                    'Klondike','La Belle Dame','Little Hawk TRV','Lower Ambush','Lower Diamond Back','Lower Jolly Jug',"Mary's Way",'Middle Jolly Jug',
                    'Muleshoe','Pipeline','Quickway','Sidewinder','Snail','Summer Road','Sundance','Sunkid Slope','Sunset','Tenderfoot I',
                    'Tenderfoot II','Upper Bunny Fair','Upper Diamond Back','Wayback','Windmill'],

        "Loveland": ['All Smiles','Apollo (Upper)','Awesome','Boomerang','Cat Walk',"Chet's Run",'Creek Trail','Deuces Wild',
                    'Drifter','Fire Bowl','Forest Meadow','Home Run','Keno','Lower Creek Trail','Magic Carpet Slope','Mambo',
                    'North Turtle Creek','Perfect Bowl',"Richard's Run",'Rookie Road','Roulette','Royal Flush','Scrub','Spillway',
                    'Straight Flush','Switchback (Lower)','Switchback (Upper)','Take Off','Take Off','Tango Road','Telestar',
                    'Tempest','Turtle Creek','Twist (Lower)','Twist (Upper)','Zig-Zag','Zip Trail','Zippity Split'],

        "Monarch": ['G lade', 'Little Joe', 'Lower Tango', 'Rookie', 'Roundabout', 'Sidewinder', 'Sky Walker I', 'Sleepy Hollow',
                'Sky Walker II', 'Snowflake', 'Tenderfoot', 'G reat D ivide', 'Freeway', 'Little Mo', 'Romp', 'Snow Burn',
                ''],

        "Steamboat": ['B.C. Ski Way', 'Boulevard', 'Lower Broadway', 'Giggle Gulch', 'Park Lane', 'Preview', 'Rendezvous Way', 'Lower Right-O-Way',
                'Mid Right-O-Way', 'Upper Right-O-Way', 'Short Cut', 'Sitz', 'So What', 'South Peak Flats', 'Spur Run Road', 'Spur Run Face',
                'Sundial', 'Swinger', 'Upper Why Not', 'Mid Why Not', 'Lower Why Not', 'Upper Yoo Hoo', 'Mid Yoo Hoo', 'Baby Powder gladed',
                'Bashor Terrain Park', 'Betwixt', 'Blizzard', 'Buckshot', "Buddy's Run", 'Calf Roper', 'Lower Cowboy Coffee', 'Upper Cowboy Coffee',
                'Daybreak', "Eagle's Nest", "Lower Eagle's Nest", 'Flintlock', 'Heavenly Daze', 'Lower High Noon', 'Upper High Noon', 'High Line',
                "Huffman's", "Jess' Cut Off", 'Kit', 'Lightning', 'Main Drag', 'Meadow Lane', 'Moonlight', "One O'Clock", "Over Easy", 'Lower Quickdraw',
                'Upper Quickdraw', 'Lower Rainbow', 'Upper Rainbow', 'Ramrod', 'Rooster', "Ruby's Run", 'Skyline', 'Spike', 'Sunshine Liftline',
                'Upper Tomohawk', 'Lower Tomohawk', 'Tower', 'Tornado Lane', 'Traverse', 'Upper Vagabond', 'Lower Vagabond', 'Velvet', 'Vogue',
                'Flying Z Gulch', 'Longhorn', 'Sunnyside', 'Lights Out Sunset', "Two O'Clock", 'Corridor', 'Drop Out', 'Flying Z', 'Last Chance',
                'Middle Rib', 'Rolex', 'See Me', "Storm Peak Left", "Ted's Ridge", 'Upper Valley View', 'Lower Valley View', 'Voo Doo', 'West Side'],

        "Taos": ['Bambi Glade', 'Rueggli', 'High Five', 'High Five Pitch', 'Strawberry Hill', 'White Feather', 'White Feather (Middle Pitch)',
                'Firlefanz', 'Lower Stauffenberg', 'Mucho Gusto', 'Porcupine', 'Powderhorn Bowl', 'Powderhorn Upper', 'Powderhorn Lower',
                'Powderhorn Gully', 'Upper Powderhorn', 'Bonanza', "Jess's (Lower)", "Jess's (Upper)", 'Bambi', 'West Basin', 'Easy Trip',
                'Honeysuckle', 'Japanese flag', 'Lower Patton', 'Lower Totemoff', 'Winkelreid', 'Baby Bear', 'Lone Star', "Maxie's",
                'Shalako (Upper)', 'Shalako (Lower)', 'Upper Patton', 'Upper Totemoff'],

        "Telluride": ['Meadows', 'Peaks Trail', 'Boomerang Lower', 'Boomerang Upper', 'Butterfly', 'Hoot Brown Expert Terrain Park',
                'Village Bypass', 'Misty Maiden', 'Peak-A-Boo', 'Sheridan Headwall', 'Cakewalk', "South Henry’s", 'Polar Queen',
                'Woozley’s Way Lower', 'Woozley’s Way Upper', 'Milk Run Lower', 'Milk Run Upper', 'Telluride Trail', 'Bail Out',
                'Easy Out', 'Last Chance', 'Lookout Lower', 'Lookout Upper', 'Plunge Upper', 'Bridges', 'Double Cabin', 'Galloping Goose Upper',
                'Galloping Goose Lower', 'Sundance', "Teddy’s Way", 'Beginner Park', 'Little Maude', 'Nellie', 'Magnolia', 'May Girl',
                'UTE Park'],

        "Vail":     ['Avanti Lower', 'Avanti Upper', 'Bear Tree', 'Big Rock Park', 'Boomer', 'Born Free', 'Chopstix',
                    'Columbine', 'Could 9', 'Coyote Crossing', "Dealer's Choice", 'Expresso', 'Flapjack', 'Gopher Hill',
                    'Hunky Dory', 'Lodgepole', 'Lost Boy', 'Mid-Vail Express', 'Northstar', 'Ouzo', 'Overeasy',
                    'Pickeroon', 'Pickeroon Lower', 'Poppyfields West', 'Practice Pkwy', 'Ramshorn', "Ruder's Route",
                    'Showboat', 'Simba Lower', 'Simba Upper', 'Sourdough', 'Swingsville', 'Swingsville Ridge',
                    'Teaching Area', 'The Meadows', 'The Preserve', 'The Star', 'Tin Pants', 'Tin Pants Catwalk',
                    'Whippersnapper', 'Whiskey Jack', 'Whiskey Jack Catwalk', 'Yonder'],       
        
        "Winter Park": ['Allen Phipps', 'Big Valley', "Bill Wilson's Way", 'Bobcat', 'Easy Way', 'Gunbarrel', 'Upper High Lonesome', 'Lower High Lonesome',
                'Hobo Alley', 'Jack Kendrick', 'Upper Lonesome Whistle', 'Low Lonesome Whistle', 'Upper Parkway', 'Turnpike-Parkway Bypass',
                'Village Way - Parkway Bypass', 'Village Way - Upper Parkway', 'March Hare', 'March Hare East', 'Marmot Flats', 'Mock Turtle',
                'Olympia Spur', 'Porcupine', 'Shoo Fly', 'Sorensen Park', 'Tie Siding', 'Turnpike', 'Vista Dome', 'Wagon Trail', 'Whistlestop',
                'Lower White Rabbit', 'Bluebell', 'Buckaroo', "Butch's Breezeway", 'Corona Way', 'Cranmer', 'Upper Cranmer', 'Lower Cranmer',
                'Forget-Me-Not', 'Upper Jabberwocky', 'Jabberwocky', 'Lower Jabberwocky', 'Larry Sale', 'Mary Jane Trail', 'Mary Jane Face',
                'Paintbrush', 'Roundhouse Lower', 'Roundhouse', 'Stagecoach', 'Sundance', 'Tweedle Dee', 'White Rabbit', 'Upper White Rabbit',
                'Upper Cheshire Cat', 'Lower Cheshire Cat', 'Lower Hughes', 'Upper Hughes', 'Hughes to Sale', 'Litter Pierre', 'Sleeper',
                'Village Way - Practice Hill', 'Village Way - Mountain Road', 'Village Way - Cranmer Cutoff', 'Whistle Stop',
                'Village Way - Primrose', 'Village Way - Green Acres'],

        "Wolf Creek": ['A­way', 'Bunny Hop – Lower', 'Bunny Hop – Middle', 'Bunny Hop – Upper', 'Divide Trail', 'Easy Out', 'Kelly Boyce Trail – Lower',
                'Kelly Boyce Trail – Upper', 'Powder Puff – Lower', 'Powder Puff – Upper', 'Nova', "Susan's", 'Turnpike – Lower', 'Turnpike – Upper',
                "Alberta's Trail", 'Bonanza Crossover – Upper', 'Bonanza Crossover – Lower', 'Bonanza Trail', 'Charisma', 'Criss Cross',
                'Legs', 'Coyote Park Trail', 'Muskrat Ramble', 'Navajo Trail – Lower', 'Navajo Trail – Upper', 'Park Avenue', 'Summer Day',
                'Tranquility – Lower', 'Tranquility – Upper', 'Magic Carpet']
                    
                    }

    lst_groomed_runs = list(chain(*dict_groomed_runs.values()))

    df_resorts = combine.add_groomed_col(
        df=df_resorts,
        groomed_lst=lst_groomed_runs)

    """
    Import webscraped data
    """

    df_webscraped_trails = pd.read_csv("../data/formatted/webscrape_trail_data_20200203.csv")

    # Rename resorts
    dict_webscrape_trail_names = {'alpine-meadows': "Alpine Meadows",
                                  'arapahoe-basin': "Arapahoe Basin",
                                  'aspen-snowmass': "Aspen Snowmass",
                                  'bald-mountain': "Bald Mountain",
                                  'beaver-creek-resort': "Beaver Creek",
                                  'copper-mountain-resort': "Copper",
                                  'crested-butte-mountain-resort': "Crested Butte",
                                  'diamond-peak': "Diamond Peak",
                                  'eldora-mountain-resort': "Eldora",
                                  'loveland-ski-area': "Loveland",
                                  'monarch-ski-area': "Monarch",
                                  'steamboat-ski-resort': "Steamboat",
                                  'taos-ski-valley': "Taos",
                                  'telluride-ski-resort': "Telluride",
                                  'vail-ski-resort': "Vail",
                                  'winter-park-resort': "Winter Park",
                                  'wolf-creek-ski-area': "Wolf Creek"}

    df_webscraped_trails["resort_name"] = df_webscraped_trails["resort_name"].map(
        dict_webscrape_trail_names).\
        fillna(df_webscraped_trails["resort_name"])

    df_webscraped_trails.rename(columns={"resort_name": "resort", "Name": "trail_name"}, inplace=True)
    
    # Merge DataFrames
    df_merged = pd.merge(df_resorts, df_webscraped_trails, on=["resort", "trail_name"], how="inner")
    

    # Add ability numbers and color numbers
    ability_levels = {'Beginner': 1, 'Novice': 2, 'Low Intermediate': 3,
                    'Intermediate': 4, 'Advanced': 5, 'Expert': 6, 'Glade': 5}
    colors = {'green': 1, 'blue': 2, 'black': 3, 'double-black': 4}

    df_merged['ability_nums'] = df_merged['ability_level'].map(ability_levels)
    df_merged['color_nums'] = df_merged['difficulty'].map(colors)

    import pdb; pdb.set_trace()

    # Save data to Parquet file
    # df_merged.to_parquet("../data/formatted_resort_data_20200209.parquet", index=False)
    
'''
Dictionary of dictionaries {resort: {level: [trails]}}
For trails that df_resorts, but have slightly different names from the webscraping (by color)
'''
dict_trails_to_add = {}
dict_trails_to_add['Alpine Meadows'] = {'green': ['Meadow Run', 'Subway Run', 'Teaching Terrain'],
                                   'blue': ['Bobby’s Run', 'Maid Marian', 'Nick’s Run', 'Ray’s Rut', 'Reily’s Run',
                                            'Sandy’s Corner', 'Scotty’s Beam', 'Werner’s Schuss', "Terry’s Return"],
                                   'black': ['Peter’s Peril', 'Hidden Knoll’s', 'Promise Land'],
                                   'bb': []}

dict_trails_to_add['Arapahoe Basin'] = {'green': ['Wrangler Lower', 'Wrangler Middle', 'Wrangler Upper', 'Molly Hogan 1', 'Molly Hogan 2', "Molly's Magic Carpet", 'Molly Hogan Upper', 'Carpet II'],
                                   'blue': ['Cornice Run I', 'Cornice Run II', 'T.B. Glade'],
                                   'black': ['Powder Keg Lower', 'Powder Keg Upper'],
                                   'bb': ['13 Cornices Upper', '13 Cornices Lower', 'Roller Coaster', 'West Alley']}

dict_trails_to_add['Beaver Creek'] = {'green': ['Beginner Terrain', 'BC Mtn Expressway', 'Easy Come _Easy Go', 'Elkhorn', 'Haymeadow',
                                           'Holden', 'Leav the Beav', 'Meadows', 'Rubarb', 'Ridge Point', 'Highlands Skiway',
                                           'Primrose'],
                                 'blue': ['Creekside', 'Stacker_lower', 'McCoy', 'Paintbrush', 'West Fall Road', 'Camprobber Road',
                                          'Cabin Fever', 'Wapti'],
                                 'black': ['Boarders Loop', 'Goshawk', 'Harrier', 'Centennial', 'Wapiti', 'S. Star'],
                                 'bb': ['Stone Creek Chutes']}

dict_trails_to_add['Copper'] = {'green': ['Lower Carefree', 'Upper Carefree', "Lower Easy Feelin'", "Upper Easy Feelin'",
                                     'Lower High Point', 'Middle High Point', 'Upper High Point', 'Upper Leap Frog',
                                     'Lower Leap Frog', 'Lower Loverly', 'Middle Loverly', 'Upper Loverly', 'Lower Roundabout',
                                     'Middle Roundabout', 'Upper Roundabout', 'See and Ski', 'Lower Soliloquy', 'Upper Soliloquy',
                                     'West Tenmile', 'Green Acres', 'Gem', 'Rugrat', 'Easy Rider', 'The Glide', 'Slingshot',
                                     'Lower Easy Road Traverse', 'Upper Easy Road Traverse'],
                           'blue': ['Copperfields', 'Upper Skid Road'],
                           'black': ["CDL's", 'Allcante', "Ute Overlook", 'Lower Lillie G', 'Upper Lillie G', 'Retreat'],
                           'bb': []}

dict_trails_to_add['Crested Butte'] = {'green': ['Big Al’s', 'Bubba’s Shortcut Upper', 'Bubba’s Shortcut Lower', 'Keystone Lower',
                                            'Twister Lower', 'Peachtree Connector', 'Smith Hill Lower', 'Teaching Terrain',
                                            'To Base Area', "Rustler’s Gulch", 'Augusta', 'High Tide', 'Topsy', "Splain's Gulch"],
                                  'blue': ['Gus Way', 'Homeowners', 'Treasury Lower', 'Gallowich', 'Panion’s Run', 'Ruby Chief Lower',
                                           'Gallowich Upper', 'Keystone Upper', 'Treasury Upper', 'Tulsa', 'Smith Hill Upper',
                                           'Ruby Chief Upper', 'Bear', 'Meander', 'Paradise Access', 'Little Lizzie'],
                                  'black': ['Silvanite', 'Twister Upper', 'Twister Connector', 'Keystone Ridge', 'Mach 1', 'Peoria',
                                            'Horseshoe'],
                                  'bb': ['Headwall']}

dict_trails_to_add['Diamond Peak'] = {'green': [],
                                 'blue': [],
                                 'black': ['FIS', 'O God', 'GS'],
                                 'bb': []}

dict_trails_to_add['Eldora'] = {'green': ['Upper Bunny Fair', 'Fox Tail', 'Little Hawk TRV', 'Tenderfoot I', 'Tenderfoot II'],
                           'blue': ['Crewcut', 'Corona TRV', "Four O' Clock Trail", 'Middle Jolly Jug',
                                    'Lower Jolly Jug', 'Upper Bunny Fair', 'Quickway', 'Sundance', 'Sunkid Slope'],
                           'black': ['Challenge Liftline', 'Corona Road', 'Klondike', 'Upper Diamond Back'],
                           'bb': ['Upper Jolly Jug', 'Liftline']}

dict_trails_to_add['Loveland'] = {'green': ['Cat Walk', 'Deuces Wild', 'Home Run', 'Zig-Zag', 'Magic Carpet Slope'],
                             'blue': ['Apollo (Lower)', 'Apollo (Upper)', 'Blackjack (Lower)', 'Blackjack (Upper)', 'North Chutes', 'Switchback (Lower)',
                                      'Switchback (Upper)', 'Twist (Lower)', 'Twist (Upper)', "Upper Richard's", 'Tempest', "Chet's Run"],
                             'black': ['Cats Meow', 'Fail Safe Trees I', 'Fail Safe Trees II', 'Sunburst Chutes',
                                       "Hook 'Em Horns"],
                             'bb': ['#4 Headwall', 'Upper #4 Headwall', 'Patrol Bowl (Lower)', 'Patrol Bowl (Upper)']}

dict_trails_to_add['Monarch'] = {'green': ['K C Cutoff', 'Sky Walker I', 'Sky Walker II', 'D rifter', 'G lade', 'Safari'],
                            'blue': ['Bee Line', "D oc’s Run", 'G reat D ivide', 'Q uick D raw', 'Snow Burn', 'Lower Hall’s Alley'],
                            'black': ["B’s Bash", 'D ire Straits', "G eno’s Meadow", "G unbarrel", 'K anonen', 'O utback',
                                      'Upper X mas Tree', 'Upper Hall’s Alley', 'Frazzle'],
                            'bb': ['Mirkwood Basin', 'Mirkwood Basin Egress', ]}

dict_trails_to_add['Taos'] = {'green': ['Japanese flag', "Jess's (Lower)", "Jess's (Upper)", "Winkelreid", 'Bambi Glade',
                                   'Strawberry Hill', 'High Five Pitch', 'Rueggli', 'Zipper 1', 'Zipper 2', 'Zipper 3'],
                         'blue': ["Maxie's", 'Powderhorn Lower', 'Powderhorn Upper', 'Shalako (Lower)', 'Shalako (Upper)',
                                  'Topa Papa'],
                         'black': ['Raspberry Hill'],
                         'bb': ['Lorelei Trees']}

dict_trails_to_add['Vail'] = {'green': ["Cubs Way", 'Eagles Nest Ridge', 'Flapjack', 'Lionsway Cutoff', 'Lower Lionsway',
                                   'Upper Lionsway', 'Minni Ha Ha', 'Practice Pkwy', 'Timberline Catwalk.', 'Transmontane',
                                   'Windish Way', 'Grand Junction Catwalk', 'Teaching Area', 'Tin Pants Catwalk',
                                   'Whiskey Jack Catwalk'],
                         'blue': ['Avanti Lower', 'Avanti Upper', 'China Bowl Egress', 'Choker Cutoff', 'Kellys Toll Road',
                                  'Riva Ridge Lower', 'Mid-Vail Express', 'Ranger Racoon', "Ruder's Route", 'Simba Lower',
                                  'Simba Upper', 'Simba Racer', 'Sleepy Time', 'Berries', 'Pickeroon', 'The Preserve',
                                  'Ledges Lower', 'Ledges Upper', 'Resolultion Upper', 'Expresso', 'Cheetah', 'Bwana Upper',
                                  'Pride Lower', 'Pride Upper', 'Grand Review', 'Resolution Lower', 'Snag Park Lower',
                                  'Snag Park Upper'],
                         'black': ['Dueces Wild', 'Wild Card', 'Genghis Kahn', 'Inner MongoliaBowl', 'Legdes Lower',
                                   'Ledges Upper', 'Lookma', 'South Lookma', 'Lovers Leap', 'Safari', 'Montane Glade',
                                   'North Rim', 'South Rim', 'OS', 'Old 9 Lift Line', 'Outer Mongolia Bowl',
                                   'Shangri-La Glades', 'Shangri-la Glades E', 'Steep and Deep',
                                   'Riva Ridge Upper', "Widge's Ridge", "Windows Trees", 'Berries-Cookshack', 'Powerline Trees',
                                   "Minnie's MileLower", 'Genghis Khan', 'Outer MongoliaBowl', 'Tea Cup Glades'],
                         'bb': ['Front Side Chutes', 'Mud Slide Chutes', 'Prima Lower', 'Prima Upper', 'Pump House Chutes',
                                '']}

dict_trails_to_add['Winter Park'] = {'green': ['Allen Phipps', "Bill Wilson's Way", 'Upper High Lonesome', 'Lower High Lonesome',
                                          'Hook Up', 'Moose Wallow', 'March Hare', 'Wagon Trail', 'Whistle Stop', 'Sorensen Park'],
                                'blue': ['Belmar Bowl', 'Upper Cranmer', 'Lower Cranmer', 'Dilly Dally Alley', 'Forget-Me-Not',
                                         'Upper Jabberwocky', 'Low Lonesome Whistle', 'Mary Jane Trail', "Parry's Peak", 'Primrose Glades',
                                         'Upper Rendezvous', 'Lower Rendezvous', 'Roundhouse Lower', 'Shoot Out', 'Columbine Upper',
                                         'Upper White Rabbit', 'Bellmar Bowl', 'Chuckwagon', 'Lower Cheshire Cat', 'March Hare East'],
                                'black': ['Aces and Eights', "Bradley's Bash", 'Engeldive Cutoff', 'Upper Hughes', 'Iron Horse Trail Upper',
                                          'Iron Horse Trail Middle Upper', 'Iron Horse Trail Middle Lower', 'Iron Horse Trail Lower',
                                          'Johnston Junction', 'Litter Pierre', 'Pioneer Express Trail (Lower)', "Mulligan's Mile",
                                          "Over N' Underwood", "Retta's Run", 'Riflesight Notch', 'Sharp Nose', 'Sleepy Hollow',
                                          'Sleeper Glades', 'Super Gauge Trail (Rock Garden)', 'Mary Jane Face', 'Pioneer Express Trail (Upper)',
                                          'Norwegian', 'Columbine Lower', 'Upper Cheshire Cat', 'Roll Over'],
                                'bb': []}

dict_trails_to_remove = {
    "Arapahoe Basin": ['High Noon Terrain Park','Treeline Terrain Park', 'Shooting Gallery', 'Poma Line'],
    "Beaver Creek": ['Chair 2', 'Half- Barrell Half Pipe', 'Half Hitch', 'Nastar Ski Racing', 'Park101_Flattops',
                       'Utility Corridor', 'Pitchfork', 'Pines Skiway', "Anderson's Alley", 'Homefire', 'Tall Timber',
                       'Ridge Rider'],
    "Copper": ["Bruce's Way", 'Bee Road', 'Road Home', 'Cross Cut'],
    "Crested Butte": ['Gallowitch Bend', 'Silver Queen Connector', 'Aspen Park', "Shep's Chute"],
    "Loveland": ['T-bar Road','Sani Flush', 'Awesome II', 'Rip Curl', ''],
    "Monarch": ['K2', 'Tumbelina Lift Line'],
    "Taos": ['White Feather (Middle Pitch)', 'Raspberry (Pitch 1)', 'Raspberry (Pitch 2)', 'Raspberry (Pitch 3)',
                      'Raspberry Hill Traverse', 'Top of Lifts 2 and 6', 'Lorelei Egress', 'Hunziker Egress', 'Lift 6 Liftline',
                      'Avy Road', 'Maidenform'],
    "Vail": ['Avanti-Cookshack', 'Chair 2 Lift Line', 'Pickeroon Lower', 'Pickeroon-Cookshack', 'Ricochet',
                      'Mountain Top Lift Line', 'Ramshorn Glade', 'Swingsville Ridge', 'Apres Trees East', 'Apres Trees West',
                      'Ho Chi Min Trail', 'Ptarmigan Cornice', "Sama's", 'Turkey Yard', 'Aspen Alley', 'Chair 6 Lift Line', 'Follow Me Road',
                      'Mule Skinner', 'Pony Express', 'Faro Glade', 'Old Midway Catwalk', "Minnie's Cutoff", "Minnie's Mile Upper",
                      "Minnie's Mile Upper Face", 'Hairbag Alley Lower', 'International', 'Mid-Vail Milling Area', 'Villages Catwalk',
                      'Vista Bahn Line Upper', 'Way Over Yonder', 'Gondola Lift Line', 'Simba Face', 'Cascade Way', 'China Wall', 'to Two Elk',
                      'West Wall', 'Upper MongoliaBowl', 'Bwama-Simba Collector', 'Cubs Way Upper', 'Pride Upper Face', 'Black Forest Milling Area',
                      'Nastar', 'Pay-to-Race', 'East Tea Cup', 'Petes Lift Line', 'Berries Catwalk', 'Ch 10 Access', 'Lift Line', "Roger's Glade",
                      "Smokey's", 'Timberline Face', 'Minnies Mile Upper Face'],
    "Winter Park": ['Meadows', 'Nirvana', 'Village Way - Primrose'],
    "Wolf Creek": ['Meadows', 'Nirvana', 'Village Way - Primrose']
}


def remove_trails(resort_dict, resort, trail_lst):
    '''
    Remove trails with no data other than master plan

    Inputs:
        resort from resort_dict (str)
        trail_lst from trails_to_remove (list)
    Outputs:
        Pandas DataFrame with trails removed
    '''
    resort_df_new = resort_dict[resort][~resort_dict[resort]
                                        ['trail_name'].isin(trail_lst)]
    return resort_df_new


# for resort, trail_lst in zip(resort_dict, trails_to_remove):
#     resort_dict[resort] = remove_trails(resort, trail_lst)

# TODO: Fix Monarch trail names?
# lst_monarch_trails = ['Quick Draw', 'KC Cutoff', "Doc's Run", 'Dire Straits', 'Great Divide', "Geno's Meadow"]
# "Litter Pierre"


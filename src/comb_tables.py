import pickle
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .create_tables import (BC_table, DP_table, WP_table, loveland_table,
                            monarch_table, vail_table)

warnings.filterwarnings('ignore')


class CombineTables:

    def __init__(self):
        self.resorts = {'Loveland': ['../data/Loveland.txt', 'CO'],
                        'Arapahoe Basin': ['../data/Arapahoe_Basin.txt', 'CO'],
                        'Copper': ['../data/Copper.txt', 'CO'],
                        'Eldora': ['../data/Eldora.txt', 'CO'],
                        'Alpine Meadows': ['../data/Alpine_Meadows.txt', 'CA'],
                        'Vail': ['../data/Vail.txt', 'CO'],
                        'Monarch': ['../data/Monarch.txt', 'CO'],
                        'Crested Butte': ['../data/Crested_Butte.txt', 'CO'],
                        'Taos': ['../data/Taos.txt', 'NM'],
                        'Diamond Peak': ['../data/DP.txt', 'NV'],
                        'Winter Park': ['../data/WP.csv', 'CO'],
                        'Beaver Creek': ['../data/Beaver_Creek.txt', 'CO'],
                        'Telluride': ['../data/new/Telluride.txt', 'CO'],
                        'Bald Mountain': ['../data/new/Bald_Mountain.txt', 'CO'],
                        'Steamboat': ['../data/new/Steamboat.txt', 'CO'],
                        'Aspen Snowmass': ['../data/new/Aspen_Snowmass.txt', 'CO'],
                        'Wolf Creek': ['../data/new/Wolf_Creek.txt', 'CO']}

        # Keys of resorts compatible with each script
        self.BC_script = ['Beaver Creek']
        self.DP_script = ['Diamond Peak']
        self.loveland_script = [
            'Loveland', 'Arapahoe Basin', 'Copper', 'Eldora', 'Alpine Meadows']
        self.monarch_script = ['Monarch', 'Crested Butte', 'Taos']
        self.vail_script = ['Vail']
        self.WP_script = ['Winter Park']

        # comb_tables2 scripts
        self.loveland_script = ['Telluride']
        self.BM_script = ['Bald Mountain']
        self.steamboat_script = ['Steamboat']
        self.AS_script = ['Aspen Snowmass']
        self.WC_script = ['Wolf Creek']

    def format_resorts(self):
        """
        """

        #TODO:: Create list of resorts; iterate through this.
        d = {}
        for resort in self.loveland_script:
            filename, location = self.resorts[resort]
            d[resort] = loveland_table.fix_dtype(
                filename, resort, location)
        for resort in self.vail_script:
            filename, location = self.resorts[resort]
            d[resort] = vail_table.fix_dtype(
                filename, resort, location)
            # del d[resort]['horiz_length']
        for resort in self.monarch_script:
            filename, location = self.resorts[resort]
            d[resort] = monarch_table.fix_dtype(
                filename, resort, location)
            # del d[resort]['plan_length']
        for resort in self.DP_script:
            filename, location = self.resorts[resort]
            d[resort] = DP_table.fix_dtype(
                filename, resort, location)
            # d[resort].drop(['plan_length', 'pct_inc',
            #                 'plan_area'], axis=1, inplace=True)
        for resort in self.WP_script:
            filename, location = self.resorts[resort]
            d[resort] = WP_table.fix_dtype(
                filename, resort, location)
        for resort in self.BC_script:
            filename, location = self.resorts[resort]
            d[resort] = BC_table.fix_dtype(
                filename, resort, location)

        # comb_tables2 script
        for resort in loveland_script:
            filename, location = resorts[resort]
            d[resort] = loveland_table.fix_dtype(
                filename, resort, location)
        for resort in BM_script:
            filename, location = resorts[resort]
            d[resort] = BM_table.fix_dtype(filename, resort, location)
        for resort in steamboat_script:
            filename, location = resorts[resort]
            d[resort] = steamboat_table.fix_dtype(
                filename, resort, location)
        for resort in AS_script:
            filename, location = resorts[resort]
            d[resort] = AS_table.fix_dtype(filename, resort, location)
        for resort in WC_script:
            filename, location = resorts[resort]
            d[resort] = WC_table.fix_dtype(filename, resort, location)
            del d[resort]['plan_length']



        columns = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)',
                   'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level', 'resort', 'location']

        whole_table = pd.concat(d.values())
        # making sure the columns are in the correct order
        whole_table = whole_table[columns]
        CO_resorts = whole_table[whole_table['location'] == 'CO']

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

        df["ability_level"] = df["ability_level"].map(dict_ability_levels)

        # ### from my ipython notebook
        # # standardizing the ability levels
        # whole_table['ability_level'][whole_table['ability_level'] == 'Advanced Intermediate'] = 'Advanced'
        # whole_table['ability_level'][whole_table['ability_level'] == 'Adv. Intermediate'] = 'Advanced'
        # whole_table['ability_level'][whole_table['ability_level'] == 'Hike To'] = 'Expert'
        # whole_table['ability_level'][whole_table['ability_level'] == 'Exp Bowl'] = 'Expert'


"""
Separate resorts into independent DataFrames
"""
loveland = whole_table[whole_table['resort'] == 'Loveland']
AB = whole_table[whole_table['resort'] == 'Arapahoe Basin']
copper = whole_table[whole_table['resort'] == 'Copper']
eldora = whole_table[whole_table['resort'] == 'Eldora']
AM = whole_table[whole_table['resort'] == 'Alpine Meadows']
vail = whole_table[whole_table['resort'] == 'Vail']
monarch = whole_table[whole_table['resort'] == 'Monarch']
CB = whole_table[whole_table['resort'] == 'Crested Butte']
taos = whole_table[whole_table['resort'] == 'Taos']
DP = whole_table[whole_table['resort'] == 'Diamond Peak']
WP = whole_table[whole_table['resort'] == 'Winter Park']
BC = whole_table[whole_table['resort'] == 'Beaver Creek']
telluride = whole_table[whole_table['resort'] == 'Telluride']
BM = whole_table[whole_table['resort'] == 'Bald Mountain']
steamboat = whole_table[whole_table['resort'] == 'Steamboat']
AS = whole_table[whole_table['resort'] == 'Aspen Snowmass']
WC = whole_table[whole_table['resort'] == 'Wolf Creek']


resort_dfs = [loveland, AB, copper, eldora,
              AM, vail, monarch, CB, taos, DP, WP, BC,
              telluride, BM, steamboat, AS, WC]


'''fixing trail names'''
trail_names_to_fix = [copper, AM, vail, monarch, CB, taos, DP, eldora]


def fix_trail_names(df):
    '''
    Inputs:
    df from trail_names_to_fix (DataFrame)
    Outputs:
    df w/ trail name fixed - removing number at beginning (DataFrame)
    '''
    df['trail_name'] = df['trail_name'].apply(
        lambda x: ' '.join(x.split()[1:]))
    return df


for trail in trail_names_to_fix:
    fix_trail_names(trail)
copper['trail_name'] = copper['trail_name'].apply(
    lambda x: ' '.join([i for i in x.split() if i[0].isnumeric() == False]))


'''groomed runs'''
# TODO: Sort names of each list of runs
# TODO: Create dictionary of resort to ski runs?
groomed_LL = ['Take Off', 'Cat Walk', 'Mambo', 'Home Run', 'Spillway', 'Tempest', 'Tango Road', 'Turtle Creek', "Richard's Run",
              'Fire Bowl', 'North Turtle Creek', 'Drifter', 'Switchback (Lower)', 'Switchback (Upper)', 'Boomerang',
              'Zig-Zag', 'Twist (Lower)', 'Twist (Upper)', 'Creek Trail', 'Lower Creek Trail', 'Perfect Bowl', 'Scrub',
              'Apollo (Upper)', 'Telestar', 'Deuces Wild', 'Forest Meadow', 'Roulette', 'Keno', 'Royal Flush', 'Straight Flush',
              'Take Off', 'All Smiles', 'Zip Trail', 'Zippity Split', "Chet's Run", 'Awesome', 'Rookie Road', 'Magic Carpet Slope']

groomed_AB = ['Wrangler Lower', 'Wrangler Middle', 'Wrangler Upper', 'Chisholm', 'Chisholm Trail', 'Sundance',
              'Molly Hogan Upper', 'High Noon', 'Lenawee Face', 'Humbug', 'Powerline', 'West Wall', 'Grizzly Road',
              'Lenawee Parks', "Dercum's Gulch", 'Norway Face', 'Cornice Run I', 'Cornice Run II', 'West Gully', 'Knolls',
              'Falcon', 'Larkspur', 'Independence', 'Columbine', 'Shining Light', 'Molly Hogan 1', 'Molly Hogan 2',
              "Molly's Magic Carpet", 'Carpet II']

groomed_c = ['Lower Easy Road Traverse', 'Upper Easy Road Traverse', 'Upper Leap Frog', 'Bittersweet',
             'Bouncer', 'Fair Play', 'Foul Play', 'Main Vein', 'Rhapsody', 'Coppertone', 'Easy Road Too', 'Lower High Point',
             'Middle High Point', 'Upper High Point', 'Woodwinds', 'Woodwinds Traverse', 'Otto Bahn', 'Rattler', 'Ptarmigan',
             'Green Acres', 'Lower Roundabout', 'Upper Roundabout', 'Middle Roundabout', 'Clear  Cut', 'Lower Sluice', 'Union Park',
             'Triple Zero', 'Upper Lillie G', "Andy's Encore", 'Collage', 'Oh No', 'Skid Road', 'Upper Skid Road', "Rosi's Run",
             'I-Way', 'Minor Matter', 'Lower Soliloquy', 'Upper Soliloquy', 'American Flyer', 'The Moz', 'Windsong', 'Lower Carefree',
             'Upper Carefree', "Lower Easy Feelin'", "Upper Easy Feelin'", 'Hidden Vein', 'Vein Glory', 'Lower Loverly', 'Scooter',
             'Gem', 'Easy Rider', 'Rugrat', 'The Glide', 'Slingshot', 'Clear Cut', 'Copperopolis']

groomed_e = ['Tenderfoot I', 'Tenderfoot II', 'Ho Hum', 'Easy Way', 'Bunnyfair', 'Fox Tail', 'Snail', 'Quickway', 'Sundance',
             'Upper Bunny Fair', 'Corkscrew', 'Little Hawk TRV', 'Bonanza', 'Chute', 'Sunkid Slope', 'Middle Jolly Jug',
             'Lower Jolly Jug', "Mary's Way", 'Summer Road', 'Sunset', 'Challenge', 'Challenge Liftline', 'Crewcut', 'Hornblower',
             'Hotdog Alley', 'International', 'Klondike', 'Windmill', 'Corona Road', 'La Belle Dame', 'Corona TRV', 'Dream & Scream',
             "Four O' Clock Trail", 'Lower Ambush', 'Lower Diamond Back', 'Sidewinder', 'Upper Diamond Back', 'Around the Horn',
             'Corona', 'Muleshoe', 'Pipeline', 'Wayback']

groomed_AM = ['East Creek', 'Weasel Run', 'Lakeview to Weasel', "Nick’s Run", 'Leisure Lane', 'Outer Limits', 'Shooting Star',
              'Twilight Zone', 'Meadow Run', 'Charity', 'Dance Floor', 'Rock Garden', "Sandy’s Corner", "Werner’s Schuss",
              "Bobby’s Run", 'Winter Road', 'Summer Road', 'Maid Marian', "Ray’s Rut", "Reily’s Run", 'Sherwood Run',
              'Return Road', 'Subway Run', 'Alpine Bowl', "Loop Road", 'Sun Spot', 'Wolverine', 'D-8', 'Teaching Terrain',
              "Yellow Trail", 'Ladies Slalom', "Scott Ridge Run", "Mountain View", 'Terry’s Return']

groomed_v = ['Boomer', 'Flapjack', 'Gopher Hill', 'Northstar', "Ruder's Route", 'Sourdough', 'Tin Pants', 'Tin Pants Catwalk',
             'Whippersnapper', 'Whiskey Jack', 'Whiskey Jack Catwalk', 'Avanti Lower', 'Avanti Upper', 'Bear Tree', 'Expresso',
             'Hunky Dory', 'Mid-Vail Express', 'Overeasy', 'Ramshorn', 'Swingsville', 'The Meadows', 'Swingsville Ridge', 'Born Free',
             'Columbine', "Dealer's Choice", 'Lost Boy', 'Lodgepole', 'Ouzo', 'Pickeroon', 'Pickeroon Lower', 'Practice Pkwy',
             'Simba Lower', 'Simba Upper', 'The Preserve', 'Yonder', 'Chopstix', 'Poppyfields West', 'Big Rock Park', 'Could 9',
             'The Star', 'Coyote Crossing', 'Showboat', 'Teaching Area']

groomed_m = ['G lade', 'Little Joe', 'Lower Tango', 'Rookie', 'Roundabout', 'Sidewinder', 'Sky Walker I', 'Sleepy Hollow',
             'Sky Walker II', 'Snowflake', 'Tenderfoot', 'G reat D ivide', 'Freeway', 'Little Mo', 'Romp', 'Snow Burn',
             '']

groomed_CB = ['Keystone Lower', 'Roller Coaster', 'Peanut', 'Houston', 'Warming House Hill', 'Kubler', "Big Al’s", 'Smith Hill Lower',
              'Smith Hill Upper', 'Twister Lower', 'Mineral Point', 'Poverty Gulch', 'North Star', 'Silver Queen Road', 'Keystone Upper',
              'Upper Park', 'Augusta', 'High Tide', "Rustler’s Gulch", 'Cascade', 'North Pass', 'Gunsight Pass', "Panion’s Run",
              'Buckley', "Splain's Gulch", 'Homeowners', 'Deer Pass', 'Prospector', 'Lower Gallowich', 'Gallowich Upper', 'Black Eagle',
              'Daisy', 'Treasury Lower', 'Treasury Upper', 'Conundrum', "Bubba’s Shortcut Upper", "Bubba’s Shortcut Lower", 'Bushwacker',
              'Gus Way', 'Ruby Chief Lower', 'Ruby Chief Upper', 'Paradise Bowl', 'Forest Queen', 'Yellow Brick Road', 'Teaching Terrain',
              'International']

groomed_t = ['Bambi Glade', 'Rueggli', 'High Five', 'High Five Pitch', 'Strawberry Hill', 'White Feather', 'White Feather (Middle Pitch)',
             'Firlefanz', 'Lower Stauffenberg', 'Mucho Gusto', 'Porcupine', 'Powderhorn Bowl', 'Powderhorn Upper', 'Powderhorn Lower',
             'Powderhorn Gully', 'Upper Powderhorn', 'Bonanza', "Jess's (Lower)", "Jess's (Upper)", 'Bambi', 'West Basin', 'Easy Trip',
             'Honeysuckle', 'Japanese flag', 'Lower Patton', 'Lower Totemoff', 'Winkelreid', 'Baby Bear', 'Lone Star', "Maxie's",
             'Shalako (Upper)', 'Shalako (Lower)', 'Upper Patton', 'Upper Totemoff']

groomed_DP = ['Crystal Ridge', 'The Great Flume', 'Spillway', 'Sunnyside', "Luggi's", 'Freeway', 'Penguin', 'Ridge Run',
              'Chute', 'Upper Show-off', 'Lower Show-off', "Dusty's Delight", 'Popular', 'Lodgepole', 'School Yard']

groomed_WP = ['Allen Phipps', 'Big Valley', "Bill Wilson's Way", 'Bobcat', 'Easy Way', 'Gunbarrel', 'Upper High Lonesome', 'Lower High Lonesome',
              'Hobo Alley', 'Jack Kendrick', 'Upper Lonesome Whistle', 'Low Lonesome Whistle', 'Upper Parkway', 'Turnpike-Parkway Bypass',
              'Village Way - Parkway Bypass', 'Village Way - Upper Parkway', 'March Hare', 'March Hare East', 'Marmot Flats', 'Mock Turtle',
              'Olympia Spur', 'Porcupine', 'Shoo Fly', 'Sorensen Park', 'Tie Siding', 'Turnpike', 'Vista Dome', 'Wagon Trail', 'Whistlestop',
              'Lower White Rabbit', 'Bluebell', 'Buckaroo', "Butch's Breezeway", 'Corona Way', 'Cranmer', 'Upper Cranmer', 'Lower Cranmer',
              'Forget-Me-Not', 'Upper Jabberwocky', 'Jabberwocky', 'Lower Jabberwocky', 'Larry Sale', 'Mary Jane Trail', 'Mary Jane Face',
              'Paintbrush', 'Roundhouse Lower', 'Roundhouse', 'Stagecoach', 'Sundance', 'Tweedle Dee', 'White Rabbit', 'Upper White Rabbit',
              'Upper Cheshire Cat', 'Lower Cheshire Cat', 'Lower Hughes', 'Upper Hughes', 'Hughes to Sale', 'Litter Pierre', 'Sleeper',
              'Village Way - Practice Hill', 'Village Way - Mountain Road', 'Village Way - Cranmer Cutoff', 'Whistle Stop',
              'Village Way - Primrose', 'Village Way - Green Acres']

groomed_BC = ['Leav the Beav', 'Sawbuck', 'Grubstake', "Gunder's", 'Roughlock', 'Redtail', 'Primrose', 'Larkspur', '1876',
              'Bear Trap', 'Centennial', 'Buckboard', 'C Prime', 'Intertwine', 'Stacker_lower', 'Red Buffalo', 'Stirrup',
              'Cresta', 'Golden Bear', 'Little Brave', 'Cabin Fever', 'Springtooth', 'BC Mtn Expressway', 'Bluebell',
              'Dally', 'Haymeadow', 'Harrier', 'Latigo', 'Stone Creek Meadows', 'Bitterroot', 'Booth Gardens', 'Beginner Terrain',
              'Chair 2', 'Yarrow', 'Bridle', 'Cinch', 'Assay', 'Piney', 'Powell', 'Upper Sheephorn']

groomed_t = ['Meadows', 'Peaks Trail', 'Boomerang Lower', 'Boomerang Upper', 'Butterfly', 'Hoot Brown Expert Terrain Park',
             'Village Bypass', 'Misty Maiden', 'Peak-A-Boo', 'Sheridan Headwall', 'Cakewalk', "South Henry’s", 'Polar Queen',
             'Woozley’s Way Lower', 'Woozley’s Way Upper', 'Milk Run Lower', 'Milk Run Upper', 'Telluride Trail', 'Bail Out',
             'Easy Out', 'Last Chance', 'Lookout Lower', 'Lookout Upper', 'Plunge Upper', 'Bridges', 'Double Cabin', 'Galloping Goose Upper',
             'Galloping Goose Lower', 'Sundance', "Teddy’s Way", 'Beginner Park', 'Little Maude', 'Nellie', 'Magnolia', 'May Girl',
             'UTE Park']

groomed_BM = ['Upper College', 'Lower College', 'Lower River Run', 'Mid River Run', 'Olympic Lane/Ridge', 'Lower Olympic', 'Cut-Off',
              'Blue Grouse', 'Canyon', 'Lower Warm Springs', 'Warm Springs Face', 'Upper Flying Squirrel', 'Lower Flying Squirrel',
              'Hemingway', "Lower Picabo's Street", 'Cozy', 'Greyhawk']

groomed_s = ['B.C. Ski Way', 'Boulevard', 'Lower Broadway', 'Giggle Gulch', 'Park Lane', 'Preview', 'Rendezvous Way', 'Lower Right-O-Way',
             'Mid Right-O-Way', 'Upper Right-O-Way', 'Short Cut', 'Sitz', 'So What', 'South Peak Flats', 'Spur Run Road', 'Spur Run Face',
             'Sundial', 'Swinger', 'Upper Why Not', 'Mid Why Not', 'Lower Why Not', 'Upper Yoo Hoo', 'Mid Yoo Hoo', 'Baby Powder gladed',
             'Bashor Terrain Park', 'Betwixt', 'Blizzard', 'Buckshot', "Buddy's Run", 'Calf Roper', 'Lower Cowboy Coffee', 'Upper Cowboy Coffee',
             'Daybreak', "Eagle's Nest", "Lower Eagle's Nest", 'Flintlock', 'Heavenly Daze', 'Lower High Noon', 'Upper High Noon', 'High Line',
             "Huffman's", "Jess' Cut Off", 'Kit', 'Lightning', 'Main Drag', 'Meadow Lane', 'Moonlight', "One O'Clock", "Over Easy", 'Lower Quickdraw',
             'Upper Quickdraw', 'Lower Rainbow', 'Upper Rainbow', 'Ramrod', 'Rooster', "Ruby's Run", 'Skyline', 'Spike', 'Sunshine Liftline',
             'Upper Tomohawk', 'Lower Tomohawk', 'Tower', 'Tornado Lane', 'Traverse', 'Upper Vagabond', 'Lower Vagabond', 'Velvet', 'Vogue',
             'Flying Z Gulch', 'Longhorn', 'Sunnyside', 'Lights Out Sunset', "Two O'Clock", 'Corridor', 'Drop Out', 'Flying Z', 'Last Chance',
             'Middle Rib', 'Rolex', 'See Me', "Storm Peak Left", "Ted's Ridge", 'Upper Valley View', 'Lower Valley View', 'Voo Doo', 'West Side']

groomed_AS = []

groomed_WC = ['A­way', 'Bunny Hop – Lower', 'Bunny Hop – Middle', 'Bunny Hop – Upper', 'Divide Trail', 'Easy Out', 'Kelly Boyce Trail – Lower',
              'Kelly Boyce Trail – Upper', 'Powder Puff – Lower', 'Powder Puff – Upper', 'Nova', "Susan's", 'Turnpike – Lower', 'Turnpike – Upper',
              "Alberta's Trail", 'Bonanza Crossover – Upper', 'Bonanza Crossover – Lower', 'Bonanza Trail', 'Charisma', 'Criss Cross',
              'Legs', 'Coyote Park Trail', 'Muskrat Ramble', 'Navajo Trail – Lower', 'Navajo Trail – Upper', 'Park Avenue', 'Summer Day',
              'Tranquility – Lower', 'Tranquility – Upper', 'Magic Carpet']

grooms = [groomed_LL, groomed_AB, groomed_c, groomed_e, groomed_AM, groomed_v,
          groomed_m, groomed_CB, groomed_t, groomed_DP, groomed_WP, groomed_BC,
          groomed_BM, groomed_s, groomed_AS, groomed_WC]


'''adding groomed column'''


def add_groomed_col(df, groomed_lst):
    '''  
    Inputs:
    resort_df from resort_dfs (DataFrame)
    groomed_lst from grooms (list)
    Outputs:
    resort_df w/ groomed column added (DataFrame)
    '''
    df['groomed'] = 0
    df['groomed'][df['trail_name'].isin(groomed_lst)] = 1
    return df

# TODO: Migrate to main block
for resort, groom in zip(resort_dfs, grooms):
    add_groomed_col(resort, groom)


'''importing pickled dict from webscrape_trails.py'''
pkl_file = open('../data/resort_dict.pkl', 'rb')
# pkl_file = open('../data/resort_dict2.pkl', 'rb') # comb_tables2
dct = pickle.load(pkl_file)
pkl_file.close()

'''REDEFINING'''
resorts = ['Loveland',
           'Arapahoe Basin',
           'Copper',
           'Eldora',
           'Alpine Meadows',
           'Vail',
           'Monarch',
           'Crested Butte',
           'Taos',
           'Diamond Peak',
           'Winter Park',
           'Beaver Creek',
           'Telluride',
           'Bald Mountain',
           'Steamboat',
           'Aspen Snowmass',
           'Wolf Creek']
levels = ['green', 'blue', 'black', 'bb']
resort_dfs = [loveland, AB, copper, eldora,
              AM, vail, monarch, CB, taos, DP, WP, BC,
              telluride, BM, steamboat, AS, WC]
resort_dict = dict(zip(resorts, resort_dfs))


def missing_trails(color_trails, resort):
    '''
    Inputs:
    color_trails = trails_by_color[resort][level] (list)
    resort from resort_dict (str)
    Outputs:
    list of trails by color from webscraping that weren't in the dataframe
    '''
    trail_lst = []
    for trail in color_trails:
        if trail not in list(resort_dict[resort]['trail_name']):
             trail_lst.append(trail)
    return trail_lst


'''getting a useable list of trails to compare by color'''


def get_trails_list(resort, level):
    '''
    Inputs: 
    resort from resorts (str)
    level from levels (str)
    Outputs:
    list of trail names in a useable string format (list)
    '''
    if dct[resort][level] is None:
        return []
    else:
        return [word.encode('ascii', 'ignore').strip().decode('utf-8') for word in dct[resort][level]['Name']]


trails_by_color = {}
for resort in resort_dict:
    trails_by_color[resort] = {level: get_trails_list(
        resort, level) for level in levels}


'''adding a colors column'''


def make_colors(resort):
    '''
    Inputs:
    resort_df from resort_dfs (DataFrame)
    resort from resorts (str)
    Outputs:
    resort_df w/ colors column added (DataFrame)
    '''
    resort_dict[resort]['colors'] = 'color'
    levels = ['green', 'blue', 'black', 'bb']
    for level in levels:
        resort_dict[resort]['colors'][resort_dict[resort]
                                      ['trail_name'].isin(get_trails_list(resort, level))] = level
    return resort_dict[resort]


for resort in resort_dict:
    make_colors(resort)


'''
Dictionary of dictionaries {resort: {level: [trails]}}
For trails that are in the resort_df but have slightly different names from the webscraping (by color)
'''
trails_to_add = {}
trails_to_add['Alpine Meadows'] = {'green': ['Meadow Run', 'Subway Run', 'Teaching Terrain'],
                                   'blue': ['Bobby’s Run', 'Maid Marian', 'Nick’s Run', 'Ray’s Rut', 'Reily’s Run',
                                            'Sandy’s Corner', 'Scotty’s Beam', 'Werner’s Schuss', "Terry’s Return"],
                                   'black': ['Peter’s Peril', 'Hidden Knoll’s', 'Promise Land'],
                                   'bb': []}
trails_to_add['Loveland'] = {'green': ['Cat Walk', 'Deuces Wild', 'Home Run', 'Zig-Zag', 'Magic Carpet Slope'],
                             'blue': ['Apollo (Lower)', 'Apollo (Upper)', 'Blackjack (Lower)', 'Blackjack (Upper)', 'North Chutes', 'Switchback (Lower)',
                                      'Switchback (Upper)', 'Twist (Lower)', 'Twist (Upper)', "Upper Richard's", 'Tempest', "Chet's Run"],
                             'black': ['Cats Meow', 'Fail Safe Trees I', 'Fail Safe Trees II', 'Sunburst Chutes',
                                       "Hook 'Em Horns"],
                             'bb': ['#4 Headwall', 'Upper #4 Headwall', 'Patrol Bowl (Lower)', 'Patrol Bowl (Upper)']}
trails_to_add['Arapahoe Basin'] = {'green': ['Wrangler Lower', 'Wrangler Middle', 'Wrangler Upper', 'Molly Hogan 1', 'Molly Hogan 2', "Molly's Magic Carpet", 'Molly Hogan Upper', 'Carpet II'],
                                   'blue': ['Cornice Run I', 'Cornice Run II', 'T.B. Glade'],
                                   'black': ['Powder Keg Lower', 'Powder Keg Upper'],
                                   'bb': ['13 Cornices Upper', '13 Cornices Lower', 'Roller Coaster', 'West Alley']}
trails_to_add['Copper'] = {'green': ['Lower Carefree', 'Upper Carefree', "Lower Easy Feelin'", "Upper Easy Feelin'",
                                     'Lower High Point', 'Middle High Point', 'Upper High Point', 'Upper Leap Frog',
                                     'Lower Leap Frog', 'Lower Loverly', 'Middle Loverly', 'Upper Loverly', 'Lower Roundabout',
                                     'Middle Roundabout', 'Upper Roundabout', 'See and Ski', 'Lower Soliloquy', 'Upper Soliloquy',
                                     'West Tenmile', 'Green Acres', 'Gem', 'Rugrat', 'Easy Rider', 'The Glide', 'Slingshot',
                                     'Lower Easy Road Traverse', 'Upper Easy Road Traverse'],
                           'blue': ['Copperfields', 'Upper Skid Road'],
                           'black': ["CDL's", 'Allcante', "Ute Overlook", 'Lower Lillie G', 'Upper Lillie G', 'Retreat'],
                           'bb': []}
trails_to_add['Eldora'] = {'green': ['Upper Bunny Fair', 'Fox Tail', 'Little Hawk TRV', 'Tenderfoot I', 'Tenderfoot II'],
                           'blue': ['Crewcut', 'Corona TRV', "Four O' Clock Trail", 'Middle Jolly Jug',
                                    'Lower Jolly Jug', 'Upper Bunny Fair', 'Quickway', 'Sundance', 'Sunkid Slope'],
                           'black': ['Challenge Liftline', 'Corona Road', 'Klondike', 'Upper Diamond Back'],
                           'bb': ['Upper Jolly Jug', 'Liftline']}
trails_to_add['Vail'] = {'green': ["Cubs Way", 'Eagles Nest Ridge', 'Flapjack', 'Lionsway Cutoff', 'Lower Lionsway',
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
trails_to_add['Monarch'] = {'green': ['K C Cutoff', 'Sky Walker I', 'Sky Walker II', 'D rifter', 'G lade', 'Safari'],
                            'blue': ['Bee Line', "D oc’s Run", 'G reat D ivide', 'Q uick D raw', 'Snow Burn', 'Lower Hall’s Alley'],
                            'black': ["B’s Bash", 'D ire Straits', "G eno’s Meadow", "G unbarrel", 'K anonen', 'O utback',
                                      'Upper X mas Tree', 'Upper Hall’s Alley', 'Frazzle'],
                            'bb': ['Mirkwood Basin', 'Mirkwood Basin Egress', ]}
trails_to_add['Crested Butte'] = {'green': ['Big Al’s', 'Bubba’s Shortcut Upper', 'Bubba’s Shortcut Lower', 'Keystone Lower',
                                            'Twister Lower', 'Peachtree Connector', 'Smith Hill Lower', 'Teaching Terrain',
                                            'To Base Area', "Rustler’s Gulch", 'Augusta', 'High Tide', 'Topsy', "Splain's Gulch"],
                                  'blue': ['Gus Way', 'Homeowners', 'Treasury Lower', 'Gallowich', 'Panion’s Run', 'Ruby Chief Lower',
                                           'Gallowich Upper', 'Keystone Upper', 'Treasury Upper', 'Tulsa', 'Smith Hill Upper',
                                           'Ruby Chief Upper', 'Bear', 'Meander', 'Paradise Access', 'Little Lizzie'],
                                  'black': ['Silvanite', 'Twister Upper', 'Twister Connector', 'Keystone Ridge', 'Mach 1', 'Peoria',
                                            'Horseshoe'],
                                  'bb': ['Headwall']}
trails_to_add['Taos'] = {'green': ['Japanese flag', "Jess's (Lower)", "Jess's (Upper)", "Winkelreid", 'Bambi Glade',
                                   'Strawberry Hill', 'High Five Pitch', 'Rueggli', 'Zipper 1', 'Zipper 2', 'Zipper 3'],
                         'blue': ["Maxie's", 'Powderhorn Lower', 'Powderhorn Upper', 'Shalako (Lower)', 'Shalako (Upper)',
                                  'Topa Papa'],
                         'black': ['Raspberry Hill'],
                         'bb': ['Lorelei Trees']}
trails_to_add['Diamond Peak'] = {'green': [],
                                 'blue': [],
                                 'black': ['FIS', 'O God', 'GS'],
                                 'bb': []}
trails_to_add['Winter Park'] = {'green': ['Allen Phipps', "Bill Wilson's Way", 'Upper High Lonesome', 'Lower High Lonesome',
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
trails_to_add['Beaver Creek'] = {'green': ['Beginner Terrain', 'BC Mtn Expressway', 'Easy Come _Easy Go', 'Elkhorn', 'Haymeadow',
                                           'Holden', 'Leav the Beav', 'Meadows', 'Rubarb', 'Ridge Point', 'Highlands Skiway',
                                           'Primrose'],
                                 'blue': ['Creekside', 'Stacker_lower', 'McCoy', 'Paintbrush', 'West Fall Road', 'Camprobber Road',
                                          'Cabin Fever', 'Wapti'],
                                 'black': ['Boarders Loop', 'Goshawk', 'Harrier', 'Centennial', 'Wapiti', 'S. Star'],
                                 'bb': ['Stone Creek Chutes']}
trails_to_add['Telluride'] = {'green': [],
                              'blue': [],
                              'black': [],
                              'bb': []}
trails_to_add['Bald Mountain'] = {'green': [],
                                  'blue': [],
                                  'black': [],
                                  'bb': []}
trails_to_add['Steamboat'] = {'green': [],
                              'blue': [],
                              'black': [],
                              'bb': []}
trails_to_add['Aspen Snowmass'] = {'green': [],
                                   'blue': [],
                                   'black': [],
                                   'bb': []}
trails_to_add['Wolf Creek'] = {'green': [],
                               'blue': [],
                               'black': [],
                               'bb': []}


'''add trails to colors'''


def add_trails_to_add(resort):
    '''
    Inputs:
    resort from resorts (str)
    Outputs:
    resort_df w/ class column updated w/ trail names that didn't make the list (DataFrame)
    '''
    levels = ['green', 'blue', 'black', 'bb']
    for level in levels:
        resort_dict[resort]['colors'][resort_dict[resort]
                                      ['trail_name'].isin(trails_to_add[resort][level])] = level
    return resort_dict[resort]


for resort in resort_dict:
    add_trails_to_add(resort)


'''trails to remove, since i don't have data on them other than the master plan'''
trails_to_remove_LL = ['T-bar Road',
                       'Sani Flush', 'Awesome II', 'Rip Curl', '']
trails_to_remove_AB = ['High Noon Terrain Park',
                       'Treeline Terrain Park', 'Shooting Gallery', 'Poma Line']
trails_to_remove_c = ["Bruce's Way", 'Bee Road', 'Road Home', 'Cross Cut']
trails_to_remove_e = []
trails_to_remove_WP = ['Meadows', 'Nirvana', 'Village Way - Primrose']
trails_to_remove_m = ['K2', 'Tumbelina Lift Line']
trails_to_remove_CB = ['Gallowitch Bend',
                       'Silver Queen Connector', 'Aspen Park', "Shep's Chute"]
trails_to_remove_t = ['White Feather (Middle Pitch)', 'Raspberry (Pitch 1)', 'Raspberry (Pitch 2)', 'Raspberry (Pitch 3)',
                      'Raspberry Hill Traverse', 'Top of Lifts 2 and 6', 'Lorelei Egress', 'Hunziker Egress', 'Lift 6 Liftline',
                      'Avy Road', 'Maidenform']
trails_to_remove_DP = []
trails_to_remove_BC = ['Chair 2', 'Half- Barrell Half Pipe', 'Half Hitch', 'Nastar Ski Racing', 'Park101_Flattops',
                       'Utility Corridor', 'Pitchfork', 'Pines Skiway', "Anderson's Alley", 'Homefire', 'Tall Timber',
                       'Ridge Rider']
trails_to_remove_v = ['Avanti-Cookshack', 'Chair 2 Lift Line', 'Pickeroon Lower', 'Pickeroon-Cookshack', 'Ricochet',
                      'Mountain Top Lift Line', 'Ramshorn Glade', 'Swingsville Ridge', 'Apres Trees East', 'Apres Trees West',
                      'Ho Chi Min Trail', 'Ptarmigan Cornice', "Sama's", 'Turkey Yard', 'Aspen Alley', 'Chair 6 Lift Line', 'Follow Me Road',
                      'Mule Skinner', 'Pony Express', 'Faro Glade', 'Old Midway Catwalk', "Minnie's Cutoff", "Minnie's Mile Upper",
                      "Minnie's Mile Upper Face", 'Hairbag Alley Lower', 'International', 'Mid-Vail Milling Area', 'Villages Catwalk',
                      'Vista Bahn Line Upper', 'Way Over Yonder', 'Gondola Lift Line', 'Simba Face', 'Cascade Way', 'China Wall', 'to Two Elk',
                      'West Wall', 'Upper MongoliaBowl', 'Bwama-Simba Collector', 'Cubs Way Upper', 'Pride Upper Face', 'Black Forest Milling Area',
                      'Nastar', 'Pay-to-Race', 'East Tea Cup', 'Petes Lift Line', 'Berries Catwalk', 'Ch 10 Access', 'Lift Line', "Roger's Glade",
                      "Smokey's", 'Timberline Face', 'Minnies Mile Upper Face']
trails_to_remove_AM = []

trails_to_remove = [trails_to_remove_LL, trails_to_remove_AB, trails_to_remove_c, trails_to_remove_e, trails_to_remove_AM, trails_to_remove_v,
                    trails_to_remove_m, trails_to_remove_CB, trails_to_remove_t, trails_to_remove_DP, trails_to_remove_WP, trails_to_remove_BC]


'''Remove Trails'''


def remove_trails(resort, trail_lst):
    '''
    Inputs:
    resort from resort_dict (str)
    trail_lst from trails_to_remove (list)
    Outputs:
    resort_df with trails removed (DataFrame)
    '''
    resort_df_new = resort_dict[resort][~resort_dict[resort]
                                        ['trail_name'].isin(trail_lst)]
    return resort_df_new


for resort, trail_lst in zip(resort_dict, trails_to_remove):
    resort_dict[resort] = remove_trails(resort, trail_lst)


'''put the dfs back together'''
final_df = pd.concat([resort for resort in resort_dict.values()])

ability_levels = {'Beginner': 1, 'Novice': 2, 'Low Intermediate': 3,
                  'Intermediate': 4, 'Advanced': 5, 'Expert': 6, 'Glade': 5}
colors = {'green': 1, 'blue': 2, 'black': 3, 'bb': 4, 'color': 0}

final_df['ability_nums'] = final_df['ability_level'].map(ability_levels)
final_df['color_nums'] = final_df['colors'].map(colors)

final_df = final_df.reset_index(drop=True)

final_df['trail_name'].iloc[424] = 'Teaching Terrain 1'
final_df['trail_name'].iloc[425] = 'Teaching Terrain 2'
final_df['trail_name'].iloc[750] = 'Teaching Terrain 1'
final_df['trail_name'].iloc[751] = 'Teaching Terrain 2'
final_df['trail_name'].iloc[901] = 'Whistle Stop Lower'
final_df['trail_name'].iloc[908] = 'Whistle Stop Upper'
for i, j in zip(range(1116, 1125), range(1, 10)):
    final_df['trail_name'].iloc[i] = final_df['trail_name'].iloc[i] + \
        " " + str(j)


'''fixing Monarch trail names'''
a = list(final_df['trail_name'][final_df['resort'] == 'Monarch'])
b = [x.split() for x in a]
c = [''.join(x) if len(x[0]) == 1 else ' '.join(x) for x in b]
c[19] = 'Quick Draw'
c[20] = 'KC Cutoff'
c[41] = "Doc's Run"
c[42] = 'Dire Straits'
c[47] = 'Great Divide'
c[53] = "Geno's Meadow"
final_df['trail_name'][final_df['resort'] == 'Monarch'] = c

'''fix trail name'''
final_df['trail_name'][final_df['trail_name']
                       == 'Litter Pierre'] = 'Little Pierre'


output = open('../data/df.pkl', 'wb')
pickle.dump(final_df, output)
output.close()

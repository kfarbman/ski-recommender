import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier

import pandas as pd
import loveland_table
import vail_table
import monarch_table
import DP_table
import WP_table
import BC_table

resorts = {'Loveland': ['data/Loveland.txt', 'CO'],
           'Arapahoe Basin': ['data/Arapahoe_Basin.txt', 'CO'],
           'Copper': ['data/Copper.txt', 'CO'],
           'Eldora': ['data/Eldora.txt', 'CO'],
           'Alpine Meadows': ['data/Alpine_Meadows.txt', 'CA'],
           'Vail': ['data/Vail.txt', 'CO'],
           'Monarch': ['data/Monarch.txt', 'CO'],
           'Crested Butte': ['data/Crested_Butte.txt', 'CO'],
           'Taos': ['data/Taos.txt', 'NM'],
           'Diamond Peak': ['data/DP.txt', 'NV'],
           'Winter Park': ['data/WP.csv', 'CO'],
           'Beaver Creek': ['data/Beaver_Creek.txt', 'CO']}

# which resorts work with which script           
loveland_script = ['Loveland', 'Arapahoe Basin', 'Copper', 'Eldora', 'Alpine Meadows']
vail_script = ['Vail']
monarch_script = ['Monarch', 'Crested Butte', 'Taos']
DP_script = ['Diamond Peak']
WP_script = ['Winter Park']
BC_script = ['Beaver Creek']


d = {}
for resort in loveland_script:
    filename, location = resorts[resort]
    d[resort]= loveland_table.fix_dtype(filename,resort,location)
for resort in vail_script:
    filename, location = resorts[resort]
    d[resort]= vail_table.fix_dtype(filename,resort,location)
    del d[resort]['horiz_length']
for resort in monarch_script:
    filename, location = resorts[resort]
    d[resort]= monarch_table.fix_dtype(filename,resort,location)
    del d[resort]['plan_length']
for resort in DP_script:
    filename, location = resorts[resort]
    d[resort]= DP_table.fix_dtype(filename,resort,location)
    d[resort].drop(['plan_length', 'pct_inc', 'plan_area'],axis=1,inplace=True)
for resort in WP_script:
    filename, location = resorts[resort]
    d[resort] = WP_table.fix_dtype(filename,resort,location)
for resort in BC_script:
    filename, location = resorts[resort]
    d[resort] = BC_table.fix_dtype(filename,resort,location)
    
columns = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level','resort','location']   

whole_table = pd.concat(d.values())
whole_table = whole_table[columns] # making sure the columns are in the correct order
CO_resorts = whole_table[whole_table['location'] == 'CO']



### from my ipython notebook
# standardizing the ability levels
whole_table['ability_level'][whole_table['ability_level'] == 'Advanced Intermediate'] = 'Advanced'
whole_table['ability_level'][whole_table['ability_level'] == 'Adv. Intermediate'] = 'Advanced'
whole_table['ability_level'][whole_table['ability_level'] == 'Hike To'] = 'Expert'
whole_table['ability_level'][whole_table['ability_level'] == 'Exp Bowl'] = 'Expert'


'''separating resorts back out'''
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


resort_dfs = [loveland,AB,copper,eldora,AM,vail,monarch,CB,taos,DP,WP,BC]


'''fixing trail names'''
trail_names_to_fix = [copper,AM,vail,monarch,CB,taos,DP,eldora]
def fix_trail_names(df):
    '''
    Inputs:
    df from trail_names_to_fix (DataFrame)
    Outputs:
    df w/ trail name fixed - removing number at beginning (DataFrame)
    '''
    df['trail_name'] = df['trail_name'].apply(lambda x: ' '.join(x.split()[1:]))
    return df
for trail in trail_names_to_fix:
    fix_trail_names(trail)
copper['trail_name'] = copper['trail_name'].apply(lambda x: ' '.join([i for i in x.split() if i[0].isnumeric() == False]))


'''groomed runs'''
groomed_LL = ['Take Off', 'Cat Walk', 'Mambo', 'Home Run', 'Spillway', 'Tempest', 'Tango Road', 'Turtle Creek', "Richard's Run",
           'Fire Bowl', 'North Turtle Creek', 'Drifter', 'Switchback (Lower)', 'Switchback (Upper)', 'Boomerang',
           'Zig-Zag', 'Twist (Lower)', 'Twist (Upper)', 'Creek Trail', 'Lower Creek Trail', 'Perfect Bowl', 'Scrub',
           'Apollo (Upper)', 'Telestar', 'Deuces Wild', 'Forest Meadow', 'Roulette', 'Keno', 'Royal Flush', 'Straight Flush',
           'Take Off', 'All Smiles', 'Zip Trail', 'Zippity Split', "Chet's Run", 'Awesome', 'Rookie Road','Magic Carpet Slope']

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

groomed_e = ['']


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
             'The Star', 'Coyote Crossing', 'Showboat']

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

grooms = [groomed_LL,groomed_AB,groomed_c,groomed_e,groomed_AM,groomed_v,groomed_m,groomed_CB,groomed_t,groomed_DP,groomed_WP,groomed_BC]


'''adding groomed column'''
def add_groomed_col(df,groomed_lst):
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
    
for resort, groom in zip(resort_dfs,grooms):
    add_groomed_col(resort,groom)
    
    

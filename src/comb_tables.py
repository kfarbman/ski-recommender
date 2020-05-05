import pickle
import warnings
from itertools import chain

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')


class CombineTables:

	def __init__(self):
		
		# Load trail data
		self.df_trails = pd.read_parquet("./data/trail_data_20200423.parquet")
		
		# Load mountain data
		self.df_mountains = pd.read_parquet("./data/mountain_data_20200423.parquet")
		
		self.resort_locations = {
			'Alpine Meadows': 'CA',
			'Arapahoe Basin': 'CO',
			'Aspen Snowmass': 'CO',
			'Bald Mountain':  'CO',
			'Beaver Creek': 'CO',
			'Copper': 'CO',
			'Crested Butte': 'CO',
			'Diamond Peak': 'NV',
			'Eldora': 'CO',
			'Jackson Hole': 'WY',
			'Loveland': 'CO',
			'Monarch': 'CO',
			'Steamboat': 'CO',
			'Taos': 'NM',
			'Telluride': 'CO',
			'Vail': 'CO',
			'Winter Park': 'CO',
			'Wolf Creek': 'CO'}

		self.dict_groomed_runs = {
		
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

	def map_resort_location(self):
		"""
		Map state to resort name

		INPUT
			None
		
		OUTPUT
			df_mountains DataFrame with 'Location' column
		"""
		self.df_mountains["Location"] = self.df_mountains["Resort"].map(self.resort_locations).fillna("__NA__")

	def add_groomed_col(self):
		'''
		Add groomed column to trail data

		Inputs:
			None
		Outputs:
			df_trails DataFrame with "Groomed" column
		'''
		lst_groomed_runs = list(chain(*self.dict_groomed_runs.values()))

		self.df_trails['Groomed'] = "Ungroomed"
		self.df_trails['Groomed'][self.df_trails['Trail Name'].isin(lst_groomed_runs)] = "Groomed"

	def merge_data_frames(self):
		"""
		Merge trail and mountain DataFrames into single DataFrame

		INPUT
			None

		OUTPUT
			Merged DataFrame
		"""

		df_merged = pd.merge(self.df_trails, self.df_mountains, on="Resort", how="inner")

		return df_merged


if __name__ == '__main__':

	combine = CombineTables()

	# Add Location column to mountain data
	combine.map_resort_location()

	# Add groomed column to trail data	
	combine.add_groomed_col()

	# Merge trail and mountain data
	df_merged = combine.merge_data_frames()

	# Save combined data
	# df_merged.to_csv("./data/combined_data_20200423.csv", index=False, header=True)

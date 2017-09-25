# ski-recommender

http://ec2-34-233-11-239.compute-1.amazonaws.com:8080/


Working on creating a ski run recommender.

Technologies: sklearn, flask, matplotlib, html/javascript/css, pandas, numpy, BeautifulSoup, AWS EC2

create_tables
-has scripts which take in pdf/txt/csv and convert to a dataframe by resort
-slightly different conditions from tables meant using different scripts

data
-contains txt/pdf/csv tables from master development plans

web_app 
-contains files to run web app

.ipynb
-used most of these to play around until I had what I wanted for a real script
-also used for visualization

visualizations.ipynb
-contains some interesting visualizations of data

comb_tables.py
-creates a dictionary of resort dataframes (created from scripts in create_tables)
-fixes trail names
-adds grooming column
-adds color column (from webscrape_trails and manually)
-removes trails that don't have grooming or color info (were in the master development plan)
-puts the dataframes from each resort back together
-maps ability levels and colors to numbers
-fixes names from Monarch and trails that have the same name at the same resort
-saves a pickle of the dataframe

cosine_sims.py
-made cosine_sim_recommendations function (actually appears in app.py)

df.pkl
-pickle of dataframe used for trail recommendations

mtn_df.pkl
-pickle of dataframe used for mountain recommendations

resort_dict.pickle
-pickle of dictionary of resort/color dataframes from webscrape_trails

make_mtn_df.py
-creates dataframe from pickle of dataframe used for recommendations
-webscrapes to add resort level data
-saves a pickle of the new dataframe

resort_stats.py
-webscrapes stats by resort
-NOT CURRENTLY USING

webscrape_trails.py
-webscrapes to get trails by color for each resort
-saves a pickle of dictionary of results

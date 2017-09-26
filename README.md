# ski-recommender

As I was prepping for my PSIA Level 3 exam at Vail (never having skied at Vail), 
word on the slopes was that the mogul portion of the ski exam was going to be 
on Prima and Pronto. From my research on Vail, I knew that Prima and Pronto were 
black and double black, but I didn't know what to compare them to. With Winter Park 
as my home mountain, I had skied a huge range of black mogul runs, and they were all 
vastly different. Someone told me that if I could ski Outhouse at Winter Park, 
that was a pretty good indicator of how I would do on Prima or Pronto - they had a 
similar slope and width and were ungroomed. 

How awesome would it be to find runs similar to a given run based on their features, 
even at a mountain you know nothing about? You can find runs at a mountain you're 
unfamiliar with that are similar to a run you love. Or you can find out what a run 
you've never skied on is like by finding out which runs it is like at a resort you know.

Try it out: http://ec2-34-233-11-239.compute-1.amazonaws.com:8080/


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

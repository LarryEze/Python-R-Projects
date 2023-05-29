#!/usr/bin/env python
# coding: utf-8

# ## 1. Importing the Data
# <p><img src="https://assets.datacamp.com/production/project_1230/img/nyc.jpg" alt="New York City skyline" width="600px">
# <br>
# Welcome to New York City (NYC), one of the most-visited cities in the world. 
# As a result, there are many <a href="https://www.airbnb.com/"><em>Airbnb</em></a> listings to meet the high demand for temporary lodging for anywhere between a few nights to many months. 
# In this notebook, we will take a look at the NYC Airbnb market by combining data from multiple file types like <code>.csv</code>, <code>.tsv</code>, and <code>.xlsx</code>.</p>
# <p><br><br>
# We will be working with three datasets:</p>
# <ol>
# <li><p><code>"datasets/airbnb_price.csv"</code></p></li>
# <li><p><code>"datasets/airbnb_room_type.xlsx"</code></p></li>
# <li><p><code>"datasets/airbnb_last_review.tsv"</code></p></li>
# </ol>
# <p><br><br>
# Our goals are to convert untidy data into appropriate formats to analyze, and answer key questions including:</p>
# <ul>
# <li>What is the average price, per night, of an Airbnb listing in NYC? </li>
# <li>How does the average price of an Airbnb listing, per month, compare to the private rental market? </li>
# <li>How many adverts are for private rooms? </li>
# <li>How do Airbnb listing prices compare across the five NYC boroughs?</li>
# </ul>

# In[2]:


import pandas as pd
import numpy as np
import datetime as dt

# Load airbnb_price.csv, prices
prices = pd.read_csv("datasets/airbnb_price.csv")

# Load airbnb_room_type.xlsx, xls
xls = pd.ExcelFile("datasets/airbnb_room_type.xlsx")

# Parse the first sheet from xls, room_types
room_types = xls.parse(0)

# Load airbnb_last_review.tsv, reviews
reviews = pd.read_csv("datasets/airbnb_last_review.tsv", sep="\t")

# Print the first five rows of each DataFrame
print(prices.head(), "\n", room_types.head(), "\n", reviews.head())


# In[3]:


get_ipython().run_cell_magic('nose', '', '\nprices_copy = pd.read_csv(\'datasets/airbnb_price.csv\')\nxls_copy = pd.ExcelFile(\'datasets/airbnb_room_type.xlsx\')\nroom_types_copy = xls_copy.parse(0)\nreviews_copy = pd.read_csv("datasets/airbnb_last_review.tsv", sep=\'\\t\')\n\ndef test_pandas_loaded():\n    assert \'pd\' in globals(), \\\n    "Have you imported pandas using the correct alias?"\n\ndef test_prices_loaded():\n    assert isinstance(prices, pd.DataFrame), \\\n    "Have you created a DataFrame called prices by using pd.read_csv()?"\n    assert prices_copy.equals(prices), \\\n    """"Did you correctly load "datasets/airbnb_price.csv"""\n\ndef test_room_types_loaded():\n    assert isinstance(room_types, pd.DataFrame), \\\n    "Have you created a DataFrame called room_types by using pd.read_csv()?"\n    assert room_types_copy.equals(room_types), \\\n    """Did you correctly load "datasets/airbnb_room_type.xlsx"""\n\ndef test_reviews_loaded():\n    assert isinstance(reviews, pd.DataFrame), \\\n    """Have you created a DataFrame called reviews by using pd.read_csv() and setting sep="\\t"?"""\n    assert reviews_copy.equals(reviews), \\\n    """Did you correctly load "datasets/airbnb_last_review.tsv"""')


# ## 2. Cleaning the price column
# <p>Now the <code>DataFrames</code> have been loaded, the first step is to calculate the average price per listing by <code>room_type</code>. </p>
# <p>You may have noticed that the <code>price</code> column in the <code>prices</code> DataFrame currently states each value as a string with the currency (dollars) following, i.e.,</p>
# <pre><code>price
# 225 dollars
# 89 dollars
# 200 dollars</code></pre>
# <p></p>
# <p>We will need to clean the column in order to calculate the average price.</p>

# In[4]:


# Remove whitespace and string characters from prices column
prices["price"] = prices["price"].str.replace(" dollars", "")

# Convert prices column to numeric datatype
prices["price"] = pd.to_numeric(prices["price"])

# Print descriptive statistics for the price column
print(prices["price"].describe())


# In[5]:


get_ipython().run_cell_magic('nose', '', '\nprices_copy = pd.read_csv(\'datasets/airbnb_price.csv\')\nprices_copy = prices_copy[\'price\'].str.replace(" dollars", "")\nprices_copy = pd.to_numeric(prices_copy)\n\ndef test_prices_column():\n    assert prices_copy.equals(prices[\'price\']), \\\n    "Did you remove all string characters from the \'price\' column?"\n    assert prices[\'price\'].dtype == \'int64\' or prices[\'price\'].dtype == \'float64\', \\\n    "Did you correctly convert the \'price\' column to numeric data type?"')


# ## 3. Calculating average price
# <p>We can see three quarters of listings cost \$175 per night or less. </p>
# <p>However, there are some outliers including a maximum price of \$7,500 per night! </p>
# <p>Some of listings are actually showing as free. Let's remove these from the <code>DataFrame</code>, and calculate the average price.</p>

# In[6]:


# Subset prices for listings costing $0, free_listings
free_listings = prices["price"] == 0

# Update prices by removing all free listings from prices
prices = prices.loc[~free_listings]

# Calculate the average price, avg_price
avg_price = round(prices["price"].mean(), 2)

# Print the average price
print("The average price per night for an Airbnb listing in NYC is ${}.".format(avg_price))


# In[7]:


get_ipython().run_cell_magic('nose', '', '\ndef test_prices():\n    assert prices[\'price\'].isin([0]).any() == False, \\\n    "Have all listings with a price of $0 been removed from the DataFrame?"\n\ndef test_avg_price():\n    assert avg_price == round(prices[\'price\'].mean(), 2) or avg_price == prices["price"].mean().round(2), \\\n    "Did you choose the correct method to calculate the average price?"')


# ## 4. Comparing costs to the private rental market
# <p>Now we know how much a listing costs, on average, per night, but it would be useful to have a benchmark for comparison. 
# According to <a href="https://www.zumper.com/rent-research">Zumper</a>, a 1 bedroom apartment in New York City costs, on average, $3,100 per month. Let's convert the per night prices of our listings into monthly costs, so we can compare to the private market. </p>

# In[8]:


# Add a new column to the prices DataFrame, price_per_month
prices["price_per_month"] = prices["price"] * 365 / 12

# Calculate average_price_per_month
average_price_per_month = round(prices["price_per_month"].mean(), 2)

# Compare Airbnb and rental market
print("Airbnb monthly costs are ${}, while in the private market you would pay {}.".format(average_price_per_month, "$3,100.00"))


# In[9]:


get_ipython().run_cell_magic('nose', '', '\ndef test_price_per_month_in_df():\n    assert \'price_per_month\' in prices.columns, \\\n    "Has \'price_per_month\' been added as a column in the \'prices\' DataFrame?"\n    \ndef test_price_per_month_correct_values():\n    prices_per_month_copy = prices[\'price\'] * 365 / 12\n    assert prices_per_month_copy.equals(prices[\'price_per_month\']), \\\n    "Have you correctly calculated the values in the \'price_per_month\' column?"\n\ndef test_avg_price_per_month_correct_values():\n    average_price_per_month_copy = round(prices[\'price_per_month\'].mean(), 2)\n    assert round(np.mean(prices[\'price_per_month\']), 2) == average_price_per_month_copy, \\\n    "Have you correctly calculated the average price per month? Make sure you have rounded to the nearest two decimal places."')


# ## 5. Cleaning the room type column
# <p>Unsurprisingly, using Airbnb appears to be substantially more expensive than the private rental market. We should, however, consider that these Airbnb listings include single private rooms or even rooms to share, as well as entire homes/apartments. 
# <br><br>
# Let's dive deeper into the <code>room_type</code> column to find out the breakdown of listings by type of room. The <code>room_type</code> column has several variations for <code>private room</code> listings, specifically: </p>
# <ul>
# <li>"Private room"</li>
# <li>"private room"</li>
# <li>"PRIVATE ROOM"</li>
# </ul>
# <p>We can solve this by converting all string characters to lower case (upper case would also work just fine). </p>

# In[10]:


# Convert the room_type column to lowercase
room_types["room_type"] = room_types["room_type"].str.lower()

# Update the room_type column to category data type
room_types["room_type"] = room_types["room_type"].astype("category")

# Create the variable room_frequencies
room_frequencies = room_types["room_type"].value_counts()

# Print room_frequencies
print(room_frequencies)


# In[11]:


get_ipython().run_cell_magic('nose', '', '\nroom_types_copy = pd.read_excel("datasets/airbnb_room_type.xlsx")\nroom_types_copy = room_types_copy[\'room_type\'].str.lower()\nroom_types_copy = room_types_copy.astype(\'category\')\n\ndef test_lower_case():\n    assert np.all(room_types[\'room_type\'].str.islower()) == True, \\\n    "Have you converted all string characters to lower case?"\n    assert room_types[\'room_type\'].equals(room_types_copy), \\\n    "Have all string characters in the column been converted to lower case?"\n\ndef test_room_frequencies():\n    room_counts_copy = room_types_copy.value_counts()\n    assert room_frequencies.equals(room_counts_copy), \\\n    "Have you correctly defined room_frequencies?"')


# ## 6. What timeframe are we working with?
# <p>It seems there is a fairly similar sized market opportunity for both private rooms (45% of listings) and entire homes/apartments (52%) on the Airbnb platform in NYC.
# <br><br></p>
# <p>Now let's turn our attention to the <code>reviews</code> DataFrame. The <code>last_review</code> column contains the date of the last review in the format of "Month Day Year" e.g., May 21 2019. We've been asked to find out the earliest and latest review dates in the DataFrame, and ensure the format allows this analysis to be easily conducted going forwards. </p>

# In[12]:


# Change the data type of the last_review column to datetime
reviews["last_review"] = pd.to_datetime(reviews["last_review"])

# Create first_reviewed, the earliest review date
first_reviewed = reviews["last_review"].dt.date.min()

# Create last_reviewed, the most recent review date
last_reviewed = reviews["last_review"].dt.date.max()

# Print the oldest and newest reviews from the DataFrame
print("The earliest Airbnb review is {}, the latest review is {}".format(first_reviewed, last_reviewed))


# In[13]:


get_ipython().run_cell_magic('nose', '', '\nreviews_copy = pd.read_csv("datasets/airbnb_last_review.tsv", sep=\'\\t\')\nreviews_copy[\'last_review\'] = pd.to_datetime(reviews_copy[\'last_review\'])\n\ndef test_first_review_date():\n    first_reviewed_copy = reviews_copy[\'last_review\'].dt.date.min()\n    assert first_reviewed == first_reviewed_copy, \\\n    "Has \'first_reviewed\' been calculated correctly?"\n\ndef test_last_review_date():\n    last_reviewed_copy = reviews_copy[\'last_review\'].dt.date.max()\n    assert last_reviewed == last_reviewed_copy, \\\n    "Has \'last_reviewed\' been calculated correctly?"')


# ## 7. Joining the DataFrames.
# <p>Now we've extracted the information needed, we will merge the three DataFrames to make any future analysis easier to conduct. Once we have joined the data, we will remove any observations with missing values and check for duplicates.</p>

# In[14]:


# Merge prices and room_types to create rooms_and_prices
rooms_and_prices = prices.merge(room_types, how="outer", on="listing_id")

# Merge rooms_and_prices with the reviews DataFrame to create airbnb_merged
airbnb_merged = rooms_and_prices.merge(reviews, how="outer", on="listing_id")

# Drop missing values from airbnb_merged
airbnb_merged.dropna(inplace=True)

# Check if there are any duplicate values
print("There are {} duplicates in the DataFrame.".format(airbnb_merged.duplicated().sum()))


# In[15]:


get_ipython().run_cell_magic('nose', '', '\nprices_copy = pd.read_csv(\'datasets/airbnb_price.csv\')\nxls_copy = pd.ExcelFile(\'datasets/airbnb_room_type.xlsx\')\nroom_types_copy = xls_copy.parse(0)\nreviews_copy = pd.read_csv("datasets/airbnb_last_review.tsv", sep=\'\\t\')\nprices_copy[\'price\'] = prices_copy[\'price\'].str.replace(" dollars", "")\nprices_copy[\'price\'] = pd.to_numeric(prices_copy[\'price\'])\nfree_listings = prices_copy[\'price\'] == 0\nprices_copy = prices_copy.loc[~free_listings]\nprices_copy[\'price_per_month\'] = prices_copy[\'price\'] * 365 / 12\nroom_types_copy[\'room_type\'] = room_types_copy[\'room_type\'].str.lower()\nroom_types_copy[\'room_type\'] = room_types_copy[\'room_type\'].astype(\'category\')\nreviews_copy[\'last_review\'] = pd.to_datetime(reviews_copy[\'last_review\'])\nrooms_and_prices_copy = prices_copy.merge(room_types_copy, how=\'outer\', on=\'listing_id\')\n\ndef test_rooms_and_prices_shape():\n    assert rooms_and_prices.shape[0] == 25209, \\\n    "Have you correctly merged the \'prices\' and \'room_types\' DataFrames? Expected the new DataFrame to have a different length."\n    assert rooms_and_prices.shape[1] == 6, \\\n    "\'rooms_and_prices\' doesn\'t contain the correct number of columns. Did you use the correct join method and specify the relevant column to merge on?"\n\ndef test_airbnb_merged_shape():\n    assert airbnb_merged.shape[0] == 25184, \\\n    "Have you correctly merged the \'rooms_and_prices\' and \'reviews\' DataFrames? Expected the new DataFrame to have a different length."\n    assert airbnb_merged.shape[1] == 8, \\\n    "\'airbnb_merged\' doesn\'t contain the correct number of columns. Did you use the correct join method and specify the relevant column to merge on?"\n\ndef test_rooms_and_prices():\n    assert rooms_and_prices.equals(rooms_and_prices_copy), \\\n    "Have you correctly merged \'prices\' and \'room_types\'? Expected different values."\n\ndef test_airbnb_merged():\n    airbnb_merged_copy = rooms_and_prices_copy.merge(reviews_copy, how=\'outer\', on=\'listing_id\')\n    airbnb_merged_copy = airbnb_merged_copy.dropna()\n    assert airbnb_merged.equals(airbnb_merged_copy), \\\n    "Have you correctly merged \'rooms_and_prices\' with \'reviews\'? Expected different values."')


# ## 8. Analyzing listing prices by NYC borough
# <p>Now we have combined all data into a single DataFrame, we will turn our attention to understanding the difference in listing prices between <a href="https://en.wikipedia.org/wiki/Boroughs_of_New_York_City">New York City boroughs</a>. 
# We can currently see boroughs listed as the first part of a string within the <code>nbhood_full</code> column, e.g., </p>
# <pre><code>Manhattan, Midtown
# Brooklyn, Clinton Hill
# Manhattan, Murray Hill
# Manhattan, Hell's Kitchen
# Manhattan, Chinatown</code></pre>
# <p></p>
# <p>We will therefore need to extract this information from the string and store in a new column, <code>borough</code>, for analysis.</p>

# In[16]:


# Extract information from the nbhood_full column and store as a new column, borough
airbnb_merged["borough"] = airbnb_merged["nbhood_full"].str.partition(",")[0]

# Group by borough and calculate summary statistics
boroughs = airbnb_merged.groupby("borough")["price"].agg(["sum", "mean", "median", "count"])

# Round boroughs to 2 decimal places, and sort by mean in descending order
boroughs = boroughs.round(2).sort_values("mean", ascending=False)

# Print boroughs
print(boroughs)


# In[17]:


get_ipython().run_cell_magic('nose', '', '\nprices_copy = pd.read_csv(\'datasets/airbnb_price.csv\')\nxls_copy = pd.ExcelFile(\'datasets/airbnb_room_type.xlsx\')\nroom_types_copy = xls_copy.parse(0)\nreviews_copy = pd.read_csv("datasets/airbnb_last_review.tsv", sep=\'\\t\')\nprices_copy[\'price\'] = prices_copy[\'price\'].str.replace(" dollars", "")\nprices_copy[\'price\'] = pd.to_numeric(prices_copy[\'price\'])\nfree_listings = prices_copy[\'price\'] == 0\nprices_copy = prices_copy.loc[~free_listings]\nprices_copy[\'price_per_month\'] = prices_copy[\'price\'] * 365 / 12\nroom_types_copy[\'room_type\'] = room_types_copy[\'room_type\'].str.lower()\nroom_types_copy[\'room_type\'] = room_types_copy[\'room_type\'].astype(\'category\')\nreviews_copy[\'last_review\'] = pd.to_datetime(reviews_copy[\'last_review\'])\ncorrect_airbnb_merged = rooms_and_prices.merge(reviews, how=\'outer\', on=\'listing_id\')\ncorrect_airbnb_merged = correct_airbnb_merged.dropna()\ncorrect_airbnb_merged[\'borough\'] = correct_airbnb_merged[\'nbhood_full\'].str.partition(\',\')[0]\ncorrect_boroughs = correct_airbnb_merged.groupby(\'borough\')[\'price\'].agg([\'sum\', \'mean\', \'median\', \'count\']).round(2).sort_values(\'mean\', ascending=False)\n\ndef test_borough_column_exists():\n    assert \'borough\' in airbnb_merged.columns, \\\n    "Did you add \'borough\' as a column to the \'airbnb_merged\' DataFrame?"\n    \ndef test_summary_statistics():\n    assert \'sum\' in boroughs.columns, \\\n    "Did you include \'sum\' as one of the summary statistics? Can\'t find this column in \'boroughs\'."\n    assert \'mean\' in boroughs.columns, \\\n    "Did you include \'mean\' as one of the summary statistics? Can\'t find this column in \'boroughs\'."\n    assert \'median\' in boroughs.columns, \\\n    "Did you include \'median\' as one of the summary statistics? Can\'t find this column in \'boroughs\'."\n    assert \'count\' in boroughs.columns, \\\n    "Did you include \'count\' as one of the summary statistics? Can\'t find this column in \'boroughs\'."\n    \ndef test_borough_column_values():\n    borough_list = [\'Manhattan\', \'Brooklyn\', \'Queens\', \'Staten Island\', \'Bronx\']\n    assert airbnb_merged[\'borough\'].isin(borough_list).any(), \\\n    "Did you correctly split the \'nbhood_full\' column? Expected different values in the \'borough\' column."\n    \ndef test_boroughs():\n    assert boroughs.iloc[-1].values.tolist() == [55156.0, 79.25, 65.0, 696.0], \\\n    """Did you sort the values by "mean" in descending order? Expected the lowest average price to be in the final row of the DataFrame."""\n    assert boroughs.iloc[0].values.tolist() == [1898417.0, 184.04, 149.0, 10315.0], \\\n    """Did you sort the values by "mean" in descending order? Expected the highest average price to be in the first row of the DataFrame."""')


# ## 9. Price range by borough
# <p>The above output gives us a summary of prices for listings across the 5 boroughs. In this final task we would like to categorize listings based on whether they fall into specific price ranges, and view this by borough. 
# <br><br>
# We can do this using percentiles and labels to create a new column, <code>price_range</code>, in the DataFrame.
# Once we have created the labels, we can then group the data and count frequencies for listings in each price range by borough.
# <br><br>
# We will assign the following categories and price ranges:</p>
# <table>
# <thead>
# <tr>
# <th>label</th>
# <th>price</th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td><code>Budget</code></td>
# <td>\$0-69</td>
# </tr>
# <tr>
# <td><code>Average</code></td>
# <td>\$70-175</td>
# </tr>
# <tr>
# <td><code>Expensive</code></td>
# <td>\$176-350</td>
# </tr>
# <tr>
# <td><code>Extravagant</code></td>
# <td>&gt; \$350</td>
# </tr>
# </tbody>
# </table>

# In[18]:


# Create labels for the price range, label_names
label_names = ["Budget", "Average", "Expensive", "Extravagant"]

# Create the label ranges, ranges
ranges = [0, 69, 175, 350, np.inf]

# Insert new column, price_range, into DataFrame
airbnb_merged["price_range"] = pd.cut(airbnb_merged['price'], bins=ranges, labels=label_names)

# Calculate borough and price_range frequencies, prices_by_borough
prices_by_borough = airbnb_merged.groupby(['borough', 'price_range']).size()
print(prices_by_borough)


# In[19]:


get_ipython().run_cell_magic('nose', '', '    \ndef test_label_names():\n    correct_labels = [\'Budget\', \'Average\', \'Expensive\', \'Extravagant\']\n    assert correct_labels == label_names, \\\n    "Have you correctly specified the \'label_names\', expected something else?"\n\ndef test_ranges():\n    correct_ranges = [0, 69, 175, 350, np.inf]\n    assert correct_ranges == ranges, \\\n    "Have you entered the correct values for \'ranges\', expected something different?"\n    \ndef test_budget_prices():\n    budget = airbnb_merged[airbnb_merged[\'price_range\'] == \'Budget\']\n    average = airbnb_merged[airbnb_merged[\'price_range\'] == \'Average\']\n    expensive = airbnb_merged[airbnb_merged[\'price_range\'] == \'Expensive\']\n    extravagant = airbnb_merged[airbnb_merged[\'price_range\'] == \'Extravagant\']\n    assert budget[\'price\'].max() == 69, \\\n    "Have you correctly mapped the labels and ranges to the \'price_range\' column?"\n    assert average[\'price\'].min() > 69 and average[\'price\'].max() == 175, \\\n    "Have you correctly mapped the labels and ranges to the \'price_range\' column?"\n    assert expensive[\'price\'].min() > 175 and expensive[\'price\'].max() == 350, \\\n    "Have you correctly mapped the labels and ranges to the \'price_range\' column?"\n    assert extravagant[\'price\'].min() > 350, \\\n    "Have you correctly mapped the labels and ranges to the \'price_range\' column?"\n\ndef test_correct_grouping():\n    prices_by_borough_copy = airbnb_merged.groupby([\'borough\', \'price_range\'])[\'price_range\'].count()\n    assert prices_by_borough.equals(prices_by_borough_copy) or prices_by_borough.equals(airbnb_merged.groupby([\'borough\', \'price_range\'])[\'price_range\'].agg({"price_range": "count"})), \\\n    "Have you grouped airbnb_merged on the correct columns? Did you specify the appropriate method to count observations?"')


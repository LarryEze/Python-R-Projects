#!/usr/bin/env python
# coding: utf-8

# ## 1. DRY: Don't repeat yourself
# <p><img src="https://assets.datacamp.com/production/project_1234/img/survey.png" style="float: center;" alt="A pictogram of a blood bag with blood donation written in it" width="100%"></p>
# <p>Have you ever started your data analysis and ended up with repetitive code? Our colleague Brenda who works as a Product Analyst, has found herself in this situation and has asked us for some help. She's written a script to pull Net Promotor Score (NPS) data from various sources. NPS works by asking <em>How likely is it that you would recommend our product to a friend or colleague?</em> with a rating scale of 0 to 10. Brenda has set up this NPS survey in various ways, including emails and pop-ups on the mobile app and website. To compile the data from the different sources, she's written the following code:</p>
# <pre><code class="py language-py"># Read the NPS email responses into a DataFrame
# email = pd.read_csv("datasets/2020Q4_nps_email.csv")
# # Add a column to record the source
# email['source'] = 'email'
# 
# # Repeat for NPS mobile and web responses
# mobile = pd.read_csv("datasets/2020Q4_nps_mobile.csv")
# mobile['source'] = 'mobile'
# web = pd.read_csv("datasets/2020Q4_nps_web.csv")
# web['source'] = 'web'
# 
# # Combine the DataFrames
# q4_nps = pd.concat([email,mobile,web])
# </code></pre>
# <p>This results in the DataFrame <code>q4_nps</code> that looks like this:</p>
# <table>
# <thead>
# <tr>
# <th></th>
# <th><code>response_date</code></th>
# <th><code>user_id</code></th>
# <th><code>nps_rating</code></th>
# <th><code>source</code></th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td>0</td>
# <td>2020-10-29</td>
# <td>36742</td>
# <td>2</td>
# <td>email</td>
# </tr>
# <tr>
# <td>1</td>
# <td>2020-11-26</td>
# <td>31851</td>
# <td>10</td>
# <td>email</td>
# </tr>
# <tr>
# <td>2</td>
# <td>2020-10-27</td>
# <td>44299</td>
# <td>10</td>
# <td>email</td>
# </tr>
# <tr>
# <td>…</td>
# <td>…</td>
# <td>…</td>
# <td>…</td>
# <td>…</td>
# </tr>
# </tbody>
# </table>
# <p>This code works, but it violates the Don't Repeat Yourself (DRY) programming principle. Brenda repeats the same code for email, mobile, and web, except with different variable names and file names. While it's often quicker to copy and paste, it makes it easier to introduce errors. For example, if you need to edit one of those lines, you have to do it in multiple places. Enter functions! Repeated code is a sign that we need functions. Let's write a function for Brenda.</p>

# In[2]:


# Import pandas with the usual alias
import pandas as pd

# Write a function that matches the docstring
def convert_csv_to_df(csv_name, source_type):
    """ Converts an NPS CSV into a DataFrame with a column for the source. 

    Args:
        csv_name (str): The name of the NPS CSV file.
        source_type (str): The source of the NPS responses.

    Returns:
        A DataFrame with the CSV data and a column, source.
    """
    df = pd.read_csv(csv_name)
    df['source'] = source_type
    return df

# Test the function on the mobile data
convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")


# In[3]:


get_ipython().run_cell_magic('nose', '', 'from inspect import signature\n\n# correct answer\ndef correct(csv_name, source_type):\n    df = pd.read_csv(csv_name)\n    df[\'source\']= source_type\n    return df\n\nuser_df = convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")\n\ndef test_convert_csv_to_df():\n    # check num of arguments is 2\n    assert len(signature(convert_csv_to_df).parameters) == 2, \\\n    \'Your function should have two arguments: the name of the CSV file and the source type. Both of which are strings.\'\n    # check that a dataframe being returned\n    assert isinstance(user_df, pd.DataFrame), \\\n    \'Your function should return a DataFrame.\'\n    # see if source column is there\n    assert \'source\' in user_df.columns, \\\n    \'Your function should add a column called `source` to the DataFrame.\'\n    # check that all four columns are there\n    assert len(user_df.columns) == 4, \\\n    \'Your function should return a DataFrame with four columns: `response_date`, `user_id`, `nps_rating`, and `source`.\'\n    # catch all\n    assert correct("datasets/2020Q4_nps_email.csv", "email").equals(convert_csv_to_df("datasets/2020Q4_nps_email.csv", "email")), \\\n    \'Your function is not returning the expected output.\'')


# ## 2. Verifying the files with the "with" keyword
# <p>Excellent, we have a function that reads and cleans Brenda's CSVs precisely the way she needs! She can call this function in the future for as many different sources as she wants. Before we combine the NPS DataFrames, we want to add a function that verifies that the files inputted are valid. Each of these NPS dataset files should have three columns: <code>response_date</code>, <code>user_id</code>, <code>nps_rating</code>. Previously, Brenda would check this manually by opening each file. </p>
# <p>Let's write a function that uses the <strong>context manager</strong> <code>with open()</code> so that we properly close the files we open, <a href="https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files">even if an exception is raised</a>. If we don't use the <code>with</code> keyword with <code>open()</code> , we would need to call <code>close()</code> after we're done with the file. Even then, it's risky because an error might be raised before the <code>close()</code> functions are called. </p>
# <p>The function will return <code>True</code> if the file contains the right columns. Otherwise, it will return <code>False</code>. To test the function, we'll use <code>datasets/corrupted.csv</code> to simulate a corrupted invalid NPS file.</p>

# In[4]:


# Define a function check_csv which takes csv_name
def check_csv(csv_name):
    """ Checks if a CSV has three columns: response_date, user_id, nps_rating

    Args:
        csv_name (str): The name of the CSV file.

    Returns:
        Boolean: True if the CSV is valid, False otherwise 
    """
    # Open csv_name as f using the with keyword
    with open(csv_name) as f:
        first_line = f.readline()
        # Return true if the CSV has the three specified columns
        if first_line == "response_date,user_id,nps_rating\n":
            return True
        # Otherwise, return false    
        else:
            return False

# Test the function on a corrupted NPS file
check_csv('datasets/corrupted.csv')


# In[5]:


get_ipython().run_cell_magic('nose', '', '\nimport inspect\n\n# correct answer\ndef correct_check(csv_name):\n    with open(csv_name) as f:\n        first_line = f.readline()\n        if first_line == "response_date,user_id,nps_rating\\n":\n            return True\n        else:\n            return False\n\ndef test_check_csv():\n    # check that check_csv() has been defined\n    assert inspect.isfunction(check_csv), \\\n    \'Did you define a function with the name `check_csv`?\'\n    # check num of arguments is 1\n    assert len(inspect.signature(check_csv).parameters) == 1, \\\n    \'Your function should have one argument: the name of the CSV file.\'\n    # check that a Boolean being returned\n    assert isinstance(check_csv(\'datasets/corrupted.csv\'), bool), \\\n    \'Your function should return a boolean, meaning it should return either `True` or `False`.\'\n    assert isinstance(check_csv(\'datasets/2020Q4_nps_email.csv\'), bool), \\\n    \'Your function should return a boolean, meaning it should return either `True` or `False`.\'\n    # make sure this returns false\n    assert not check_csv(\'datasets/corrupted.csv\'), \\\n    "`check_csv(\'datasets/corrupted.csv\')` is returning `True` despite not having the three columns needed."\n    # make sure this returns true\n    assert check_csv(\'datasets/2020Q4_nps_email.csv\'), \\\n    "`check_csv(\'datasets/2020Q4_nps_email.csv\')` is returning `False` despite having the three columns needed."\n    # catch all\n    assert correct_check(\'datasets/2020Q4_nps_web.csv\')== check_csv(\'datasets/2020Q4_nps_web.csv\'), \\\n    \'Your function is not returning the expected output.\'')


# ## 3. Putting it together with nested functions
# <p>Alright, we now have one function that verifies that the CSVs are valid and another that converts them into the DataFrame format needed by Brenda. What's left? Looking at the script, this is the last line we haven't covered: <code>q4_nps = pd.concat([email,mobile,web])</code>. We could use this line of code, but we'll see more code repetition if we get CSVs from other sources or time periods.</p>
# <p>To make sure our code is scalable, we're going to write a function called <code>combine_nps_csvs()</code> that takes in a dictionary. Python dictionaries have key:value pairs. In our case, the CSV's name and source type will be the key and value, respectively. That way, we can define a dictionary with as many NPS files as we have and run it through <code>combine_nps_csvs()</code>. For each file, we'll check that it's valid using <code>check_csv()</code>, and if it is, we'll use <code>convert_csv_to_df()</code> to convert it into a DataFrame. At the start of the function, we'll define an empty DataFrame called <code>combined</code> and everytime a CSV is succesfully converted, we'll concatenate it to <code>combined</code>.</p>

# In[6]:


# Write a function combine_nps_csvs() with the arg csvs_dict 
def combine_nps_csvs(csvs_dict):
    # Define combine as an empty DataFrame
    combined = pd.DataFrame()
    # Iterate over csvs_dict to get the name and source of the CSVs
    for csv_name, source_type in csvs_dict.items():
        # Check if the csv is valid using check_csv()
        if check_csv(csv_name):
            # Convert the CSV using convert_csv_to_df() and assign it to temp
            temp = convert_csv_to_df(csv_name, source_type)
            # Concatenate combined and temp and assign it to combined
            combined = pd.concat([combined, temp])
        # If the file is not valid, print a message with the CSV's name
        else:
            print(source_type + " is not a valid file and will not be added.")
    # Return the combined DataFrame
    return combined

my_files = {
  "datasets/2020Q4_nps_email.csv": "email",
  "datasets/2020Q4_nps_web.csv": "web",
  "datasets/2020Q4_nps_mobile.csv": "mobile",
  "datasets/corrupted.csv": "social_media"
}

# Test the function on the my_files dictionary
combine_nps_csvs(my_files)


# In[7]:


get_ipython().run_cell_magic('nose', '', '\nimport inspect\nimport pandas as pd\n\n# correct answer\ndef correct_combine(csvs_dict):\n    combined = pd.DataFrame()\n    for csv_name, source_type in csvs_dict.items():\n        if check_csv(csv_name):\n            temp = convert_csv_to_df(csv_name, source_type)\n            combined = pd.concat([combined, temp])\n        # else:\n          #  print(csv_name + " is not a valid file and will not be added.")\n    return combined\n\nmy_files = {\n  "datasets/2020Q4_nps_email.csv": "email",\n  "datasets/2020Q4_nps_web.csv": "web",\n  "datasets/2020Q4_nps_mobile.csv": "mobile",\n  "datasets/corrupted.csv": "social_media"\n}\n\ncorrect_ans = correct_combine(my_files)\nuser_ans = combine_nps_csvs(my_files)\n\ndef test_combine():\n    # check that combine_nps_csvs() has been defined\n    assert inspect.isfunction(combine_nps_csvs), \\\n    \'Did you define a function with the name `combine_nps_csvs`?\'  \n    # check num of arguments is 1\n    assert len(inspect.signature(combine_nps_csvs).parameters) == 1, \\\n    \'Your function should have one argument: csvs_dict.\'\n    assert len(inspect.signature(combine_nps_csvs).parameters) == 1, \\\n    \'Your function should have one argument: csvs_dict.\'\n    # check that a dataframe is returned\n    assert isinstance(user_ans, pd.DataFrame), \\\n    \'Your function should return a DataFrame.\'\n    # check that there are no more that 6906 rows\n    assert user_ans.shape[0] <= correct_ans.shape[0], \\\n    "Are you only including data from valid CSV files? It looks like your function is returning more rows than expected."\n    assert user_ans.shape[0] >= correct_ans.shape[0], \\\n    "It looks like your function is returning fewer rows than expected."\n    # catch all\n    assert user_ans.equals(user_ans), \\\n    \'Your function is not returning the expected output.\'')


# ## 4. Detractors, Passives, and Promoters
# <p>We've summarized our colleague's script into one function: <code>combine_nps_csvs()</code>! Let's move on to analyzing the NPS data, such as actually calculating NPS. As a reminder, NPS works by asking <em>How likely is it that you would recommend our product to a friend or colleague?</em> with a rating scale of 0 to 10.</p>
# <p>NPS ratings are categorized into three groups. Ratings between 0 to 6 are <strong>detractors</strong>, ratings between 7 to 8 are <strong>passives</strong>, and finally, ratings 9 to 10 are <strong>promoters</strong>. There's more to analyzing NPS, but remember, functions should be small in scope and should just "do one thing". So before we get ahead of ourselves, let's write a simple function that takes an NPS rating and categorizes it into the appropriate group.</p>

# In[8]:


def categorize_nps(x):
    """ 
    Takes a NPS rating and outputs whether it is a "promoter", 
    "passive", "detractor", or "invalid" score. "invalid" is
    returned when the score is not between 0-10.

    Args:
        x: The NPS rating

    Returns:
        String: the NPS category or "invalid".
    """
    # Write the rest of the function to match the docstring    
    if x == 9 or x == 10:
        return 'promoter'
    elif x == 7 or x == 8:
        return'passive'
    elif x >= 0 and x <= 6:
        return 'detractor'
    else:
        return "invalid"

# Test the function 
categorize_nps(8)


# In[9]:


get_ipython().run_cell_magic('nose', '', 'import inspect\nimport pandas as pd\n\ndef correct_cat(x):\n    if x == 9 or x == 10:\n        return \'promoter\'\n    elif x == 7 or x == 8:\n        return\'passive\'\n    elif x >= 0 and x <= 6:\n        return \'detractor\'\n    else:\n        return "invalid"\n    \ntest_series = pd.Series(range(-100,101))\n\ndef test_categorize():\n    # check that categorize_nps() has been defined\n    assert inspect.isfunction(categorize_nps), \\\n    \'Did you define a function with the name `categorize_nps`?\'  \n    # check num of arguments is 1\n    assert len(inspect.signature(categorize_nps).parameters) == 1, \\\n    \'Your function should have one argument: a rating.\'\n    # check that a string is returned\n    assert isinstance(categorize_nps(8432), str), \\\n    \'Your function should always return a string.\'\n    # check that a string is returned\n    assert isinstance(categorize_nps(2), str), \\\n    \'Your function should always return a string.\'\n    # catch all with ignoring case\n    assert (test_series.apply(categorize_nps).str.lower()).equals(test_series.apply(correct_cat).str.lower()), \\\n    "Your function is not returning the right string. Double check your code\'s logic for categorizing a rating."')


# ## 5. Applying our function to a DataFrame
# <p>So we have a function that takes a score and outputs which NPS response group it belongs to. It would be great to have this as a column in our NPS DataFrames, similar to the <code>source</code> column we added. Since we've modularized our code with functions, all we need to do is edit our <code>convert_cvs_to_df()</code> function and nest <code>categorize_nps()</code> into it. However, the way we'll nest <code>categorize_nps()</code> will be different than previous times. The <code>pandas</code> library has a handy function called <code>apply()</code>, which lets us apply a function to each column or row of a DataFrame. </p>

# In[10]:


def convert_csv_to_df(csv_name, source_type):  
    """ Convert an NPS CSV into a DataFrame with columns for the source and NPS group.

    Args:
        csv_name (str): The name of the NPS CSV file.
        source_type (str): The source of the NPS responses.

    Returns:
         A DataFrame with the CSV data and columns: source and nps_group.
    """
    df = pd.read_csv(csv_name)
    df['source'] = source_type
    # Define a new column nps_group which applies categorize_nps to nps_rating
    df['nps_group'] = df['nps_rating'].apply(categorize_nps)
    return df

# Test the updated function with mobile data
convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")


# In[11]:


get_ipython().run_cell_magic('nose', '', '\nimport inspect\nimport pandas as pd\n\ndef correct_convert(csv_name, source_type):    \n    df = pd.read_csv(csv_name)\n    df[\'source\'] = source_type\n    # Define a new column nps_group which applies categorize_nps to nps_rating\n    df[\'nps_group\'] = df[\'nps_rating\'].apply(categorize_nps)\n    return df\n\nuser_df = convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")\n\ndef test_new_convert():\n    # check num of arguments is 2\n    assert len(inspect.signature(convert_csv_to_df).parameters) == 2, \\\n    \'`convert_csv_to_df()` should still have two arguments: the name of the CSV file and the source type. Both of which are strings.\'\n    # check that a dataframe being returned\n    assert isinstance(user_df, pd.DataFrame), \\\n    \'`convert_csv_to_df()` should still return a DataFrame.\'\n    # see if source column is there\n    assert \'nps_group\' in user_df.columns, \\\n    \'Your function should add a column called `nps_group` to the DataFrame.\'\n    # check that it now returns a df with 5 cols\n    assert len(user_df.columns) == 5, \\\n    \'`convert_csv_to_df()` should return a DataFrame with five columns: `response_date`, `user_id`, `nps_rating`, `source`, and `nps_group`.\'\n    # catch all\n    assert correct_convert("datasets/2020Q4_nps_email.csv", "email").equals(convert_csv_to_df("datasets/2020Q4_nps_email.csv", "email")), \\\n    \'Your function is not returning the expected output.\'')


# ## 6. Calculating the Net Promoter Score
# <p>If we hadn't broken down our code into functions earlier, we would've had to edit our code in multiple places to add a <code>nps_group</code> column, increasing the chance of introducing errors. It also helps that our functions have one responsibility keeping our code flexible and easier to edit and debug.</p>
# <p>Now we're in a good place to calculate the Net Promoter Score! This is calculated by subtracting the percentage of detractor ratings from the percentage of promoter ratings, in other words:</p>
# <p>$
# NPS = \frac{\text{# of Promoter Rating - # of Detractor Ratings}}{\text{Total # of Respondents}} * 100
# $</p>
# <p>We want to calculate the NPS across all sources, so we'll use <code>combine_nps_csvs()</code> from Task 3 to consolidate the source files. As expected, that will output a DataFrame which we'll use as an input for a new function we're going to write, <code>calculate_nps()</code>. </p>

# In[12]:


# Define a function calculate_nps that takes a DataFrame
def calculate_nps(nps_df):
    # Calculate the NPS score using the nps_group column 
    counts = nps_df['nps_group'].value_counts()
    detractor = counts['detractor']
    promotor = counts['promoter']
    total = counts.sum()
    # Return the NPS Score
    return ((promotor-detractor)/ total) * 100

my_files = {
  "datasets/2020Q4_nps_email.csv": "email",
  "datasets/2020Q4_nps_web.csv": "web",
  "datasets/2020Q4_nps_mobile.csv": "mobile",
}

# Test the function on the my_files dictionary
q4_nps = combine_nps_csvs(my_files)
calculate_nps(q4_nps)


# In[13]:


get_ipython().run_cell_magic('nose', '', 'import inspect\n\n# forget to multiply by 100\ndef wrong_calc(nps_df):\n    counts = nps_df[\'nps_group\'].value_counts()\n    detractor = counts[\'detractor\']\n    promotor = counts[\'promoter\']\n    total = counts.sum()\n    return (promotor-detractor)/ total\n\ndef correct_calc(nps_df):\n    counts = nps_df[\'nps_group\'].value_counts()\n    detractor = counts[\'detractor\']\n    promotor = counts[\'promoter\']\n    total = counts.sum()\n    return ((promotor-detractor)/ total)*100\n\ndef correct_convert(csv_name, source_type):    \n    df = pd.read_csv(csv_name)\n    df[\'source\'] = source_type\n    # Define a new column nps_group which applies categorize_nps to nps_rating\n    df[\'nps_group\'] = df[\'nps_rating\'].apply(categorize_nps)\n    return df\n\nmy_files = {\n  "datasets/2020Q4_nps_email.csv": "email",\n  "datasets/2020Q4_nps_web.csv": "web",\n  "datasets/2020Q4_nps_mobile.csv": "mobile",\n}\n\n# Test the function on the my_files dictionary\nq4_nps = combine_nps_csvs(my_files)\nuser_ans = calculate_nps(q4_nps)\n\n\ndef test_calc():\n    # check num of arguments is 1\n    assert len(inspect.signature(calculate_nps).parameters) == 1, \\\n    "Your function should have one argument, a DataFrame"\n    # returning float\n    assert isinstance(user_ans, float), \\\n    "Your function should return a float. Make sure you\'re not rounding at any point of the calculation."\n    # did they forget to multiply by 100\n    assert calculate_nps(correct_convert("datasets/2020Q4_nps_mobile.csv", "mobile")) != wrong_calc(correct_convert("datasets/2020Q4_nps_mobile.csv", "mobile")), \\\n    "Did you forget to multiply by 100?"\n    # are they calculating it right?\n    assert calculate_nps(correct_convert("datasets/2020Q4_nps_mobile.csv", "mobile")) == calculate_nps(correct_convert("datasets/2020Q4_nps_mobile.csv", "mobile")), \\\n    "Your function is incorrectly calculating NPS. Make sure to follow the logic of the provided formula."')


# ## 7. Breaking down NPS by source
# <p>Is it good to have an NPS score around 10? The worst NPS score you can get is -100 when all respondents are detractors, and the best is 100 when all respondents are promoters. Depending on the industry of your service or product, average NPS scores vary a lot. However, a negative score is a bad sign because it means you have more unhappy customers than happy customers. Typically, a score over 50 is considered excellent, and above 75 is considered best in class.</p>
# <p>Although our score is above 0, it's still on the lower end of the spectrum. The product team concludes that majorly increasing NPS across our customer base is a priority. Luckily, we have this NPS data that we can analyze more so we can find data-driven solutions. A good start would be breaking down the NPS score by the source type. For instance, if people are rating lower on the web than mobile, that's some evidence we need to improve the browser experience.</p>

# In[14]:


# Define a function calculate_nps_by_source that takes a DataFrame
def calculate_nps_by_source(nps_df):
    # Add docstring
    """ uses check_csv() and convert_csv_to_df() to convert valid files into DataFrames and combines the resulting DataFrames into one DataFrame

    Args:
        csvs_dict (dict): The dataframe to calculate on.
        csv_name: The name of the CSV
        source_type: The CSV source

    Returns:
        DataFrame: The combined DataFrame of combined and temp
    """
    # Group the DataFrame by source and apply calculate_nps()
    x = nps_df.groupby(['source']).apply(calculate_nps)
    # Return a series with the NPS scores broken by source
    return x


my_files = {
  "datasets/2020Q4_nps_email.csv": "email",
  "datasets/2020Q4_nps_web.csv": "web",
  "datasets/2020Q4_nps_mobile.csv": "mobile",
}

# Test the function on the my_files dictionary
q4_nps = combine_nps_csvs(my_files)
calculate_nps_by_source(q4_nps)


# In[15]:


get_ipython().run_cell_magic('nose', '', '\nimport inspect\nimport pandas as pd\n\ndef correct_calc(nps_df):\n    counts = nps_df[\'nps_group\'].value_counts()\n    detractor = counts[\'detractor\']\n    promotor = counts[\'promoter\']\n    total = counts.sum()\n    return ((promotor-detractor)/ total)*100\n\ndef correct_by_source(nps_df):\n    x = nps_df.groupby([\'source\']).apply(correct_calc)\n    return x\n\nmy_files = {\n  "datasets/2020Q4_nps_email.csv": "email",\n  "datasets/2020Q4_nps_web.csv": "web",\n  "datasets/2020Q4_nps_mobile.csv": "mobile",\n}\n\n# Test the function on the my_files dictionary\nq4_nps = combine_nps_csvs(my_files)\nuser_ans = calculate_nps_by_source(q4_nps)\ncorr_ans = correct_by_source(q4_nps)\n\n\ndef test_calc():\n    # check num of arguments is 1\n    assert len(inspect.signature(calculate_nps_by_source).parameters) == 1, \\\n    "Your function should have one argument, a DataFrame"\n    # returning float\n    assert isinstance(user_ans, pd.Series), \\\n    "Your function should return a Series with the NPS scores broken by source."\n    # are they calculating it right?\n    assert user_ans.equals(corr_ans), \\\n    "Your function is incorrectly calculating NPS. Make sure to follow the logic of the provided formula."')


# ## 8. Adding docstrings
# <p>Interesting! The mobile responses have an NPS score of about -15, which is noticeably lower than the other two sources. There are few ways we could continue our analysis from here. We could use the column <code>user_id</code> to reach out to users who rated poorly on the mobile app for user interviews. We could also breakdown NPS by source and date to see if there was a date where NPS started clearly decreasing - perhaps the same time there was a bug or feature realeased. With the functions we created, Brenda is in a good place to continue this work!</p>
# <p>The last thing we'll discuss is docstrings. In Task 1, 2, 4 and 5, we included docstrings for <code>convert_csv_to_df()</code>, <code>check_csv()</code>, and <code>categorize_nps()</code>. However, we should include docstrings for all the functions we write so that others can better re-use and maintain our code. Docstrings tell readers what a function does, its arguments, its return value(s) if any, and any other useful information you want to include, like error handling. There are several standards for writing docstrings in Python, including: <a href="https://numpydoc.readthedocs.io/en/latest/format.html">Numpydoc</a>, <a href="https://google.github.io/styleguide/pyguide.html">Google-style</a> (chosen style in this notebook), and <a href="https://www.python.org/dev/peps/pep-0287/">reStructuredText</a>.</p>
# <p>To make sure Brenda and other colleagues can follow our work, we are going to add docstrings to the remaining undocumented functions: <code>combine_nps_csvs()</code>, <code>calculate_nps()</code>, and <code>calculate_nps_by_source</code>. It's up to you how you want to write the docstrings - we'll only check that a docstring exists for each of these functions. </p>

# In[16]:


# Copy and paste your code for the function from Task 3
def combine_nps_csvs(csvs_dict):
    # Add docstring
    """Combines multiple CSV files into a single Pandas DataFrame.

    Args:
        csvs_dict (dict): A dictionary of CSV filenames and their source type.

    Returns:
        pandas.DataFrame: A combined DataFrame of all CSV files.
    """
    # Define combine as an empty DataFrame
    combined = pd.DataFrame()
    # Iterate over csvs_dict to get the name and source of the CSVs
    for csv_name, source_type in csvs_dict.items():
        # Check if the csv is valid using check_csv()
        if check_csv(csv_name):
            # Convert the CSV using convert_csv_to_df() and assign it to temp
            temp = convert_csv_to_df(csv_name, source_type)
            # Concatenate combined and temp and assign it to combined
            combined = pd.concat([combined, temp])
        # If the file is not valid, print a message with the CSV's name
        else:
            print(source_type + " is not a valid file and will not be added.")
    # Return the combined DataFrame
    return combined
    
# Copy and paste your code for the function from Task 6
def calculate_nps(nps_df):
    # Add docstring
    """Calculates the NPS score of a Pandas DataFrame.

    Args:
        nps_df (pandas.DataFrame): The DataFrame to calculate the NPS score on.

    Returns:
        float: The NPS score as a percentage.
    """
    # Calculate the NPS score using the nps_group column 
    counts = nps_df['nps_group'].value_counts()
    detractor = counts['detractor']
    promotor = counts['promoter']
    total = counts.sum()
    # Return the NPS Score
    return ((promotor-detractor)/ total) * 100
    
# Copy and paste your code for the function from Task 7
def calculate_nps_by_source(nps_df):
    # Add docstring
    """Calculates the NPS score for each source type in a Pandas DataFrame.

    Args:
        nps_df (pandas.DataFrame): The DataFrame to calculate NPS scores on.

    Returns:
        pandas.Series: A series of NPS scores broken down by source type.
    """
    # Group the DataFrame by source and apply calculate_nps()
    x = nps_df.groupby(['source']).apply(calculate_nps)
    # Return a series with the NPS scores broken by source
    return x


# In[17]:


get_ipython().run_cell_magic('nose', '', '\nimport inspect\n\ncom = combine_nps_csvs.__doc__\ncalc1 = calculate_nps.__doc__\ncalc2 = calculate_nps_by_source.__doc__\n\n\ndef test_docs():\n    assert (com is not None), \\\n    "It looks like there is no docstring for `combine_nps_csvs()`. Did you enclose the docstring in triple quotes?"\n    assert (calc1 is not None), \\\n    "It looks like there is no docstring for `calculate_nps()`. Did you enclose the docstring in triple quotes?"\n    assert (calc2 is not None), \\\n    "It looks like there is no docstring for `calculate_nps_by_source()`. Did you enclose the docstring in triple quotes?"\n    ')


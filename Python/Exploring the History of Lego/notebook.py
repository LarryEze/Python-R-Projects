#!/usr/bin/env python
# coding: utf-8

# ## 1. Introduction
# <p>Everyone loves Lego (unless you ever stepped on one). Did you know by the way that "Lego" was derived from the Danish phrase leg godt, which means "play well"? Unless you speak Danish, probably not. </p>
# <p>In this project, we will analyze a fascinating dataset on every single Lego block that has ever been built!</p>
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_10/datasets/lego-bricks.jpeg" alt="lego"></p>

# In[88]:


# Nothing to do here


# In[89]:


get_ipython().run_cell_magic('nose', '', 'def test_default():\n  assert True')


# ## 2. Reading Data
# <p>A comprehensive database of lego blocks is provided by <a href="https://rebrickable.com/downloads/">Rebrickable</a>. The data is available as csv files and the schema is shown below.</p>
# <p><img src="https://s3.amazonaws.com/assets.datacamp.com/production/project_10/datasets/downloads_schema.png" alt="schema"></p>
# <p>Let us start by reading in the colors data to get a sense of the diversity of Lego sets!</p>

# In[90]:


# Import pandas
import pandas as pd

# Read colors data
colors = pd.read_csv('datasets/colors.csv')

# Print the first few rows
colors.head()


# In[91]:


get_ipython().run_cell_magic('nose', '', '\ntest_colors = pd.read_csv(\'datasets/colors.csv\')\ndef test_colors_exists():\n    assert \'colors\' in globals(), "You should read the data into a variable named `colors`"\n    assert colors.equals(test_colors), "Did you read in the correct csv file?"')


# ## 3. Exploring Colors
# <p>Now that we have read the <code>colors</code> data, we can start exploring it! Let us start by understanding the number of colors available.</p>

# In[92]:


# How many distinct colors are available?
num_colors = colors['rgb'].size

# Print num_colors
print('Number of distinct colors:', num_colors)


# In[93]:


get_ipython().run_cell_magic('nose', '', 'def test_num_colors():\n    assert num_colors == 135, "The variable num_colors should equal 135"')


# ## 4. Transparent Colors in Lego Sets
# <p>The <code>colors</code> data has a column named <code>is_trans</code> that indicates whether a color is transparent or not. It would be interesting to explore the distribution of transparent vs. non-transparent colors.</p>

# In[94]:


# Summarize colors based on whether they are transparent or not?
colors_summary = colors.groupby('is_trans').count()
colors_summary


# In[95]:


get_ipython().run_cell_magic('nose', '', 'def test_colors_summary_exists():\n    assert \'colors_summary\' in globals(), "You should have defined a variable named `colors_summary`"\ndef test_colors_summary():\n    assert colors_summary.shape == (2, 3), "The DataFrame colors_summary should contain 2 rows and 3 columns"')


# ## 5. Explore Lego Sets
# <p>Another interesting dataset available in this database is the <code>sets</code> data. It contains a comprehensive list of sets over the years and the number of parts that each of these sets contained. </p>
# <p><img src="https://imgur.com/1k4PoXs.png" alt="sets_data"></p>
# <p>Let us use this data to explore how the average number of parts in Lego sets has varied over the years.</p>

# In[96]:


get_ipython().run_line_magic('matplotlib', 'inline')
# Read sets data as `sets`
sets = pd.read_csv('datasets/sets.csv')

# Create a summary of average number of parts by year: `parts_by_year`
parts_by_year = sets[['year', 'num_parts']].groupby('year').mean()

# Plot trends in average number of parts by year
parts_by_year.plot()


# In[97]:


get_ipython().run_cell_magic('nose', '', '\ntest_sets = pd.read_csv(\'datasets/sets.csv\')\n\ndef test_sets_exists():\n    assert \'sets\' in globals(), "You should read the data into a variable named `sets`"\n    assert sets.equals(test_sets), "Did you read in the correct csv file?"\n    \ndef test_parts_by_year_exists():\n    assert \'parts_by_year\' in globals(), "You should have defined a variable named `parts_by_year`"\n    assert len(parts_by_year) == 66, "Did you correctly group the `sets` DataFrame by year?"')


# ## 6. Lego Themes Over Years
# <p>Lego blocks ship under multiple <a href="https://shop.lego.com/en-US/Themes">themes</a>. Let us try to get a sense of how the number of themes shipped has varied over the years.</p>

# In[98]:


# themes_by_year: Number of themes shipped by year
themes_by_year = sets.groupby('year')[['theme_id']].nunique()
themes_by_year.head()


# In[99]:


get_ipython().run_cell_magic('nose', '', 'def test_themes_by_year_exists():\n    assert \'themes_by_year\' in globals(), "You should have defined a variable named `themes_by_year`"\ndef test_themes_by_year():\n    assert len(themes_by_year) == 66, "The DataFrame `themes_by_year` should contain 66 rows."\ndef test_themes_by_year_names():\n    colnames = [\'theme_id\']\n    assert all(name in themes_by_year for name in colnames), "Your DataFrame, bnames, should have the column `theme_id`."')


# ## 7. Wrapping It All Up!
# <p>Lego blocks offer an unlimited amount of fun across ages. We explored some interesting trends around colors, parts, and themes. Before we wrap up, let's take a closer look at the <code>themes_by_year</code> DataFrame you created in the previous step.</p>

# In[102]:


# Get the number of unique themes released in 1999
num_themes = themes_by_year.loc[1999,'theme_id']

# Print the number of unique themes released in 1999
print(num_themes)


# In[101]:


get_ipython().run_cell_magic('nose', '', 'def test_default():\n  assert True')


# In[ ]:





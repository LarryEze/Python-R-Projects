
# Load necessary packages
library(tidyverse)

# Load the data
responses <- read_csv("datasets/kagglesurvey.csv")

# Print the first 10 rows
print(responses, limit = 10)

library("testthat")
library('IRkernel.testthat')

run_tests({
    test_that("Read in data correctly.", {
        expect_is(responses, "tbl_df", 
            info = 'You should use read_csv() (with an underscore) to read "datasets/kagglesurvey.csv" into responses.')
    })
    
    test_that("Read in data correctly.", {
        responses_test <- read_csv('datasets/kagglesurvey.csv')
        expect_equivalent(responses, responses_test, 
            info = 'responses should contain the data in "datasets/kagglesurvey.csv".')
    })
    
})

# Printing the first respondent's tools and languages
responses[1, 2]

# Add a new column, and unnest the new column
tools <- responses  %>% 
    mutate(work_tools = str_split(WorkToolsSelect, ","))  %>% 
    unnest(work_tools)

# View the first 6 rows of tools
head(tools)

run_tests({
    test_that("Tools and Languages were Split and Unnested", {
        expect_true(nrow(tools) == 47409, 
            info = 'Make sure that you split the tools at the commas and unnested them.')
    })
    
    test_that("Tools and Languages were Unnested", {
        expect_is(tools$work_tools, "character", 
            info = 'The work_tools column should be of class "character". Make sure that you unnested the results of str_split().')
    })
    
})

# Group the data by work_tools, summarise the counts, and arrange in descending order
tool_count <- tools  %>% 
    group_by(work_tools)  %>% 
    summarise(count = n())  %>% 
    arrange(desc(count))

# Print the first 6 results
head(tool_count)

run_tests({
    test_that("Tools were Grouped and Summarised", {
        expect_true(nrow(tool_count) == 50, 
            info = 'Make sure that you grouped by tools and then summarised the counts.')
    })
    
    test_that("Values were sorted correctly", {
        expect_true(tool_count[1, 2] == 6073, 
            info = 'Do not forget to sort your tool counts from largest to smallest.')
    })
    
})

# Create a bar chart of the work_tools column, most counts on the far right
ggplot(tool_count, aes(x = fct_reorder(work_tools, count), y = count)) + 
    geom_bar(stat = "identity") +
    theme(axis.text.x  = element_text(angle=90, vjust=0.5, hjust= 1))

run_tests({
   test_that("Plot is a bar chart",{
      p <- last_plot()
      q <- p$layers[[1]]
      expect_is(q$geom, "GeomBar", 
                info = "You should plot a bar chart with ggplot().")
    })
})

# Create a new column called language preference
debate_tools <- responses  %>% 
    mutate(language_preference = case_when(
        str_detect(WorkToolsSelect, "R") & ! str_detect(WorkToolsSelect, "Python") ~ "R",
        str_detect(WorkToolsSelect, "Python") & ! str_detect(WorkToolsSelect, "R") ~ "Python",
        str_detect(WorkToolsSelect, "R") & str_detect(WorkToolsSelect, "Python")   ~ "both",
        TRUE ~ "neither"
    ))


# Print the first 6 rows
head(debate_tools)

debate_tools_counts <- debate_tools %>% 
    count(language_preference)

run_tests({
    test_that("New column was created", {
        expect_is(debate_tools$language_preference, "character", 
            info = 'The language_preference column should be of class "character". Make sure that you filled this new column correctly.')
    })
    test_that("Language preferences are correct", {
        expect_equal(filter(debate_tools_counts, language_preference == "both")  %>% pull(n), 3660, 
            info = 'There is an incorrect amount of "both". Please check the case_when() statements.')
        expect_equal(filter(debate_tools_counts, language_preference == "neither")  %>% pull(n), 2860, 
            info = 'There is an incorrect amount of "neither". Please check the case_when() statements.')
        expect_equal(filter(debate_tools_counts, language_preference == "Python")  %>% pull(n), 2413, 
            info = 'There is an incorrect amount of "Python". Please check the case_when() statements.')
        expect_equal(filter(debate_tools_counts, language_preference == "R")  %>% pull(n), 1220, 
            info = 'There is an incorrect amount of "R". Please check the case_when() statements.')
        
    })
    
})

# Group by language preference, calculate number of responses, and remove "neither"
debate_plot <- debate_tools %>% 
    group_by(language_preference)  %>%
    summarise(count = n())  %>% 
    filter(!language_preference == "neither")

# Creating a bar chart
ggplot(debate_plot, aes(x = language_preference, y = count)) + 
  geom_bar(stat = "identity")

run_tests({
   test_that("Plot is a bar chart",{
      p <- last_plot()
      q <- p$layers[[1]]
      expect_is(q$geom, "GeomBar",
               info = "You should plot a bar chart with ggplot().")
    })
})

# Group by, summarise, arrange, mutate, and filter
recommendations <- debate_tools  %>% 
    group_by(language_preference, LanguageRecommendationSelect)  %>%
    summarise(count = n())  %>% 
    arrange(language_preference, desc(count))  %>% 
    mutate(row = row_number()) %>% 
    filter(row <= 4)

run_tests({
    test_that("Tools have been summarised", {
        expect_true(nrow(recommendations) == 16, 
            info = 'Make sure that you are only keeping the top 4 responses for each language used.')
    })
    
})

# Create a faceted bar plot
ggplot(recommendations, aes(x = LanguageRecommendationSelect, y = count)) +
    geom_bar(stat = "identity") + 
    facet_wrap(~language_preference)

run_tests({
   test_that("Plot is a bar chart",{
      p <- last_plot()
      q <- p$layers[[1]]
      expect_is(q$geom, "GeomBar",
               info = "You should plot a bar chart with ggplot().")
    })
})

# Would R users find this statement TRUE or FALSE?
R_is_number_one = TRUE

run_tests({
    test_that("The question has been answered", {
        expect_true(R_is_number_one, 
            info = 'Try again! Should R_is_number_one be set to TRUE or FALSE?')
    })
    
})

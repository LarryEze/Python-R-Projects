
## 1. Data on tags over time
<p>How can we tell what programming languages and technologies are used by the most people? How about what languages are growing and which are shrinking, so that we can tell which are most worth investing time in?</p>
<p>One excellent source of data is <a href="https://stackoverflow.com/">Stack Overflow</a>, a programming question and answer site with more than 16 million questions on programming topics. By measuring the number of questions about each technology, we can get an approximate sense of how many people are using it. We're going to use open data from the <a href="https://data.stackexchange.com/">Stack Exchange Data Explorer</a> to examine the relative popularity of languages like R, Python, Java and Javascript have changed over time.</p>
<p>Each Stack Overflow question has a <strong>tag</strong>, which marks a question to describe its topic or technology. For instance, there's a tag for languages like <a href="https://stackoverflow.com/tags/r">R</a> or <a href="https://stackoverflow.com/tags/python">Python</a>, and for packages like <a href="https://stackoverflow.com/questions/tagged/ggplot2">ggplot2</a> or <a href="https://stackoverflow.com/questions/tagged/pandas">pandas</a>.</p>
<p><img src="https://assets.datacamp.com/production/project_435/img/tags.png" alt="Stack Overflow tags"></p>
<p>We'll be working with a dataset with one observation for each tag in each year. The dataset includes both the number of questions asked in that tag in that year, and the total number of questions asked in that year.</p>

# Load package
library(readr)
library(dplyr)

# Load dataset
by_tag_year <- read_csv("datasets/by_tag_year.csv")

# Inspect the dataset
print(by_tag_year)

# These packages need to be loaded in the first `@tests` cell. 
library(testthat) 
library(IRkernel.testthat)

# Then follows one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
run_tests({
    test_that("the answer is correct", {
    expect_true("readr" %in% .packages(), info = "Did you load the readr package?")
    expect_true("dplyr" %in% .packages(), info = "Did you load the dplyr package?")
    expect_is(by_tag_year, "tbl_df", 
        info = "Did you read in by_tag_year with read_csv (not read.csv)?")
    expect_equal(nrow(by_tag_year), 40518, 
        info = "Did you read in by_tag_year with read_csv?")
    })
})


# Add fraction column
by_tag_year_fraction <- by_tag_year %>%
  mutate(fraction = number / year_total)

# Print the new table
print(by_tag_year_fraction)

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
run_tests({
    test_that("the answer is correct", {
    expect_is(by_tag_year_fraction, "tbl_df", 
        info = "Did you create the by_tag_year_fraction object?")
    expect_true("fraction" %in% colnames(by_tag_year_fraction), 
        info = "Did you use mutate() to add a fraction column?")
    expect_equal(by_tag_year_fraction$fraction,
                 by_tag_year_fraction$number / by_tag_year_fraction$year_total,
        info = "Check how you computed the fraction column: is it the number divided by that year's total?")
    })
    # You can have more than one test
})

# Filter for R tags
r_over_time <- by_tag_year_fraction %>%
  filter(tag == "r")

# Print the new table
print(r_over_time)

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
run_tests({
    test_that("the answer is correct", {
    expect_is(r_over_time, "tbl_df",
        info = "Did you create an r_over_time object with filter()?")
    expect_equal(nrow(r_over_time), 11,
        info = "Did you filter just for the rows with the 'r' tag?")
    expect_true(all(r_over_time$tag == "r"),
        info = "Did you filter just for the rows with the 'r' tag?")
    })
    # You can have more than one test
})

# Load ggplot2
library(ggplot2)

# Create a line plot of fraction over time
ggplot(r_over_time) +
  geom_line(aes(x = year, y = fraction))

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.

get_aesthetics <- function(p) {
    unlist(c(list(p$mapping), purrr::map(p$layers, "mapping")))
}

run_tests({
    test_that("the answer is correct", {
        expect_true("ggplot2" %in% .packages(), info = "Did you load the ggplot2 package?")
        # expect_true("scales" %in% .packages(), info = "Did you load the scales package?")

        p <- last_plot()
        expect_is(p, "ggplot", info = "Did you create a ggplot figure?")
        expect_equal(length(p$layers), 1, info = "Did you create a plot with geom_line()?")
        expect_is(p$layers[[1]]$geom, "GeomLine", info = "Did you create a plot with geom_line()?")

        aesthetics <- get_aesthetics(p)
        expect_equal(rlang::quo_name(aesthetics$x), "year",
                     info = "Did you put year on the x-axis?")
        expect_equal(rlang::quo_name(aesthetics$y), "fraction",
                     info = "Did you put fraction on the y-axis?")
        
        # expect_equal(length(p$scales$scales), 1, info = "Did you add scale_y_continuous?")    
        # expect_equal(p$scales$scales[[1]]$labels(.03), "3.00%", info = "Did you make the y-axis a percentage?")
    })
})

# A vector of selected tags
selected_tags <- c("r", "dplyr", "ggplot2")

# Filter for those tags
selected_tags_over_time <- by_tag_year_fraction %>%
  filter(tag %in% selected_tags)

# Plot tags over time on a line plot using color to represent tag
ggplot(selected_tags_over_time, aes(x = year,
                                    y = fraction,
                                    color = tag)) +
  geom_line()

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.

get_aesthetics <- function(p) {
    unlist(c(list(p$mapping), purrr::map(p$layers, "mapping")))
}

run_tests({
    test_that("the answer is correct", {
        expect_true("ggplot2" %in% .packages(), info = "Did you load the ggplot2 package?")
        
        expect_is(selected_tags_over_time, "tbl_df",
                 info = "Did you create a selected_tags_over_time data frame?")

        expect_equal(nrow(selected_tags_over_time), 28,
                 info = "Did you filter for r, dplyr, and ggplot2 and save it to selected_tags_over_time?")

        expect_equal(sort(unique(selected_tags_over_time$tag)), c("dplyr", "ggplot2", "r"),
                 info = "Did you filter for r, dplyr, and ggplot2 and save it to selected_tags_over_time?")

        p <- last_plot()
        aesthetics <- get_aesthetics(p)
        expect_is(p, "ggplot", info = "Did you create a ggplot figure?")
        expect_equal(p$data, selected_tags_over_time, info = "Did you create your plot out of selected_tags_over_time?")
        
        expect_equal(length(p$layers), 1, info = "Did you create a plot with geom_line()?")
        expect_is(p$layers[[1]]$geom, "GeomLine", info = "Did you create a plot with geom_line()?")

        expect_true(!is.null(aesthetics$x), info = "Did you put year on the x-axis?")
        expect_equal(rlang::quo_name(aesthetics$x), "year",
                     info = "Did you put year on the x-axis?")

        expect_true(!is.null(aesthetics$y), info = "Did you put fraction on the y-axis?")
        expect_equal(rlang::quo_name(aesthetics$y), "fraction",
                     info = "Did you put fraction on the y-axis?")

        expect_true(!is.null(aesthetics$colour), info = "Did you put color on the x-axis?")
        expect_equal(rlang::quo_name(aesthetics$colour), "tag",
                     info = "Did you map the tag to the color?")

        # expect_equal(length(p$scales$scales), 1, info = "Did you add scale_y_continuous?")    
        # expect_equal(p$scales$scales[[1]]$labels(.03), "3.00%", info = "Did you make the y-axis a percentage?")
    })
    # You can have more than one test
})

# Find total number of questions for each tag
sorted_tags <- by_tag_year %>%
  group_by(tag) %>%
  summarize(tag_total = sum(number)) %>%
  arrange(desc(tag_total))

# Print the new table
print(sorted_tags)

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
run_tests({
    test_that("the answer is correct", {
        expect_is(sorted_tags, "tbl_df",
                 info = "Did you create a selected_tags_over_time data frame?")

        expect_equal(colnames(sorted_tags), c("tag", "tag_total"),
                 info = "Did you group by tag and summarize to create a tag_total column?")

        expect_equal(nrow(sorted_tags), length(unique(by_tag_year$tag)),
                 info = "Did you group by tag and summarize to create a tag_total column?")

        expect_equal(sorted_tags$tag_total,
                     sort(sorted_tags$tag_total, decreasing = TRUE),
                     info = "Did you arrange in descending order of tag_total?")
    })
})

# Get the six largest tags
highest_tags <- head(sorted_tags$tag)

# Filter for the six largest tags
by_tag_subset <- by_tag_year_fraction %>%
  filter(tag %in% highest_tags)

# Plot tags over time on a line plot using color to represent tag
ggplot(by_tag_subset, aes(x = year,
                          y = fraction,
                          color = tag)) +
  geom_line()

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
get_aesthetics <- function(p) {
    unlist(c(list(p$mapping), purrr::map(p$layers, "mapping")))
}

run_tests({
    test_that("the answer is correct", {
        expect_equal(sort(unique(by_tag_subset$tag)), sort(head(sorted_tags$tag, 6)),
                   info = "Did you filter by_tag_year_fraction for only the 6 most asked-about tags, and save it as by_tag_subset?")

        expect_equal(colnames(by_tag_subset), colnames(by_tag_year_fraction),
                   info = "Did you filter by_tag_year_fraction for only the 6 most asked-about tags, and save it as by_tag_subset?")

        p <- last_plot()
        expect_is(p, "ggplot", info = "Did you create a ggplot figure?")
        expect_equal(p$data, by_tag_subset, info = "Did you create your plot out of by_tag_subset?")
        
        expect_equal(length(p$layers), 1, info = "Did you create a plot with geom_line()?")
        expect_is(p$layers[[1]]$geom, "GeomLine", info = "Did you create a plot with geom_line()?")

        aesthetics <- get_aesthetics(p)
        expect_equal(rlang::quo_name(aesthetics$x), "year",
                     info = "Did you put year on the x-axis?")
        expect_equal(rlang::quo_name(aesthetics$y), "fraction",
                     info = "Did you put fraction on the y-axis?")
        expect_equal(rlang::quo_name(aesthetics$colour), "tag",
                     info = "Did you map the tag to the color?")

        # expect_equal(length(p$scales$scales), 1, info = "Did you add scale_y_continuous?")    
        # expect_equal(p$scales$scales[[1]]$labels(.03), "3.00%", info = "Did you make the y-axis a percentage?")
    })
})

# Get tags of interest
my_tags <- c("android", "ios", "windows-phone")

# Filter for those tags
by_tag_subset <- by_tag_year_fraction %>%
  filter(tag %in% my_tags)

# Plot tags over time on a line plot using color to represent tag
ggplot(by_tag_subset, aes(x = year,
                          y = fraction,
                          color = tag)) +
  geom_line()

# one or more tests of the students code. 
# The @solution should pass the tests.
# The purpose of the tests is to try to catch common errors and to 
# give the student a hint on how to resolve these errors.
get_aesthetics <- function(p) {
    unlist(c(list(p$mapping), purrr::map(p$layers, "mapping")))
}

run_tests({
    test_that("the answer is correct", {
        expect_equal(sort(my_tags), c("android", "ios", "windows-phone"),
                    info = "Did you create a vector my_tags of just android, ios, and windows-phone?")
        
        expect_equal(sort(unique(by_tag_subset$tag)), c("android", "ios", "windows-phone"),
                   info = "Did you filter by_tag_year_fraction for only ios, android, and windows-phone?")

        expect_equal(colnames(by_tag_subset), colnames(by_tag_year_fraction),
                   info = "Did you filter by_tag_year_fraction for only the three requested tags, and save it as by_tag_subset?")

        p <- last_plot()
        expect_is(p, "ggplot", info = "Did you create a ggplot figure?")
        expect_equal(p$data, by_tag_subset, info = "Did you create your plot out of by_tag_subset?")
        
        expect_equal(length(p$layers), 1, info = "Did you create a plot with geom_line()?")
        expect_is(p$layers[[1]]$geom, "GeomLine", info = "Did you create a plot with geom_line()?")

        aesthetics <- get_aesthetics(p)
        expect_equal(rlang::quo_name(aesthetics$x), "year",
                     info = "Did you put year on the x-axis?")
        expect_equal(rlang::quo_name(aesthetics$y), "fraction",
                     info = "Did you put fraction on the y-axis?")
        expect_equal(rlang::quo_name(aesthetics$colour), "tag",
                     info = "Did you map the tag to the color?")

        # expect_equal(length(p$scales$scales), 1, info = "Did you add scale_y_continuous?")    
        # expect_equal(p$scales$scales[[1]]$labels(.03), "3.00%", info = "Did you make the y-axis a percentage?")
    })
})

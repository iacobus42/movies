Rotten Reviewers (And Studios and Actors)
=========================================
Problem Overview
----------------
[Rotten Tomatoes](http://www.rottentomatoes.com) aggregates movie reviews and rates 
each movie as being "fresh" or "rotten" based on the fraction of reviews for
the movie that were "fresh." However, this may not always provide the best 
estimation of whether a film is "fresh" or "rotten," particularly when the 
movie has a wide release and is nearly universally reviewed. Many reviewers 
may have interests that render their reviews for movies of certain genres to 
be harsher than their peers or may have an affinity for particularly actors, 
directors or studios. Additionally, some actors or studios may be more highly
rated in certain genres or years than in others. 

Conveniently, Rotten Tomatoes provides a possible method for exploring these 
questions. Rotten Tomatoes provides an API service from which data for a given 
movie, such as the complete cast listing, the director, the genres and the 
studio can be obtained. Additionally, it is possible to extract for each review
the reviewer name, publication, score (if provided) and whether the review was
"fresh" or "rotten." 

Using the Rotten Tomatoes API, I constructed a database containing information
about over 5,000 movies from 1998 to 2014. The database contains the review 
score and associated metadata (e.g., reviewer, publication, cast, genre and 
studio). Using this data, I constructed five sub-apps, each exploring 
how reviews are effected by each of the metadata listed above. Using the 
app, it is possible to visualize how harsh or forgiving a given reviewer or 
publication is or how the quality of films featuring a given actor changes 
by genre or over time. 

These visualizations provide insight into the dynamics of the review process and
the relative strengths and weaknesses of different actors and studios. The 
resulting information and knowledge is not only interesting but also relevant to
producing "unbiased" estimates of aggregated reviews. Producing unbiased 
estimates, such as the attempt detailed 
[here](http://www.beeradvocate.com/help/?topic=ratings),
is an area of active interest and is important given that reviews are generally
provided non-randomly. By considering the reviewer's prior history and 
preferences relative to the reviewer's peers, it may be possible to produce a
more objective score. 

The subapps are hosted at:

* [Visualizations by Studio](http://jacobsimmering.com:3838/studios/)
* [Visualizations by Actor](http://jacobsimmering.com:3838/actor/)
* [Visualizations by Genre](http://jacobsimmering.com:3838/genre/)
* [Visualizations by Reviewer](http://jacobsimmering.com:3838/reviewer/)
* [Visualizations by Publication](http://jacobsimmering.com:3838/publication/)

App Description
---------------
The app was originally written to exclusively use SQL commands to do the data
manipulations and aggregations. However, the app was extremely slow, taking
minutes to update. Profiling suggests whenever a SQL query contained a 
sub-query, such as that to get the films belonging to a given studio, 
performance was terrible. A simple query such as `select * from foo` ran 
very quickly. In order to get a functional application, the data manipulation
and aggregation was handed off to R after the data was pulled from the MySQL 
tables. This resulted in a 10 to 1000 fold improvement in app performance. 

The app contains five "sub-apps", each designed to provide the user with 
information about how a given reviewer, publication or studio rates/produces
content by genre and over time. The reviewer and publication features also
feature a comparsion of the reviewer's scores against peer scores for the same
film. A fourth sub-app describes how a given genre performs over time. The
fifth app visualizes how a user selected actor's films are rated over time and
by genre. Each app is discussed in greater detail below. 

### Studio
The `studio` sub-app provides information about how a given studio's films 
perform. The user is presented with a drop-down menu containing a list of 
all studios or multi-studio partnerships that have produced at least one of the
top 300 films in any of the years 1998 to 2014. On the right is a plot area. 
By default, it shows a plot of the performance of each of the entries of that
studio by genre. The light grey points are each movie's rating in the genre and
the larger, darker points are the mean for that genre for that studio. The size
of the "mean point" is proportional to the number of films in that genre. A 
dashed line describes the studio's mean rating, allowing the user to readily 
see what genres a given studio exceeds or under-performs in relative to 
the rest of its film. 

Above the plot is a nav bar allowing the user to change to the time series 
plot. This plot has a light grey point mapping to the release month and rating
of each film released by the studio. The dark connected points are the 
monthly mean rating for the studio. The blue line and shaded grey area are the
least squares estimate of the studio's changing performance over time and the
95% confidence interval around the mean. 

### Reviewer and Publication 
The reviewer and publication apps are very similar. Both contain a drop-down
menu from which the user can select any of the reviewer names or publications.
The graph to the right updates according to the user's selection. By default, 
it shows that reviewer/publication's mean "freshness" score by genre. 

Using the nav bar above the graphic, the user can change to the time plot. This
graphic has a point located at the mean freshness score for each month with 
the size of the point being proportional to the number of reviews released 
by that reviewer/publication in that month. The solid blue line is a 
[loess](http://en.wikipedia.org/wiki/Local_regression) semi-parametric estimate
of the mean. This helps evaluate the tendency of a reviewer's reviews to become
more or less harsh over time. 

The third plot, Compared to Other Reviewers/Compared to Other Outlets, describes
how the selected reviewer/outlet compares to its peers. The freshness score for
a movie can be understood as an estimate of the probability that a randomly 
selected review will be positive (e.g., fresh). This plot shows how the 
reviewer's selection of fresh/rotten changes by peer scores. Each film is 
plotted, although the scatter points are not very interesting. A loess curve
is fit and shown as the solid blue line. A line with a slope of 1/100 is shown
as the dashed line, this line is the "expected" fit if the reviewer's scores
were not consistently more or less harsh than his peers. A loess fit below this
line indicates harsher reviewers/outlets and above indicates more generous 
reviewers/outlets. 

### Genre
The user is presented with a drop-down menu from which they select their desired
genre. From here, they are presented with a time series plot showing the 
performance of films belong to that genre over time. A light grey point is 
placed for each film's review score according to its release month. The dark
black line is the mean score by month. The blue line and shaded region around
the line are the least squares estimate of the change in that genre's rating
over time and the 95\% CI around the mean. 

### Actor
The actor app allows the user to select any actor from the drop-down menu and 
visualize the performance of that actor's films. For reasons of speed and 
functionality (not to mention interest), all actors in that drop-down list have 
had more than 12 films with a credit released between 1998 and Q1 2014. By 
default, the plot area shows the ratings of films featuring the actor broken
down by genre. Each light grey point is a single film and the dark black point
is the mean by genre. The size of the black point reflects the number of films
in that genre. 

Using the nav bar, the user can change the plot area to show the actor's 
performance over time. Each point is the month and score of a movie featuring
the actor and the blue line is the loess estimated fit for the mean. The shaded
region is the 95% CI around that mean.

Detailed Methods
----------------

### Database Structure

Due to the lower system demands, greater documentation with Python and R and
the JSON format of the Rotten Tomatoes API, I opted to use MySQL over Oracle and 
APEX. A dump of the MySQL database (30.8 MB) can be found 
[here](http://jacobsimmering.com/documents/movies.sql). 
The MySQL database contains six tables. 

The first table, `mojo` contains four elements, 

* `id` (Primary key)
* `title`
* `release year`
* `release month`

The first element, `id`, is an int sequence starting at 1 and going to 5018. This 
maps to the top 300 movies from each year 1998 to 2013 and the films released 
in Q1 2014. The second element is a `VARCHAR` string that contains the title
of the film. The third and fourth elements are both ints that contain the 
month and year of the release date. 

The second table `rtid` provides a mapping from the titles derived from Box
Office Mojo to the Rotten Tomatoes IDs. These were obtained using the Rotten
Tomatoes API search feature using the title as the input string. The first 
matching result with the same year as from Box Office Mojo provided the 
Rotten Tomatoes ID. To this end, the table contains two elements, 

* `id` (Primary key)
* `rtid`

The `id` variable is the same as the `id` variable in the `mojo` table. This
provides a linkage from Rotten Tomatoes to the Box Office Mojo data. The Rotten
Tomatoes ID is given by the `rtid` variable, an int. Not all
of the searches returned a match, approximately 80% (4037) of the titles were 
mapped to a Rotten Tomatoes ID. 

The third table, `cast`, contains information about the casts of the various
films. This table contains 4 elements:

* `castPK` (Primary key)
* `rtid`
* `actorID`
* `actorName`

The `castPK` is an int that serves as the primary key. The variable `rtid` 
serves as the linkage to the other tables via the Rotten Tomatoes ID. The 
variables `actorID` and `actorName` provide information about the actor: 
`actorID` is the Rotten Tomatoes actor ID and is an int, `actorName` is the 
name of the actor and is a VARCHAR. While not strictly normalized, I opted 
against making a separate table to contain a mapping between `actorID` and 
`actorName`. Any analysis using this table would depend on a join and it did
not make sense to divide up the data only to merge it at the time of analysis. 

The fourth table, `metadata`, contains the Rotten Tomatoes metadata for the 
movie. Specifically, this table contains seven elements:

* `mpk` (Primary key)
* `rtid`
* `criticScore`
* `userScore`
* `director`
* `studio`
* `rating`
* `runTime`

`mpk` is a sequence primary key and is an int. `rtid` provides a mapping to the
other Rotten Tomatoes data and via `id` to the Box Office Mojo data. 
`criticScore` and `userScore` are both ints that contain the critic and user
scores on a scale of 0 to 100, respectively. The first director listed on 
Rotten Tomatoes for the film is stored as a VARCHAR labeled `director`. The 
studio that produced the film is contained in a VARCHAR as `studio`. The MPAA 
rating of the movie is contained in the VARCHAR element `rating` and the 
run-time, in minutes, is stored as an int labeled `runTime`. 

The fifth table contains information about each films genre, as classified by
Rotten Tomatoes. Each film can belong to a number of genres and so this was 
not combined with the metadata in `metadata`. Instead an additional table
named `genres` was constructed. This table has three elements, 

* `gpk` (Primary key)
* `rtid`
* `genre`

Where `gpk` is an int sequence and served as the primary key. `genre` is
a VARCHAR and contains a string describing the genre. Each `rtid` may occur
multiple times as the film may belong to multiple genres. 

The sixth table contains the reviews and is named `reviews`. It has 

* `reviewID` (Primary key)
* `rtid`
* `reviewer`
* `publication`
* `month`
* `year`
* `score`
* `fresh`

In this case, `reviewID` is an sequence int that serves as the primary key.
`rtid` provides the linkage to the other tables. `reviewer` and `publication`
are both VARCHARs that contain a string that is the reviewer's name and 
the publication's name, respectively. `month` and `year` describe the month
and year of the review publication. For the reviews with original scores 
provided by Rotten Tomatoes, each score was transformed to a 0-100 scale and
stored as an int in the `score` element. Finally, `fresh` is an int containing
0 or 1 depending on whether Rotten Tomatoes coded the review as `fresh` or 
`rotten`. 

### Obtaining the Data

Rotten Tomatoes only provides very limited lists of recent movies and does not
provide a meaningful way to filter these lists. The vast majority of films are
never reviewed and so a simple chronological ordering is not a practical 
source of titles. Instead, I populated the set of movies for analysis using the 
data on [Box Office Mojo](http://www.boxofficemojo.com). This website provides 
information about a film's gross, which is a meaningful variable to sort on. 

After sorting the tables by gross, I scrapped the top 300 movies for each 
year from 1998 to 2013 and for Q1 2014. The scrapping was done using Python 2.7
and Beautiful Soup 4 
([script](https://github.com/iacobus42/movies/blob/master/collection/getMojoTitles.py)).
This script parses the HTML of the Box Office Mojo website, abstracts the 
relevant data elements and writes them to a MySQL database using the `MySQLdb`
library. All data is insert using loops and `INSERT` SQL commands. 

The Rotten Tomatoes data was also obtained using Python. The data is JSON 
formatted. For the metadata, 
cast and genre information was obtained using [zachwill's Rotten Tomatoes Python
library](https://GitHub.com/zachwill/rottentomatoes). I wanted all of the 
reviews and so for the review data, I wrote my own API calls. The extensively 
commented scripts for each task are linked below:

* [Getting Rotten Tomatoes IDs](https://github.com/iacobus42/movies/blob/master/collection/getRottenTomatoesIDs.py)
* [Getting cast information](https://github.com/iacobus42/movies/blob/master/collection/getRTCastInfo.py)
* [Getting metadata and genres](https://github.com/iacobus42/movies/blob/master/collection/getMetaData.py)
* [Getting reviews](https://github.com/iacobus42/movies/blob/master/collection/getReviews.py)

As with the script that parses the Box Office Mojo table, each of these 
scripts used SQL `INSERT` commands to populate the MySQL tables. Additionally,
each of these scripts created the tables --- there is no other required SQL
code. 

### Analysis

As SQL provides essentially zero analytical capacity and no visualization 
ability, I opted to connect the MySQL database to R. R is a functional domain
specific language with a strong emphasis on data analysis and visualization 
and is rapidly becoming a dominant platform in data analytics and data mining. 
R provides simple, clear and powerful methods for manipulating and analyzing 
data. Additionally, the [`ggplot2`](http://cran.r-project.org/web/packages/ggplot2/index.html) 
package forms a very powerful graphical system for R and the 
[`shiny`](http://cran.r-project.org/web/packages/shiny/index.html) package makes
the creation of dynamic graphics and web apps much easier than traditional 
methods, such as PHP. 

A `shiny` app requires two separate files, `ui.R` and `server.R`. `ui.R` 
describes the front-end user interface, how the user change inputs and how the 
results and displayed. The `server.R` file describes processing done on those
inputs and contains the code for the generation of a graphic. The code for 
each of the `shiny` apps can be found on my 
[github repo](https://github.com/iacobus42/movies/tree/master/shiny). 

Consider
the [`studio` app](http://jacobsimmering.com:3838/studios/). The user is 
presented with a webpage with two elements, the first is a drop-down menu 
containing a list of the distinct studios in the Rotten Tomatoes data and the 
second is a plot of each film's review and the mean review by genre for all 
the movies produced by that studio. The front-end is coded as 

```
# loading required library
library(DBI)
library(RMySQL)
# setting up the MySQL connection
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
# grabbing the studio listing with sql from the metadata table
studios <- dbGetQuery(con, "select distinct studio from metadata")$studio
# releasing the connection to the database
dbDisconnect(con)

# this describes the UI and how input is accepted
shinyUI(pageWithSidebar(    
    headerPanel(""),
    sidebarPanel(
        # sets up a sidebar with a dropdown menu
        selectInput("studio", # the variable name for the backend
                    label = "Which Studio?", # the label on the dropdown menu
                    choices = studios, # the vector of options for the user
                    selected = studios[1])), # the default option
    mainPanel( 
        tabsetPanel(
        # sets up a two tabbed graph region
            # the genre graph, output id of genre_plot
            tabPanel("By Genre", plotOutput("genre_plot")),
            # the time series plot, output id of time_plot
            tabPanel("By Time", plotOutput("time_plot"))
))))
```

Rather simply, this code connects to a MySQL database named `movies` and 
performs the query shown to get a list of all the studios in the data. It then
describes a layout with a sidebar providing a drop-down box (`selectInput`) 
containing the results of the query and a main panel that contains an 
two tabs, one with a plot named `genre_plot` and the other with a plot named
`time_plot`. 

The `server.R` file is significantly more complex:
```
shinyServer(function(input, output) {
    # loading required librarys
    library(ggplot2)
    library(DBI)
    library(RMySQL)
    library(scales)
    # setting up the mysql connection
    m <- dbDriver("MySQL");
    con2 <- dbConnect(m, user='simmerin', 
                     password='simmerin',
                     host='localhost',
                     dbname='movies')
    # below describes the genre plot generation
    output$genre_plot <- renderPlot({
        # most of the data processing is done with R. The SQL resulted in a 
        # poorly performing app, often timing out. Using R for the processing
        # and aggregation sped up the app by 10-1000 fold. 
        # bringing in the scores from the metadata table
        scores <- dbGetQuery(con2, "select rtid, criticScore, studio from metadata")
        # bringing in the genre from the genres table
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        # bringing in the mapping between rtid and id
        link <- dbGetQuery(con2, "select rtid, id from rtid")
        # the mojo release dates
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2) # release the connection
        
        # dropping the films from other studios
        scores <- scores[scores$studio == input$studio, ]
        # merges does a natural join, drops unrelated ids
        data <- merge(scores, genres, by = "rtid") 
        # bringing in the linking between id and rtid
        data <- merge(data, link, by = "rtid") 
        # bringing in the release dates
        data <- merge(data, dates, by = "id")
        # formating as date for R
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        # getting mean/counts by genre
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        # getting mean/counts by month
        mByM <- aggregate(data$criticScore, by = list(data$date),
                          mean)
        cByM <- aggregate(rep(1, length(data$date)), 
                          list(data$date),
                          sum)
        # overall mean
        meanLine <- data.frame(meanLine = mean(data$criticScore, na.rm = TRUE))
        # grammar of graphics syntax to generate the genre plot shown on the app
        p <- ggplot() + 
            geom_point(aes(x = genre, y = criticScore), data = data, alpha = 0.25) + 
            geom_point(aes(x = Group.1, y = x), data = mByG, size = 10 * cByG$x/max(cByG$x)) + 
            geom_hline(aes(yintercept = meanLine), data = meanLine, lty = 2) + 
            theme_bw() + 
            scale_x_discrete(name = "") + 
            scale_y_continuous("Critic Score") + 
            theme(axis.text.x = element_text(angle = 90))
        print(p)
    })
    output$time_plot <- renderPlot({
                # most of the data processing is done with R. The SQL resulted in a 
        # poorly performing app, often timing out. Using R for the processing
        # and aggregation sped up the app by 10-1000 fold. 
        # bringing in the scores from the metadata table
        scores <- dbGetQuery(con2, "select rtid, criticScore, studio from metadata")
        # bringing in the genre from the genres table
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        # bringing in the mapping between rtid and id
        link <- dbGetQuery(con2, "select rtid, id from rtid")
        # the mojo release dates
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2) # release the connection
        
        # dropping the films from other studios
        scores <- scores[scores$studio == input$studio, ]
        # merges does a natural join, drops unrelated ids
        data <- merge(scores, genres, by = "rtid") 
        # bringing in the linking between id and rtid
        data <- merge(data, link, by = "rtid") 
        # bringing in the release dates
        data <- merge(data, dates, by = "id")
        # formating as date for R
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        # getting mean/counts by genre
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        # getting mean/counts by month
        mByM <- aggregate(data$criticScore, by = list(data$date),
                          mean)
        cByM <- aggregate(rep(1, length(data$date)), 
                          list(data$date),
                          sum)
        # overall mean
        meanLine <- data.frame(meanLine = mean(data$criticScore, na.rm = TRUE))
        # grammar of graphics syntax to generate the timeseries plot
        p <- ggplot() + 
            geom_point(aes(x = date, y = criticScore), data = data, alpha = 0.25) + 
            geom_point(aes(x = Group.1, y = x), data = mByM, size = cByM$x) + 
            geom_line(aes(x = Group.1, y = x), data = mByM) + 
            geom_smooth(aes(x = date, y = criticScore), data = data, method = "lm") + 
            theme_bw() +
            scale_x_date("", breaks = "1 years", labels = date_format("%Y")) + 
            scale_y_continuous("Critic Score")
        print(p)
    })
})
```

As with `ui.R`, a connection is established to the MySQL database named 
`movies`. The Rotten Tomatoes IDs and scores for the movies from the user 
provided studio (`input$studio`) are pulled out with the first query and stored 
as the `scores` object in R. The second query abstracts the Rotten Tomatoes IDs 
and genres for films provided by the user provided studio and the results are
stored as the R object `genres`. Testing indicated that a merge in R was 
significantly faster than a join using the MySQL connected database and so the
two data objects were merged along `rtid` in R. Testing again indicated that
there were significant performance advantages to doing the aggregation in R 
and so the mean and counts for each genre was computed in R using `aggregate`. 
The resulting data was then used to produce a plot `p`. Working with the 
plotting code, a point was placed at the location of each film's critic score
with a high degree of transparency, a second darker point was placed at the 
mean critic score for each genre with the size of the point being proportional 
to the number of films in that genre and a dashed line was drawn at the pooled 
mean. This plot is the `genre_plot` referenced in the `ui.R` file and is drawn
for the user. 

The other apps, `genre`, `actor`, `reviewer` and `publication` take a similar 
form. The code can be found in my 
[GitHub repo](https://github.com/iacobus42/movies/tree/master/shiny).

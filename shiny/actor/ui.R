library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
actors <- dbGetQuery(con, "select distinct actorName from cast")$actorName

shinyUI(pageWithSidebar(    
    headerPanel(""),
    sidebarPanel(
        selectInput("actor",
                    label = "Which actor?",
                    choices = actors,
                    selected = "Nicolas Cage")),
    mainPanel(
        plotOutput(outputId = "genre_plot"))))
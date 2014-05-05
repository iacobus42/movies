library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
cast <- dbGetQuery(con, "select actorName from cast")$actorName
actors <- aggregate(rep(1, length(cast)), list(cast), sum)
actors <- actors[actors$x >= 10, 1]
dbDisconnect(con)

shinyUI(pageWithSidebar(    
    headerPanel(""),
    sidebarPanel(
        selectInput("actor",
                    label = "Which actor?",
                    choices = actors,
                    selected = "Nicolas Cage")),
    mainPanel(
        tabsetPanel(
            tabPanel("By Genre", plotOutput("genre_plot")), 
            tabPanel("By Time", plotOutput("time_plot"))))
))

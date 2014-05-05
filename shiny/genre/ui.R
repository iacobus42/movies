library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
genres <- dbGetQuery(con, "select distinct genre from genres")$genre

shinyUI(fluidPage(theme = "http://jacobsimmering.com/documents/bootstrap.css",  
    headerPanel(""),
    sidebarPanel(
        selectInput("genre",
                    label = "What Genre?",
                    choices = genres,
                    selected = genres[1])),
    mainPanel(
        plotOutput(outputId = "genre_plot"))))

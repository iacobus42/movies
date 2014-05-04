library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
studios <- dbGetQuery(con, "select distinct studio from metadata")$studio
dbDisconnect(con)
shinyUI(pageWithSidebar(    
    headerPanel(""),
    sidebarPanel(
        selectInput("studio",
                    label = "Which Studio?",
                    choices = studios,
                    selected = studios[1])),
    mainPanel(
        tabsetPanel(
            tabPanel("By Genre", plotOutput("genre_plot")), 
            tabPanel("By Time", plotOutput("time_plot"))
))))

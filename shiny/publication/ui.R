library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
pubs <- dbGetQuery(con, "select distinct publication from reviews")$publication

shinyUI(fluidPage(
    titlePanel(""),
    sidebarLayout(
        sidebarPanel(
            selectInput("pub",
                        label = "Which Publication?",
                        choices = pubs,
                        selected = pubs[1])
        ),
        mainPanel(
            tabsetPanel(
                tabPanel("By Genre", plotOutput("genre_plot")), 
                tabPanel("By Time", plotOutput("time_plot")),
                tabPanel("Compared to Other Outlets", plotOutput("comp_plot"))
            )
        )
    )
))

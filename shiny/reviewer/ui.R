library(DBI)
library(RMySQL)
m <- dbDriver("MySQL");
con <- dbConnect(m, user='simmerin', 
                 password='simmerin',
                 host='localhost',
                 dbname='movies')
critic <- dbGetQuery(con, "select distinct reviewer from reviews")$reviewer

shinyUI(fluidPage(theme = "http://jacobsimmering.com/documents/bootstrap.css",  
    titlePanel(""),
    sidebarLayout(
        sidebarPanel(
            selectInput("critic",
                        label = "Which Reviewer?",
                        choices = critic,
                        selected = "A.O. Scott")
        ),
        mainPanel(
            tabsetPanel(
                tabPanel("By Genre", plotOutput("genre_plot")), 
                tabPanel("By Time", plotOutput("time_plot")),
                tabPanel("Compared to Other Reviewers", plotOutput("comp_plot"))
            )
        )
    )
))

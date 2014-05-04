shinyServer(function(input, output) {
    library(ggplot2)
    library(DBI)
    library(RMySQL)
    m <- dbDriver("MySQL");
    con2 <- dbConnect(m, user='simmerin', 
                      password='simmerin',
                      host='localhost',
                      dbname='movies')
    output$genre_plot <- renderPlot({
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        cast <- dbGetQuery(con2, "select rtid, actorName from cast")
        cast <- cast[cast$actorName == input$actor, ]
        scores <- scores[scores$rtid %in% cast$rtid, ]
        genres <- genres[genres$rtid %in% cast$rtid, ]

        data <- merge(scores, genres, by = "rtid")
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        meanLine <- mean(data$criticScore, na.rm = TRUE)
        p <- ggplot() + 
            geom_point(aes(x = genre, y = criticScore), data = data, alpha = 0.25) + 
            geom_point(aes(x = Group.1, y = x), data = mByG, size = 10 * cByG$x/max(cByG$x)) + 
            geom_hline(aes(yintercept = meanLine), lty = 2) + 
            theme_bw() + 
            scale_x_discrete(name = "") + 
            scale_y_continuous("Critic Score") + 
            theme(axis.text.x = element_text(angle = 90))
        print(p)
    })
})
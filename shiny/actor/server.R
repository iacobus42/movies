shinyServer(function(input, output) {
    library(ggplot2)
    library(DBI)
    library(RMySQL)
    output$genre_plot <- renderPlot({
        m <- dbDriver("MySQL");
        con2 <- dbConnect(m, user='simmerin', 
                          password='simmerin',
                          host='localhost',
                          dbname='movies')
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        cast <- dbGetQuery(con2, "select rtid, actorName from cast")
        dbDisconnect(con2)
        cast <- cast[cast$actorName == input$actor, ]
        scores <- scores[scores$rtid %in% cast$rtid, ]
        genres <- genres[genres$rtid %in% cast$rtid, ]

        data <- merge(scores, genres, by = "rtid")
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        meanLine <- data.frame(int = mean(data$criticScore, na.rm = TRUE))
        p <- ggplot() + 
            geom_point(aes(x = genre, y = criticScore), data = data, alpha = 0.25) + 
            geom_point(aes(x = Group.1, y = x), data = mByG, size = 10 * cByG$x/max(cByG$x)) + 
            geom_hline(aes(yintercept = int), data = meanLine, lty = 2) + 
            theme_bw() + 
            scale_x_discrete(name = "") + 
            scale_y_continuous("Critic Score") + 
            theme(axis.text.x = element_text(angle = 90))
        print(p)
    })
    output$time_plot <- renderPlot({
        m <- dbDriver("MySQL");
        con2 <- dbConnect(m, user='simmerin', 
                          password='simmerin',
                          host='localhost',
                          dbname='movies')
        scores <- dbGetQuery(con2, "select rtid, criticScore from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        cast <- dbGetQuery(con2, "select rtid, actorName from cast")
        link <- dbGetQuery(con2, "select rtid, id from rtid")
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2)
        cast <- cast[cast$actorName == input$actor, ]
        scores <- scores[scores$rtid %in% cast$rtid, ]        
        data <- merge(scores, genres, by = "rtid")
        data <- merge(data, link, by = "rtid")
        data <- merge(data, dates, by = "id")
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        p <- ggplot(data, aes(x = date, y = criticScore)) + 
            geom_point() + 
            geom_smooth(method = "loess") + 
            theme_bw() + 
            scale_x_date("", breaks = "1 years", labels = date_format("%Y")) + 
            scale_y_continuous("Critic Score")
        print(p)
    })
})
shinyServer(function(input, output) {
    library(ggplot2)
    library(scales)
    library(DBI)
    library(RMySQL)
    output$genre_plot <- renderPlot({
        m <- dbDriver("MySQL");
        con2 <- dbConnect(m, user='simmerin', 
                          password='simmerin',
                          host='localhost',
                          dbname='movies')
        scores <- dbGetQuery(con2, "select rtid, criticScore, studio from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        link <- dbGetQuery(con2, "select rtid, id from rtid")
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2)
        
        scores <- scores[scores$studio == input$studio, ]
        data <- merge(scores, genres, by = "rtid")
        data <- merge(data, link, by = "rtid")
        data <- merge(data, dates, by = "id")
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        mByM <- aggregate(data$criticScore, by = list(data$date),
                          mean)
        cByM <- aggregate(rep(1, length(data$date)), 
                          list(data$date),
                          sum)
        meanLine <- data.frame(meanLine = mean(data$criticScore, na.rm = TRUE))
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
        m <- dbDriver("MySQL");
        con2 <- dbConnect(m, user='simmerin', 
                          password='simmerin',
                          host='localhost',
                          dbname='movies')
        scores <- dbGetQuery(con2, "select rtid, criticScore, studio from metadata")
        genres <- dbGetQuery(con2, "select rtid, genre from genres")
        link <- dbGetQuery(con2, "select rtid, id from rtid")
        dates <- dbGetQuery(con2, "select id, month, year from mojo")
        dbDisconnect(con2)
        
        scores <- scores[scores$studio == input$studio, ]
        data <- merge(scores, genres, by = "rtid")
        data <- merge(data, link, by = "rtid")
        data <- merge(data, dates, by = "id")
        data$date <- as.Date(paste(data$year, data$month, "01", sep = "-"))
        mByG <- aggregate(data$criticScore, by = list(data$genre),
                          mean)
        cByG <- aggregate(rep(1, length(data$genre)), by = list(data$genre),
                          sum)
        mByM <- aggregate(data$criticScore, by = list(data$date),
                          mean)
        cByM <- aggregate(rep(1, length(data$date)), 
                          list(data$date),
                          sum)
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